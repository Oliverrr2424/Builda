# 系统总体方案

## 一、总体架构

- **Web 前端**：React + Next.js（支持 SSR/SSG，兼顾 SEO 与性能）
- **后端服务**：Python（FastAPI）
- **数据库**：PostgreSQL 搭配 pgvector 用于语义检索
- **缓存**：Redis（会话管理、RAG 检索缓存、频控）
- **数据抓取**：Playwright / Scrapy + 定时调度（GitHub Actions 或 AWS EventBridge）
- **LLM 网关**：优先 OpenAI GPT-4，备选 Azure OpenAI（企业合规）或 AWS Bedrock（Claude/Llama）
- **对象存储 / CDN**：Amazon S3 + CloudFront（或 Cloudflare）
- **监控 / 日志**：OpenTelemetry + Grafana/Prometheus（或 Datadog）
- **鉴权**：Auth0 / Clerk（或 AWS Cognito）
- **CI/CD**：GitHub Actions（测试、构建、部署）

> 说明：GPT-4 暂未在 AWS Bedrock 提供，如需 GPT-4 应选择 OpenAI 或 Azure OpenAI。合规优先场景推荐 Azure OpenAI 为主、OpenAI 为备；若坚持全 AWS 生态，可在 Bedrock 选用 Claude 系列替代。

## 二、数据侧：采集与模型化

### 2.1 数据源与更新策略
- **BestBuy**：官方 API（Products/Reviews），按 `categoryPath.id` 获取组件类目。
- **Amazon**：Product Advertising API，按 ASIN 拉取详情与价格，展示需标注来源。
- **Newegg**：缺少公共 API，采用 Playwright（Headless Chromium）+ 轮换代理 + 随机等待，遵循 robots.txt 与 TOS，仅抓取公开规格与价格。

**刷新节奏**
- 每隔两日执行全量扫描，发现新 SKU、下架或价格剧烈波动。
- 每日针对热度高或推荐过的 SKU 做价格与库存校准。

**合规与反爬**
- 限速、分布式代理、失败重试退避策略。
- 对敏感字段脱敏，严格标注来源与价格时间戳。

### 2.2 数据库设计

以 PostgreSQL + pgvector 为核心，主表 `products` 存储通用属性，细分表按品类拆分（如 `cpus`、`gpus` 等）。

关键字段：
- `products`：`id`、`global_sku`、标题、品牌、类别、来源、价格、库存、评分、`spec_json`、`scene_tags`、`perf_score`、`updated_at`。
- 各品类表：CPU（插槽、核心/线程、主/加速频率、TDP）、GPU（芯片、显存、TDP、长度）等。
- `product_prices`：价格历史。
- `build_templates` / `build_template_items`：预设装机方案。
- `dialogs`：对话、解析结果与推荐答案。
- `embeddings_*`：使用 `pgvector` 保存产品与方案的向量表示。

索引策略包括 `products(category, price, perf_score, scene_tags)` 组合索引与 `pgvector` 的 `ivfflat`。

## 三、AI 侧：RAG 流程与提示工程

### 3.1 主流程
1. **意图解析**：小模型或规则提取场景、预算、品牌偏好、尺寸需求、软件/游戏等要素。
2. **候选召回**：将需求文本嵌入后在 `embeddings_products` 与 `embeddings_cases` 中检索 K 个候选，结合价格、场景标签、性能分、规格兼容性进行筛选。
3. **组装器**：Python 规则层保证兼容性（插槽、内存类型、机箱尺寸、电源余量等），按预算优先满足性能阈值。
4. **LLM 决策**：将候选清单与约束输入 LLM，生成主方案、替代方案、解释与说明。
5. **输出**：结构化配置 JSON、对话文案、价格有效期与来源链接。

### 3.2 模型选型与路由
- 主生成：GPT-4（OpenAI 或 Azure OpenAI）。
- 轻量解析/分类：gpt-4o-mini、gpt-3.5-turbo 或微调后的 Llama-3-8B。
- 全 AWS 方案：Bedrock 的 Claude 3 替代 GPT-4，Cohere Embed 替代 OpenAI Embedding。
- Embedding：OpenAI `text-embedding-3-large`，必要时自托管 `nomic-embed-text`。
- FastAPI 暴露工具函数，配合 Function Calling。

### 3.3 关键 Prompt 模版
- **System Prompt**：设定“资深装机顾问”角色，强调真实数据、兼容性、解释、替代方案。
- **Planner Prompt**：隐藏链式思考，分析场景、预算分配与约束校验。
- **Generator Prompt**：输入候选 JSON 与约束，输出包含主方案、总价、替代方案与备注的结构化结果。

