import type { ChatPlanResponse } from '../types/chat'

interface PlanPreviewProps {
  plan: ChatPlanResponse | null
}

export function PlanPreview({ plan }: PlanPreviewProps) {
  if (!plan) {
    return (
      <div className="panel">
        <div className="panel-header">
          <h2>方案卡片</h2>
          <span className="panel-subtitle">生成的配置方案将展示在这里</span>
        </div>
        <div className="empty-state">
          <p>填写需求并发送后，Builda 会生成一套主机配置方案与备选方案。</p>
        </div>
      </div>
    )
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>主方案</h2>
        <span className="panel-subtitle">
          总价约 {plan.total_price.toLocaleString()} {plan.currency}
        </span>
      </div>
      <div className="plan-summary">
        <p>{plan.summary}</p>
        {plan.notes && <p className="plan-notes">{plan.notes}</p>}
      </div>
      <div className="plan-components">
        {plan.components.map((component) => (
          <div key={`${component.category}-${component.name}`} className="plan-component">
            <div>
              <span className="plan-component-category">{component.category}</span>
              <p className="plan-component-name">{component.name}</p>
            </div>
            <div className="plan-component-meta">
              <span>{component.vendor}</span>
              <strong>
                {component.price.toLocaleString()} {plan.currency}
              </strong>
            </div>
          </div>
        ))}
      </div>
      {plan.alternatives.length > 0 && (
        <div className="plan-alternatives">
          <h3>备选方案</h3>
          {plan.alternatives.map((alternative) => (
            <div key={alternative.title} className="plan-alternative">
              <div className="plan-alternative-header">
                <div>
                  <h4>{alternative.title}</h4>
                  <p>{alternative.description}</p>
                </div>
                <span>
                  总价 {alternative.total_price.toLocaleString()} {plan.currency}
                </span>
              </div>
              <ul>
                {alternative.components.map((component) => (
                  <li key={`${alternative.title}-${component.category}-${component.name}`}>
                    <span>{component.category}</span>
                    <p>{component.name}</p>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
