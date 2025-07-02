```python
"""Product service for managing shoe inventory"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.core.database import get_db_session
from app.models.product import Product, Category
from app.core.logging import get_logger

logger = get_logger(__name__)

class ProductService:
    """Service for managing products"""
    
    def __init__(self):
        pass
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        try:
            with get_db_session() as db:
                stmt = select(Product).order_by(Product.name)
                result = db.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            return []
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        try:
            with get_db_session() as db:
                return db.get(Product, product_id)
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return None
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        try:
            with get_db_session() as db:
                stmt = select(Product).where(Product.category == category).order_by(Product.name)
                result = db.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting products by category {category}: {e}")
            return []
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name, brand, or description"""
        try:
            with get_db_session() as db:
                search_term = f"%{query.lower()}%"
                stmt = select(Product).where(
                    or_(
                        Product.name.ilike(search_term),
                        Product.brand.ilike(search_term),
                        Product.description.ilike(search_term),
                        Product.category.ilike(search_term)
                    )
                ).order_by(Product.name)
                result = db.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error searching products with query '{query}': {e}")
            return []
    
    def create_product(self, **kwargs) -> Optional[Product]:
        """Create a new product"""
        try:
            with get_db_session() as db:
                product = Product(**kwargs)
                db.add(product)
                db.commit()
                db.refresh(product)
                logger.info(f"Created product: {product.name}")
                return product
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            return None
    
    def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        """Update a product"""
        try:
            with get_db_session() as db:
                product = db.get(Product, product_id)
                if not product:
                    return None
                
                for key, value in kwargs.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                
                db.commit()
                db.refresh(product)
                logger.info(f"Updated product: {product.name}")
                return product
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            return None
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        try:
            with get_db_session() as db:
                product = db.get(Product, product_id)
                if not product:
                    return False
                
                db.delete(product)
                db.commit()
                logger.info(f"Deleted product: {product.name}")
                return True
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            return False
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Update product stock"""
        try:
            with get_db_session() as db:
                product = db.get(Product, product_id)
                if not product:
                    return False
                
                product.stock = max(0, product.stock + quantity)
                db.commit()
                logger.info(f"Updated stock for {product.name}: {product.stock}")
                return True
        except Exception as e:
            logger.error(f"Error updating stock for product {product_id}: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            with get_db_session() as db:
                stmt = select(Product.category).distinct().order_by(Product.category)
                result = db.execute(stmt)
                return [row[0] for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def get_featured_products(self, limit: int = 8) -> List[Product]:
        """Get featured products (for homepage)"""
        try:
            with get_db_session() as db:
                stmt = select(Product).order_by(Product.created_at.desc()).limit(limit)
                result = db.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting featured products: {e}")
            return []
```