### 3.4 成本与性能优化
- Prompt 前缀缓存、对话摘要、RAG 优先命中。
- 用户频控、并发池、降级策略（GPT-4 → GPT-3.5/Claude）。
- 监控推荐成功率、用户修改次数与点击转化。

## 四、后端 API 契约（FastAPI）

- `POST /api/chat/plan`：根据对话返回装机方案、总价、替代方案、说明与价格时间戳。
- `GET /api/products/search`：按关键词、类别、价格区间、场景查询产品。
- `POST /api/builds/validate`：校验方案兼容性与功耗、电源建议。
- `GET /api/price/history`：返回指定产品的价格历史。
- `POST /api/feedback`：记录用户反馈、修改原因与购买情况。

鉴权采用 JWT（Auth0/Clerk），游客仅开放部分功能。

## 五、前端实现要点（Next.js）

- 聊天主视图：消息流与配置卡片结合。
- 配置卡片展示部件栅格、总价、来源跳转与替代方案切换。
- 可选过滤器：预算滑条、场景快捷按钮、机箱尺寸偏好。
- 提供一键复制清单、导出 PDF，支持 Streaming 输出、乐观 UI、错误提示。
- 状态管理：Zustand 或 Redux Toolkit；数据层使用 SWR/React Query。
- 移动端适配、国际化（中英）、货币与度量单位本地化。
- 埋点：跟踪提问→方案→外链点击→收藏等漏斗。

## 六、数据同步与清洗

- 调度：GitHub Actions/cron（UTC 3:00）触发容器化的同步任务。
- 流程：抓取 → 规格抽取 → 归一化 → 性能打分 → 标签标注 → 入库。
- 质量：脏数据检测、去重（`global_sku` 统一规则）。
- 合规：仅保存事实性规格与价格，图片链接保持原地址或许可缩略图。

## 七、监控、可观测与安全

- API 指标：P95 延迟、错误率、LLM 耗时与 token 成本。
- 数据指标：爬虫成功率、SKU 覆盖度、价格更新比率。
- 业务指标：推荐修改率、外链点击率、回访率。
- 告警：LLM 错误激增、价格更新超 48h、兼容性失败率高。
- 安全：HTTPS、CSP、依赖漏洞扫描、速率限制、WAF、密钥管理（Secrets Manager/Parameter Store）、最小权限。

## 八、里程碑规划（10–12 周）

- **Sprint 1（周 1–2）**：Next.js + FastAPI 脚手架、鉴权、Postgres/Redis 基础、最小对话流。
- **Sprint 2（周 3–4）**：数据接入与清洗、pgvector 建库、检索 API。
- **Sprint 3（周 5–6）**：完整 RAG 流程、兼容性校验、前端配置卡片。
- **Sprint 4（周 7–8）**：Prompt 优化、缓存、日志观测、A/B 测试、多语言。
- **Sprint 5（周 9–10）**：SEO、价格历史图、合规审计、灰度试运营。
- **Sprint 6（周 11–12）**：性能压测、风控、Bug 修复与上线准备。

## 九、MVP 验收标准

- 相同需求重复询问 90% 以上返回兼容且可购买方案。
- 价格时间戳 ≤ 48 小时，热销 SKU 日更命中率 ≥ 85%。
- 首 token 延迟 ≤ 2 秒，完整回答 ≤ 8 秒（RAG 命中时）。
- 用户对推荐修改不超过 2 处即可满足需求。
- 所有商品具备来源回链与合规声明。

## 十、落地清单

- Docker Compose 环境（web/api/db/redis/worker）。
- 前端依赖：`next`、`react`、`react-query`、`zustand`、`tailwindcss`、`framer-motion`。
- 后端依赖：`fastapi`、`pydantic`、`uvicorn`、`httpx`、`sqlalchemy`、`asyncpg`、`pgvector`、`redis`、`tenacity`。
- 爬虫依赖：`playwright`、`scrapy`、`selectolax`。
- AI 依赖：`openai`（或 `azure-ai-inference`/`anthropic`）、`sentence-transformers`/`nomic`。
- Prompt 与 API 契约参考本文档。
- 申请 BestBuy/PA-API Key，准备代理池与合规说明模板。
- 使用 Jira/Linear 拆解里程碑为 Story 与验收条件。

## 推荐的模型与供应商组合

- **主力**：Azure OpenAI - GPT-4（企业合规与稳定）。
- **备选**：OpenAI 直连（降级/扩容）、AWS Bedrock 上 Claude 3（适配全 AWS 方案）。
- **Embedding**：OpenAI `text-embedding-3-large` 搭配 pgvector，规模扩大后可改用自托管方案。

## 环境变量说明

可根据实际需求调整模型供应商、版本号或运行环境变量，以匹配最适合的开发体验。
