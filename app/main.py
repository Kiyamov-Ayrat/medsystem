import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health_db")
async def health_db(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
