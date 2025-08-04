from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config.database import db_settings

engine = create_async_engine(
    db_settings.URL, 
    echo = db_settings.ECHO_LOG
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit = False,
    autocommit = False,
    autoflush= True
    )

Base = declarative_base()

#Dependency for FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session

    