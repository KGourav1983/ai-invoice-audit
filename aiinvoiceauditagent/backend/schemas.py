from pydantic import BaseModel
from typing import List

class LineItem(BaseModel):
    description: str
    qty: int
    unit_price: float

class POMatchRequest(BaseModel):
    supplier: str
    line_items: List[LineItem]
