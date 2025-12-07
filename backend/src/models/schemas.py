from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TransactionSchema(BaseModel):
    transaction_id: str
    date: datetime
    customer_id: str
    customer_name: str
    phone_number: str
    gender: str
    age: int
    customer_region: str
    customer_type: str
    product_id: str
    product_name: str
    brand: str
    product_category: str
    tags: str
    quantity: int
    price_per_unit: float
    discount_percentage: float
    total_amount: float
    final_amount: float
    payment_method: str
    order_status: str
    delivery_type: str
    store_id: str
    store_location: str
    salesperson_id: str
    employee_name: str

class FilterParams(BaseModel):
    search: Optional[str] = None
    customer_region: Optional[List[str]] = None
    gender: Optional[List[str]] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    product_category: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    payment_method: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sort_by: Optional[str] = "date"
    sort_order: Optional[str] = "desc"
    page: int = 1
    page_size: int = 10

class PaginatedResponse(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    page_size: int
    data: List[TransactionSchema]
    has_next: bool
    has_prev: bool