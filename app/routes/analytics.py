from fastapi import APIRouter, HTTPException
from fastapi.params import Body  # Import Body
from app.utils import verify_password
from app.database import cursor

router = APIRouter()

@router.get("/analytics/{short_url}")
async def get_analytics(
    short_url: str,
    password: str = Body(..., embed=True)  # Accept password in the request body
):
    cursor.execute("SELECT password_hash FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    password_hash = result[0]

    if not verify_password(stored_hash=password_hash, password=password):
        raise HTTPException(status_code=403, detail="Invalid Password")

    cursor.execute("SELECT COUNT(*) FROM analytics WHERE short_url=?", (short_url,))
    access_count = cursor.fetchone()[0]

    cursor.execute("SELECT access_timestamp, ip_address FROM analytics WHERE short_url=?", (short_url,))
    logs = [{"access_timestamp": row[0], "ip_address": row[1]} for row in cursor.fetchall()]

    return {
        "access_count": access_count,
        "logs": logs
    }
