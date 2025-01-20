from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.params import Body  # Import Body
from app.utils import is_expired, get_current_time, verify_password
from app.database import connection, cursor

router = APIRouter()

@router.get("/{short_url}")
async def redirect_url(
    short_url: str,
    req: Request,
    password: str = Body(..., embed=True)  # Accept password in the request body
):
    cursor.execute("SELECT original_url, expiration_timestamp, password_hash FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")

    original_url, expiration_timestamp, password_hash = result

    if is_expired(expiration_timestamp):
        raise HTTPException(status_code=410, detail="Short URL has expired.")

    if not verify_password(stored_hash=password_hash, password=password):
        raise HTTPException(status_code=403, detail="Invalid Password")

    cursor.execute(
        "INSERT INTO analytics(short_url, access_timestamp, ip_address) VALUES (?, ?, ?)",
        (short_url, get_current_time(), req.client.host)
    )
    connection.commit()

    return {"redirect_to": original_url}
