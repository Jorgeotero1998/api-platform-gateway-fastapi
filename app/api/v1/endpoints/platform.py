from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.api.v1.deps import get_current_user, get_db, require_roles
from app.core.ratelimit import enforce_rate_limit
from app.db.models.gateway import ApiKey, UsageLog, generate_api_key, hash_api_key

router = APIRouter()


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyOut(BaseModel):
    id: str
    name: str
    is_active: bool


class ApiKeyCreated(BaseModel):
    id: str
    name: str
    api_key: str


async def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db=Depends(get_db),
):
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-API-Key")
    key_hash = hash_api_key(x_api_key)

    result = await db.execute(select(ApiKey).where(ApiKey.key_hash == key_hash))
    api_key = result.scalar_one_or_none()
    if not api_key or not api_key.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    await enforce_rate_limit(key=key_hash, limit=60, window_seconds=60)

    db.add(UsageLog(api_key_hash=key_hash, method="*", path="*"))
    await db.commit()
    return api_key


@router.post("/platform/api-keys", response_model=ApiKeyCreated)
async def create_api_key_endpoint(
    payload: ApiKeyCreate,
    db=Depends(get_db),
    _=Depends(require_roles("admin")),
):
    plain = generate_api_key()
    row = ApiKey(name=payload.name, key_hash=hash_api_key(plain), is_active=True)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return ApiKeyCreated(id=str(row.id), name=row.name, api_key=plain)


@router.get("/platform/api-keys", response_model=list[ApiKeyOut])
async def list_api_keys(db=Depends(get_db), _=Depends(require_roles("admin"))):
    result = await db.execute(select(ApiKey).order_by(ApiKey.created_at.desc()))
    rows = result.scalars().all()
    return [ApiKeyOut(id=str(k.id), name=k.name, is_active=k.is_active) for k in rows]


@router.get("/platform/echo")
async def echo(message: str = "hello", _=Depends(require_api_key)):
    return {"message": message}

