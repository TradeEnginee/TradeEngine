# models/order.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class ShippingAddress:
    full_name: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    phone: str

@dataclass
class OrderItem:
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    
    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Order:
    id: Optional[int] = None
    user_id: int = 0
    items: List[OrderItem] = field(default_factory=list)
    shipping_address: Optional[ShippingAddress] = None
    payment_method: str = ""
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    transaction_id: Optional[str] = None
    
    @property
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)
    
    @property
    def shipping_cost(self) -> float:
        return 70 if self.subtotal < 300 else 0.0
    
    @property
    def tax(self) -> float:
        return round(self.subtotal * 0.08, 2)  # 8% tax
    
    @property
    def total(self) -> float:
        return round(self.subtotal + self.shipping_cost + self.tax, 2)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal
                } for item in self.items
            ],
            "shipping_address": {
                "full_name": self.shipping_address.full_name,
                "address_line1": self.shipping_address.address_line1,
                "address_line2": self.shipping_address.address_line2,
                "city": self.shipping_address.city,
                "state": self.shipping_address.state,
                "postal_code": self.shipping_address.postal_code,
                "country": self.shipping_address.country,
                "phone": self.shipping_address.phone
            } if self.shipping_address else None,
            "payment_method": self.payment_method,
            "status": self.status.value,
            "subtotal": self.subtotal,
            "shipping_cost": self.shipping_cost,
            "tax": self.tax,
            "total": self.total,
            "transaction_id": self.transaction_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
