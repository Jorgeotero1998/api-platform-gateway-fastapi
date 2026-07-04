# API Platform (Keys, Quotas, Rate Limits) — ES/EN

## Español

Mini “API platform” estilo gateway:

- Crear API keys (admin)
- Validación por header `X-API-Key`
- Rate limit con Redis (fixed-window) + logs de uso

### Endpoints
- `/api/v1/platform/api-keys` (POST/GET, admin)
- `/api/v1/platform/echo` (GET, requiere `X-API-Key`)

---

## English

API platform gateway with API keys, Redis-backed rate limiting, and usage logs.

