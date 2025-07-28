import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.services.tayara import Tayara
from app.models.search_parms import SearchParams

router = APIRouter(prefix="/tayara", tags=["Tayara"])

@router.post("/description")
def get_descriptions(params: SearchParams):
    scraper = Tayara(query=params.query, category=params.category, page=params.page)
    descriptions = scraper.get_description(max_page=1)
    return {"descriptions": descriptions}

@router.post("/search")
def search_ads(params: SearchParams):
    scraper = Tayara(query=params.query, category=params.category, page=params.page)
    results = scraper.search(page=params.page)
    return {"results": results}

@router.post("/export",response_class=FileResponse)
def export_details(detail:SearchParams):
    scraper = Tayara(query=detail.query, category=detail.category,page=detail.page)
    result = scraper.get_description(max_page=10)
    file = Tayara.export_to_excel(result) 
    return FileResponse(
        path=file,
        filename=os.path.basename(file),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
