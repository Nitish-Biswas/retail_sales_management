from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from datetime import datetime
from src.models.schemas import FilterParams, PaginatedResponse
from src.services.data_service import DataService

router = APIRouter()
data_service = None

def init_routes(service: DataService):
    """Initialize routes with data service"""
    global data_service
    data_service = service

@router.get("/transactions", response_model=PaginatedResponse)
async def get_transactions(
    search: Optional[str] = Query(None),
    customer_region: Optional[List[str]] = Query(None),
    gender: Optional[List[str]] = Query(None),
    age_min: Optional[int] = Query(None),
    age_max: Optional[int] = Query(None),
    product_category: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    payment_method: Optional[List[str]] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    sort_by: str = Query("date"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get transactions with filters, search, sorting, and pagination"""
    try:
        date_from_parsed = datetime.fromisoformat(date_from) if date_from else None
        date_to_parsed = datetime.fromisoformat(date_to) if date_to else None
        
        filters = FilterParams(
            search=search,
            customer_region=customer_region,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            product_category=product_category,
            tags=tags,
            payment_method=payment_method,
            date_from=date_from_parsed,
            date_to=date_to_parsed,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
        
        result = data_service.get_paginated_data(filters)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter-options")
async def get_filter_options():
    """Get available filter options"""
    try:
        return data_service.get_filter_options()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))