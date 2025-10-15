# Builda – React + FastAPI full-stack project

A modern full-stack web application that pairs a Next.js 14 frontend with a FastAPI backend. Builda demonstrates an AI-assisted PC configuration flow powered by Gemini planning, curated sample data, and a polished glassmorphism UI.

## 🚀 Tech stack

### Frontend
- **React 18** – component-driven UI library
- **Next.js 14** – hybrid rendering framework
- **TypeScript** – static typing for JavaScript
- **CSS Modules** – scoped styling with glassmorphic flair

### Backend
- **Python 3.11+** – application runtime
- **FastAPI** – blazing-fast ASGI framework
- **Uvicorn** – production-ready ASGI server
- **Pydantic** – declarative settings and schema validation

## 📁 Project structure

```
Builda/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── pages/           # Page-level React components
│   │   └── styles/          # Global and modular stylesheets
│   ├── package.json         # Frontend dependencies
│   ├── tsconfig.json        # TypeScript configuration
│   ├── next.config.js       # Next.js configuration
│   └── Dockerfile           # Frontend container definition
├── backend/                  # FastAPI backend
│   ├── app/                # API, schemas, and services
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container definition
├── docker-compose.yml       # Multi-service orchestration
├── scripts/                 # Convenience scripts for local dev
└── README.md                # Project documentation
```

## 🛠️ Getting started

### Option 1: local development

#### Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend runs at http://localhost:3000.

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
The backend runs at http://localhost:8000.

### Option 2: Docker

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d --build
```

Access points:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## 📚 API surface

### Core endpoints
- `GET /` – root health message
- `GET /hello` – hello world endpoint
- `GET /health` – health check probe

### User management sample
- `GET /users` – list users
- `POST /users` – create a user
- `GET /users/{user_id}` – fetch user by ID
- `DELETE /users/{user_id}` – delete user by ID

### Gemini planning flow
- `POST /chat/plan` – request a Gemini-powered PC configuration with sample fallback
- `POST /builds/validate` – run compatibility validation on a submitted build
- `GET /products/search` – search vector-indexed sample products
- `GET /price/history/{sku}` – inspect mock price history data

## 🔧 Development notes

### Frontend
- Written in TypeScript with strict typing
- Hot-module replacement for a fast feedback loop
- Proxy-ready for calling the FastAPI backend during dev

### Backend
- Automatic OpenAPI docs via FastAPI
- CORS enabled for the Next.js frontend
- Centralized settings management using Pydantic BaseSettings

### Environment variables
Copy `backend/env.example` to `backend/.env` and provide the required values (e.g., Gemini API key).

## 📝 Development commands

### Frontend
```bash
npm run dev      # Start the dev server
npm run build    # Compile a production build
npm run start    # Serve the production build
npm run lint     # Run ESLint checks
```

### Backend
```bash
python main.py                    # Launch the FastAPI app
uvicorn main:app --reload         # Development server with reloads
uvicorn main:app --host 0.0.0.0   # Production-style server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License – see [LICENSE](LICENSE) for details.

## 🆘 Support

If you hit any issues or have questions, please open an issue or contact the maintainers.
