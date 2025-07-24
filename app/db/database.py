from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./dashboard.db"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True  # Allows for logging SQL queries in terminal
)

# Create async session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Data still accessible after commit
)

# Base class that SQLAlchemy models will inherit from
Base = declarative_base()


# Dependency to provide a DB session per request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
