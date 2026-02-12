from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.backend.website.schemas import WebsiteCreate, WebsiteResponse, WebsiteUpdate
from app.backend.website.services import (
    check_site_status_by_url,
    check_site_status_by_id,
    create_website_service,
    view_website_service,
    update_website_service,
    delete_website_service
    )
from app.backend.core.database import get_db

website_router = APIRouter(
    prefix="/websites",
    tags=["Websites"]
)

# -----------------------------
# Pega o status do website
# -----------------------------
@website_router.get(
    "/check-status",
    summary="Checks website status by URL",
    description="Check if a website is online by URL",
    tags=["Website Status"]
)
async def check_website_by_url(url: str):
    return await check_site_status_by_url(url)

# -----------------------------
# Pega o status do website pelo ID
# -----------------------------
@website_router.get(
    "/{website_id}/check-status",
    summary="Checks website status by ID",
    description="Check if a website is online by ID",
    tags=["Website Status"]
)
async def check_website_by_id(website_id: int, db: Session = Depends(get_db)):
    return await check_site_status_by_id(website_id, db)

# -----------------------------
# Salva o website no banco de dados
# -----------------------------
@website_router.post(
    "/",
    summary="Create website",
    description="Create and store a new website in the database.",
    response_model=WebsiteResponse,
    status_code=201
)
async def save_website(
    payload: WebsiteCreate,
    db: Session = Depends(get_db)
):
    website = create_website_service(
        db=db,
        name=payload.name,
        url=str(payload.url)
    )
    return website

# -----------------------------
# Visualiza todos os websites salvo no banco de dados
# -----------------------------
@website_router.get(
    "/",
    summary="List website",
    description="List all websites stored in database.",
    response_model=List[WebsiteResponse]
)
async def view_all_websites(db: Session = Depends(get_db)):
    return view_website_service(db)

# -----------------------------
# Atualiza dados do website com patch
# -----------------------------
@website_router.patch(
    "/{website_id}",
    summary="Update website",
    description="Update website in database.",
)
async def update_website(
    website_id: int,
    payload: WebsiteUpdate,
    db: Session = Depends(get_db)
):
    return update_website_service(
        db = db,
        website_id = website_id,
        name = payload.name,
        url = str(payload.url)
    )

# -----------------------------
# Deleta website do banco de dados
# -----------------------------
@website_router.delete(
    "/{website_id}",
    summary="Delete website",
    description="Delete website in database.",
    
)
async def delete_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    return delete_website_service(db, website_id)
