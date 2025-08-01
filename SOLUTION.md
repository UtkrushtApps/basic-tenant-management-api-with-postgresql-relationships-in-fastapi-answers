# Solution Steps

1. Define your async PostgreSQL database connection with SQLAlchemy in app/db.py. Set up the Base, engine, and get_db dependency.

2. Design normalized SQLAlchemy models for tenants and users in app/models.py. Ensure each user links to exactly one tenant via foreign key, define the subscription tier as an ENUM, and enforce cascading deletes from tenants to users.

3. Create Pydantic schemas in app/schemas.py for validation and serialization of Tenant and User requests and responses, including models for create, read, and update operations. Mirror the ENUM in the Pydantic layer.

4. Implement async CRUD operations for tenants and users in app/crud.py, using async SQLAlchemy sessions, with proper error handling for unique constraint violations and cascading deletes.

5. Build FastAPI endpoints in app/main.py for create/list/retrieve/update/delete (CRUD) for both tenants and users. Use dependency injection for the async DB session, respond with appropriate FastAPI status codes, and handle errors such as not found or already exists.

6. On application startup, ensure the database schema is created by running Base.metadata.create_all via the engine in FastAPI's startup event.

7. For all user endpoints, enforce tenant scoping: when creating a user, check the tenant exists; when listing users, allow filtering by tenant_id.

8. Test that deleting a tenant deletes all associated users (referential integrity with cascade delete on foreign key).

9. Test all endpoints using API tools or automated tests to ensure correct behavior and data integrity between models.

