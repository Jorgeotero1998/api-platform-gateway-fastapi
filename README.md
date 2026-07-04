# OteroAPI Platform

**EN**: API Keys + Rate Limiting + Usage Logs  
**ES**: API Keys + Rate limiting + logs de uso

## Live demo / Demo online
- **Web**: https://api-platform-gateway-fastapi.vercel.app
- **API docs**: https://api-platform-gateway-fastapi-api.onrender.com/docs
- **API health**: https://api-platform-gateway-fastapi-api.onrender.com/api/v1/health

## Stack
- FastAPI
- PostgreSQL
- Key Value
- Rate Limit

## Local setup (Docker)

`ash
cp .env.example .env
docker compose up --build
`

## Credentials (demo)

**EN**: Default demo admin is seeded from ADMIN_EMAIL / ADMIN_PASSWORD.  
**ES**: El admin demo se crea desde ADMIN_EMAIL / ADMIN_PASSWORD.

## Deploy

**EN**:
- Backend: Render (Blueprint via ender.yaml)
- Frontend: Vercel (Root Directory: web)

**ES**:
- Backend: Render (Blueprint con ender.yaml)
- Frontend: Vercel (Root Directory: web)
