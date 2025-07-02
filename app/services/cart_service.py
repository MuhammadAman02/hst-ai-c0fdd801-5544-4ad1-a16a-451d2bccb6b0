```python
"""Shopping cart service"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.core.database import get_db_session
from app.models.product import CartItem, Product
from app.services.product_service import ProductService
from app.core.logging import get_logger
import uuid

logger = get_logger(__name__)

class CartService:
    """Service for managing shopping cart"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())  # Simple session management
        self.product_service = ProductService()
    
    def add_item(self, product_id: int, quantity: int = 1, size: str = "", color: str = "") -> bool:
        """Add item to cart"""
        try:
            # Check if product exists and has stock
            product = self.product_service.get_product(product_id)
            if not product:
                raise ValueError("Product not found")
            
            if product.stock < quantity:
                raise ValueError("Insufficient stock")
            
            with get_db_session() as db:
                # Check if item already exists in cart
                stmt = select(CartItem).where(
                    CartItem.product_id == product_id,
                    CartItem.session_id == self.session_id,
                    CartItem.size == size,
                    CartItem.color == color
                )
                existing_item = db.execute(stmt).scalar_one_or_none()
                
                if existing_item:
                    # Update quantity
                    existing_item.quantity += quantity
                    logger.info(f"Updated cart item quantity: {existing_item.quantity}")
                else:
                    # Create new cart item
                    cart_item = CartItem(
                        product_id=product_id,
                        quantity=quantity,
                        size=size,
                        color=color,
                        session_id=self.session_id
                    )
                    db.add(cart_item)
                    logger.info(f"Added new item to cart: product_id={product_id}")
                
                db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding item to cart: {e}")
            raise e
    
    def remove_item(self, item_id: int) -> bool:
        """Remove item from cart"""
        try:
            with get_db_session() as db:
                cart_item = db.get(CartItem, item_id)
                if cart_item and cart_item.session_id == self.session_id:
                    db.delete(cart_item)
                    db.commit()
                    logger.info(f"Removed item from cart: {item_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error removing item from cart: {e}")
            return False
    
    def update_quantity(self, item_id: int, quantity: int) -> bool:
        """Update item quantity in cart"""
        try:
            with get_db_session() as db:
                cart_item = db.get(CartItem, item_id)
                if cart_item and cart_item.session_id == self.session_id:
                    if quantity <= 0:
                        db.delete(cart_item)
                    else:
                        cart_item.quantity = quantity
                    db.commit()
                    logger.info(f"Updated cart item quantity: {quantity}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error updating cart item quantity: {e}")
            return False
    
    def get_cart_items(self) -> List[CartItem]:
        """Get all items in cart"""
        try:
            with get_db_session() as db:
                stmt = select(CartItem).where(CartItem.session_id == self.session_id)
                result = db.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting cart items: {e}")
            return []
    
    def get_item_count(self) -> int:
        """Get total number of items in cart"""
        try:
            cart_items = self.get_cart_items()
            return sum(item.quantity for item in cart_items)
        except Exception as e:
            logger.error(f"Error getting cart item count: {e}")
            return 0
    
    def get_cart_total(self) -> float:
        """Get total price of items in cart"""
        try:
            cart_items = self.get_cart_items()
            total = 0.0
            
            for item in cart_items:
                product = self.product_service.get_product(item.product_id)
                if product:
                    total += product.price * item.quantity
            
            return total
        except Exception as e:
            logger.error(f"Error calculating cart total: {e}")
            return 0.0
    
    def clear_cart(self) -> bool:
        """Clear all items from cart"""
        try:
            with get_db_session() as db:
                stmt = delete(CartItem).where(CartItem.session_id == self.session_id)
                db.execute(stmt)
                db.commit()
                logger.info("Cleared cart")
                return True
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
            return False
    
    def get_cart_summary(self) -> Dict[str, Any]:
        """Get cart summary with items and totals"""
        try:
            cart_items = self.get_cart_items()
            items_with_products = []
            
            for item in cart_items:
                product = self.product_service.get_product(item.product_id)
                if product:
                    items_with_products.append({
                        'item': item,
                        'product': product,
                        'subtotal': product.price * item.quantity
                    })
            
            total = sum(item['subtotal'] for item in items_with_products)
            
            return {
                'items': items_with_products,
                'total': total,
                'item_count': len(cart_items),
                'total_quantity': sum(item.quantity for item in cart_items)
            }
        except Exception as e:
            logger.error(f"Error getting cart summary: {e}")
            return {
                'items': [],
                'total': 0.0,
                'item_count': 0,
                'total_quantity': 0
            }
```