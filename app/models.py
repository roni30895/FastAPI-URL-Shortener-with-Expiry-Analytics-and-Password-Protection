from pydantic import BaseModel, HttpUrl, Field # type: ignore
from typing import Optional

class url_request(BaseModel):
    original_url : HttpUrl
    exp_hour : int = 24
    password: Optional[str] = None

class url_password_request(BaseModel):
    password : str = Field(..., min_length = 5)

class url_analytics_response(BaseModel):
    access_count : int
    logs : list[dict]