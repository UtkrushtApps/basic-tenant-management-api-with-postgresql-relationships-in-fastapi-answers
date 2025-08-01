from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.db import get_db, Base, engine
from app import crud, schemas

import asyncio

app = FastAPI()

# Dependency for db session

def get_db_dependency():
    return get_db()

@app.on_event("startup")
async def startup():
    # Create DB schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Tenant Endpoints ---

@app.post("/tenants/", response_model=schemas.TenantRead, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant_in: schemas.TenantCreate, db=Depends(get_db)):
    try:
        return await crud.create_tenant(db, tenant_in)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Tenant with that name already exists")

@app.get("/tenants/", response_model=List[schemas.TenantRead])
async def list_tenants(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return await crud.get_tenants(db, skip=skip, limit=limit)

@app.get("/tenants/{tenant_id}", response_model=schemas.TenantRead)
async def get_tenant(tenant_id: int, db=Depends(get_db)):
    tenant = await crud.get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@app.put("/tenants/{tenant_id}", response_model=schemas.TenantRead)
async def update_tenant(tenant_id: int, tenant_in: schemas.TenantUpdate, db=Depends(get_db)):
    tenant = await crud.update_tenant(db, tenant_id, tenant_in)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@app.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(tenant_id: int, db=Depends(get_db)):
    success = await crud.delete_tenant(db, tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return

# --- User Endpoints ---

@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: schemas.UserCreate, db=Depends(get_db)):
    # Ensure tenant exists
    tenant = await crud.get_tenant(db, user_in.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    try:
        user = await crud.create_user(db, user_in)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with that email already exists")

@app.get("/users/", response_model=List[schemas.UserRead])
async def list_users(tenant_id: Optional[int] = None, skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return await crud.get_users(db, tenant_id=tenant_id, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int, db=Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserRead)
async def update_user(user_id: int, user_in: schemas.UserUpdate, db=Depends(get_db)):
    user = await crud.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db=Depends(get_db)):
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return
