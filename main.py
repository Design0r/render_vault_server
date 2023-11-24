from fastapi import FastAPI
from contextlib import asynccontextmanager
import databases
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, create_engine, Column, Integer, String, Text


DATABASE_URL = "sqlite:///db/rv.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

models = Table(
    "models",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("path", Text),
)
materials = Table(
    "materials",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("path", Text),
)

hdris = Table(
    "hdris",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("path", Text),
)

lightsets= Table(
    "lightsets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("path", Text),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


class Asset(BaseModel):
    name: str
    path: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


@app.post("/models/create")
async def create_model(pool: Asset):
    query = models.insert().values(name=pool.name, path=pool.path)
    await database.execute(query)
    print(f"INFO:     Model pool: {pool.name} created successfully")
    return {"message": f"Model pool {pool.name} created successfully"}


@app.post("/models/delete")
async def delete_models(pool: Asset):
    query = models.delete().where(models.c.name == pool.name)
    await database.execute(query)
    print(f"INFO:     Model pool: {pool.name} deleted successfully")
    return {"message": f"Model pool {pool.name} deleted successfully"}


@app.post("/materials/create")
async def create_materials(pool: Asset):
    query = materials.insert().values(name=pool.name, path=pool.path)
    await database.execute(query)
    print(f"INFO:     Material pool: {pool.name} created successfully")
    return {"message": f"Material pool: {pool.name} created successfully"}


@app.post("/materials/delete")
async def delete_materials(pool: Asset):
    query = materials.delete().where(materials.c.name == pool.name)
    await database.execute(query)
    print(f"INFO:     Material pool: {pool.name} deleted successfully")
    return {"message": f"Material pool {pool.name} deleted successfully"}


@app.post("/hdris/create")
async def create_hdris(pool: Asset):
    query = hdris.insert().values(name=pool.name, path=pool.path)
    await database.execute(query)
    print(f"INFO:     HDRI pool: {pool.name} created successfully")
    return {"message": f"Hdri pool: {pool.name} created successfully"}


@app.post("/hdris/delete")
async def delete_hdris(pool: Asset):
    query = hdris.delete().where(hdris.c.name == pool.name)
    await database.execute(query)
    print(f"INFO:     HDRI pool: {pool.name} deleted successfully")
    return {"message": f"Hdri pool: {pool.name} deleted successfully"}


@app.post("/lightsets/create")
async def create_lightsets(pool: Asset):
    query = lightsets.insert().values(name=pool.name, path=pool.path)
    await database.execute(query)
    print(f"INFO:     Lightset pool: {pool.name} created successfully")
    return {"message": f"Lightset pool: {pool.name} created successfully"}


@app.post("/lightsets/delete")
async def delete_lightsets(pool: Asset):
    query = lightsets.delete().where(models.c.name == pool.name)
    await database.execute(query)
    print(f"INFO:     Lightset pool: {pool.name} deleted successfully")
    return {"message": f"Lightset pool {pool.name} deleted successfully"}

@app.get("/all_pools")
async def read_all_pools():
    all_models = await database.fetch_all(models.select())
    all_materials = await database.fetch_all(materials.select())
    all_hdris = await database.fetch_all(hdris.select())
    all_lightsets = await database.fetch_all(lightsets.select())
    return {"materials": all_materials, "models": all_models, "hdris": all_hdris, "lightsets": all_lightsets}
