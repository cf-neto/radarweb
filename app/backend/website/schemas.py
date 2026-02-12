from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl

class WebsiteResponse(BaseModel):
    id: int
    name: str
    url: HttpUrl
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

class WebsiteStatusResponse(BaseModel):
    page_title: Optional[str] = None
    status: str
    http_status: Optional[int] = None
    response_time_seconds: float
    favicon: Optional[str] = None
    url: HttpUrl

class WebsiteUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None

    class Config:
        from_attributes = True