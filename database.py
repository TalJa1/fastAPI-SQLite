import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the SQLite database path
sqlite_db_path = os.getenv("SQLITE_DB_PATH", "/tmp/touch.db")
if not sqlite_db_path.startswith("/tmp"):
    logger.warning(
        "SQLite database must be in the /tmp directory for Vercel compatibility."
    )
sqlite_db_url = f"sqlite+aiosqlite:///{sqlite_db_path}"

# Load the database URL from environment variables, defaulting to the SQLite setup
DATABASE_URL = os.getenv("DATABASE_URL", sqlite_db_url)

# Create the database engine
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()


# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


# Create the database file in /tmp if using SQLite
if DATABASE_URL.startswith("sqlite") and not os.path.exists(sqlite_db_path):
    with open(sqlite_db_path, "w") as f:
        logger.info(f"SQLite database created at {sqlite_db_path}")
