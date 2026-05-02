from sqlalchemy import text
from src.infrastructure.database.session import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DB OK:", result.scalar())
except Exception as e:
    print("❌ DB ERROR:", e)