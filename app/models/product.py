```python
"""Product models for the Adidas shoe store"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Text, JSON, DateTime, func
from datetime import datetime
from typing import List, Optional
from app.core.database import Base

class Category(Base):
    """Product category model"""
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    products: Mapped[List["Product"]] = relationship(back_populates="category_obj")

class Product(Base):
    """Product model for shoes"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    brand: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    sizes: Mapped[List[str]] = mapped_column(JSON)  # Store as JSON array
    colors: Mapped[List[str]] = mapped_column(JSON)  # Store as JSON array
    stock: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Foreign key relationship (optional, for normalized categories)
    category_obj: Mapped[Optional[Category]] = relationship(back_populates="products")
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

class CartItem(Base):
    """Shopping cart item model"""
    __tablename__ = "cart_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    size: Mapped[str] = mapped_column(String(10))
    color: Mapped[str] = mapped_column(String(50))
    session_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    def __repr__(self) -> str:
        return f"<CartItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"

class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    total: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    items: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of order items
    customer_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, total={self.total}, status='{self.status}')>"
```