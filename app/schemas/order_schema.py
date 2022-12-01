from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    quantity: int
    is_active: bool
    date_created: datetime
    date_modified: datetime

    class config:
        orm_mode = True
