from fastapi import APIRouter, Query, HTTPException, FastAPI
from typing import Optional, List
from contextlib import asynccontextmanager
from src.services.data_service import data_service

@asynccontextmanager
async def transaction_lifespan(app: FastAPI):
    #STARTUP LOGIC 
    try:
        print("Server starting up: Refreshing transaction filters...")
        data_service.refresh_filters()
    except Exception as e:
        print(f"WARNING: Failed to load initial filters: {e}")
    
    yield  
    
    # SHUTDOWN LOGIC 
    print("Server shutting down: Releasing resources...")
    data_service.shutdown()

router = APIRouter(lifespan=transaction_lifespan)

@router.get("/transactions")
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
    try:
        return data_service.get_filtered_transactions(
            search=search,
            customer_region=customer_region,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            product_category=product_category,
            tags=tags,
            payment_method=payment_method,
            date_from=date_from,
            date_to=date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter-options")
async def get_filter_options():
    try:
        return data_service.get_filter_options()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
