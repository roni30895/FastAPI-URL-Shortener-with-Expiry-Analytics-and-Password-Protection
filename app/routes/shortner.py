import traceback
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.models import url_request
from app.utils import generate_shorten_url, hash_password, get_current_time, get_expiry_time
from app.database import connection, cursor

router = APIRouter()

@router.post("/shorten")
async def shorten_url(req: url_request):
    try:
        # Convert HttpUrl to string
        original_url = str(req.original_url)

        short_url = generate_shorten_url(original_url)
        creation_time = get_current_time()
        exp_timestamp = get_expiry_time(req.exp_hour)
        password_hash = hash_password(req.password)

        # Check if the URL already exists
        cursor.execute("SELECT short_url FROM urls WHERE original_url=?", (original_url,))
        existing_url = cursor.fetchone()

        if existing_url:
            return {"short_url": f"https://short.ly/{existing_url[0]}", "message": "This URL already exists"}

        # Insert into the database
        cursor.execute(
            "INSERT INTO urls(original_url, short_url, creation_timestamp, expiration_timestamp, password_hash) VALUES (?, ?, ?, ?, ?)",
            (original_url, short_url, creation_time, exp_timestamp, password_hash)
        )
        connection.commit()

        return {"short_url": f"https://short.ly/{short_url}"}

    except Exception as e:
        traceback.print_exc()  # Print error to the server logs for debugging
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )