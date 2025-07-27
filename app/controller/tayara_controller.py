from fastapi import APIRouter
from app.services.tayara import Tayara
from app.models.search_parms import SearchParams

router = APIRouter(prefix="/tayara", tags=["Tayara"])

@router.post("/description")
def get_descriptions(params: SearchParams):
    scraper = Tayara(query=params.query, category=params.category,page=params.page)
    descriptions = scraper.get_description(max_page=5)
    return {"descriptions": descriptions}

@router.post("/search")
def search_ads(params: SearchParams):
    scraper = Tayara(query=params.query, category=params.category, page=params.page)
    results = scraper.search(page=params.page)
    return {"results": results}
