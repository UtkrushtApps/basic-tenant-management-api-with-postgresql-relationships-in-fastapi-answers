from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import update as sql_update, delete as sql_delete
from app import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession

# --- TENANT CRUD ---

async def create_tenant(db: AsyncSession, tenant_in: schemas.TenantCreate) -> models.Tenant:
    tenant = models.Tenant(name=tenant_in.name)
    db.add(tenant)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(tenant)
    return tenant

async def get_tenant(db: AsyncSession, tenant_id: int) -> models.Tenant:
    result = await db.execute(select(models.Tenant).where(models.Tenant.id == tenant_id))
    return result.scalar_one_or_none()

async def get_tenants(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Tenant).offset(skip).limit(limit))
    return result.scalars().all()

async def update_tenant(db: AsyncSession, tenant_id: int, tenant_in: schemas.TenantUpdate) -> models.Tenant:
    result = await db.execute(select(models.Tenant).where(models.Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        return None
    data = tenant_in.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(tenant, k, v)
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant

async def delete_tenant(db: AsyncSession, tenant_id: int) -> bool:
    result = await db.execute(select(models.Tenant).where(models.Tenant.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        return False
    await db.delete(tenant)
    await db.commit()
    return True

# --- USER CRUD ---

async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        tenant_id=user_in.tenant_id,
        subscription_tier=user_in.subscription_tier
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: int) -> models.User:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, tenant_id: int = None, skip: int = 0, limit: int = 100):
    q = select(models.User)
    if tenant_id is not None:
        q = q.where(models.User.tenant_id == tenant_id)
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_in: schemas.UserUpdate) -> models.User:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    data = user_in.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(user, k, v)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
