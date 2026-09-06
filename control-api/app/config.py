import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mlplatform:mlplatform@localhost:5433/mlplatform",
)