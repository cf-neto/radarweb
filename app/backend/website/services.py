import time
import httpx
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.backend.website.models import SavedWebsite
from app.backend.website.schemas import WebsiteStatusResponse

# -----------------------------
# Visualizar o status do website
# -----------------------------
async def check_site_status_by_url(url: str) -> WebsiteStatusResponse:
    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        page_title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else None
        )
        icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
        favicon = urljoin(url, icon_link["href"]) if icon_link else None

        return WebsiteStatusResponse(
            site_name=page_title,
            page_title=page_title,
            status="online" if response.status_code < 400 else "unstable",
            http_status=response.status_code,
            response_time_seconds=round(time.time() - start_time, 2),
            favicon=favicon,
            url=url
        )
    

    except httpx.RequestError as exc:
        return {
            "status": "offline",
            "http_status": None,
            "error": str(exc),
            "response_time_seconds": round(time.time() - start_time, 2),
            "site_name": None,
            "favicon": None,
            "url": url
        }

# -----------------------------
# Visualizar o status do website pelo id
# -----------------------------
async def check_site_status_by_id(website_id: int, db: Session):
    website = db.query(SavedWebsite).filter(SavedWebsite.id == website_id).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(website.url)

        return {
            "status": "online" if response.status_code < 400 else "unstable",
            "http_status": response.status_code,
            "response_time_seconds": round(time.time() - start_time, 2),
            "website_name": website.name,
            "url": website.url
        }

    except httpx.RequestError as exc:
        return {
            "status": "offline",
            "http_status": None,
            "error": str(exc),
            "response_time_seconds": round(time.time() - start_time, 2),
            "website_name": website.name,
            "url": website.url
        }

# -----------------------------
# Criar website
# -----------------------------
def create_website_service(db: Session, name: str, url: str) -> SavedWebsite:
    existing = db.query(SavedWebsite).filter(SavedWebsite.url == url).first()
    existing_name = db.query(SavedWebsite).filter(SavedWebsite.name == name).first()

    if existing or existing_name:
        raise ValueError("Website already exists")
    
    website = SavedWebsite(
        name=name,
        url=url
    )

    db.add(website)
    db.commit()
    db.refresh(website)

    return website

# -----------------------------
# Função Para ver todos websites
# -----------------------------
def view_website_service(db: Session):
    all_websites = db.query(SavedWebsite).all()

    return all_websites

# -----------------------------
# Atualizar Websites
# -----------------------------
def update_website_service(
    db: Session,
    website_id: int,
    name: Optional[str] = None,
    url: Optional[str] = None
) -> SavedWebsite:
    # Procura se existe algum website pelo id
    website = db.query(SavedWebsite).filter(SavedWebsite.id == website_id).first()

    # Se não existir, retorna um erro de não encontrado
    if not website:
        raise ValueError("Website not found")
    
    # Evita url's duplicados
    if url and url != website.url:
        existing = db.query(SavedWebsite).filter(SavedWebsite.url == url).first()

        if existing:
            raise ValueError("URL already exists")
    
    if name is not None:
        website.name = name
    
    if url is not None:
        website.url = url
    
    db.commit()
    db.refresh(website)

    return website

# -----------------------------
# Deleta website pelo id
# -----------------------------
def delete_website_service(db: Session, website_id: int) -> SavedWebsite:
    website = db.query(SavedWebsite).filter(SavedWebsite.id == website_id).first()

    if not website:
        raise ValueError("Website not found")
    
    db.delete(website)
    db.commit()

    return website
