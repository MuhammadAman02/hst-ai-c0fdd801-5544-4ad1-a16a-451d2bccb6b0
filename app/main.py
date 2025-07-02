```python
"""Adidas Shoe Store - Main UI Application"""

from nicegui import ui, app
from typing import List, Optional, Dict, Any
import asyncio
from pathlib import Path

from app.core.logging import app_logger, get_logger
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.models.product import Product, Category
from app.core.database import create_tables

# Initialize logger
logger = get_logger(__name__)

# Global services
product_service = ProductService()
cart_service = CartService()

# Adidas brand colors
ADIDAS_COLORS = {
    'primary': '#000000',      # Black
    'secondary': '#FFFFFF',    # White  
    'accent': '#FF6B35',       # Orange
    'background': '#F5F5F5',   # Light gray
    'text': '#333333',         # Dark gray
    'success': '#4CAF50',      # Green
    'warning': '#FF9800',      # Orange
    'error': '#F44336'         # Red
}

class AdidasStore:
    """Main Adidas Store application class"""
    
    def __init__(self):
        self.current_category: Optional[str] = None
        self.search_query: str = ""
        self.selected_product: Optional[Product] = None
        self.cart_items_container = None
        self.products_container = None
        self.cart_badge = None
        
        # Initialize database and sample data
        create_tables()
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize sample Adidas shoe data"""
        try:
            # Check if products already exist
            existing_products = product_service.get_all_products()
            if existing_products:
                logger.info(f"Found {len(existing_products)} existing products")
                return
            
            # Sample Adidas shoes data
            sample_shoes = [
                {
                    "name": "Ultraboost 22",
                    "brand": "Adidas",
                    "price": 180.00,
                    "description": "Our most responsive running shoe, featuring BOOST midsole technology for incredible energy return.",
                    "category": "Running",
                    "sizes": ["7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12"],
                    "colors": ["Core Black", "Cloud White", "Solar Red"],
                    "stock": 50,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/fbaf991a78bc4896a3e9ad7800abcec6_9366/Ultraboost_22_Shoes_Black_GZ0127_01_standard.jpg"
                },
                {
                    "name": "Stan Smith",
                    "brand": "Adidas", 
                    "price": 80.00,
                    "description": "The iconic tennis shoe that started it all. Clean, classic, and timeless design.",
                    "category": "Lifestyle",
                    "sizes": ["6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "12"],
                    "colors": ["Cloud White/Green", "Cloud White/Navy", "All White"],
                    "stock": 75,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/Stan_Smith_Shoes_White_FX5500_01_standard.jpg"
                },
                {
                    "name": "Superstar",
                    "brand": "Adidas",
                    "price": 85.00, 
                    "description": "The shell-toe legend. Born on the basketball court, adopted by hip hop and skate culture.",
                    "category": "Lifestyle",
                    "sizes": ["6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "12"],
                    "colors": ["Cloud White/Core Black", "Core Black/Cloud White", "All White"],
                    "stock": 60,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/12365dbc7c424288a893ad7d00f7d2b4_9366/Superstar_Shoes_White_EG4958_01_standard.jpg"
                },
                {
                    "name": "NMD_R1",
                    "brand": "Adidas",
                    "price": 130.00,
                    "description": "Street-ready style meets innovative technology. BOOST midsole for all-day comfort.",
                    "category": "Lifestyle", 
                    "sizes": ["7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12"],
                    "colors": ["Core Black", "Cloud White", "Solar Red", "Collegiate Navy"],
                    "stock": 40,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/NMD_R1_Shoes_Black_FV1734_01_standard.jpg"
                },
                {
                    "name": "Gazelle",
                    "brand": "Adidas",
                    "price": 90.00,
                    "description": "Retro suede sneaker with vintage appeal. A timeless classic from the archives.",
                    "category": "Lifestyle",
                    "sizes": ["6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "12"],
                    "colors": ["Collegiate Navy", "Core Black", "Maroon", "Green"],
                    "stock": 55,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/Gazelle_Shoes_Blue_BB5478_01_standard.jpg"
                },
                {
                    "name": "Samba OG",
                    "brand": "Adidas",
                    "price": 90.00,
                    "description": "The original indoor soccer shoe. Leather upper with suede T-toe overlay.",
                    "category": "Lifestyle",
                    "sizes": ["6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "12"],
                    "colors": ["Core Black/Cloud White", "Cloud White/Core Black", "Collegiate Green"],
                    "stock": 45,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/Samba_OG_Shoes_Black_B75807_01_standard.jpg"
                },
                {
                    "name": "Adizero Boston 11",
                    "brand": "Adidas",
                    "price": 140.00,
                    "description": "Lightweight running shoe designed for speed. LIGHTSTRIKE midsole for responsive cushioning.",
                    "category": "Running",
                    "sizes": ["7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12"],
                    "colors": ["Core Black/Solar Red", "Cloud White/Core Black", "Solar Yellow"],
                    "stock": 35,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/Adizero_Boston_11_Shoes_Black_GY7657_01_standard.jpg"
                },
                {
                    "name": "Forum Low",
                    "brand": "Adidas",
                    "price": 90.00,
                    "description": "Basketball heritage meets street style. High-quality leather upper with ankle strap.",
                    "category": "Basketball",
                    "sizes": ["7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12"],
                    "colors": ["Cloud White/Core Black", "Core Black/Cloud White", "All White"],
                    "stock": 40,
                    "image_url": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/a615b3c9c7b54dc5b6e8ad5200169b1e_9366/Forum_Low_Shoes_White_FY7757_01_standard.jpg"
                }
            ]
            
            # Create products
            for shoe_data in sample_shoes:
                product_service.create_product(**shoe_data)
            
            logger.info(f"Created {len(sample_shoes)} sample products")
            
        except Exception as e:
            logger.error(f"Error initializing sample data: {e}")
    
    def create_header(self):
        """Create the main header with navigation"""
        with ui.header().classes('bg-black text-white shadow-lg'):
            with ui.row().classes('w-full items-center justify-between px-4 py-2'):
                # Logo and brand
                with ui.row().classes('items-center gap-4'):
                    ui.image('https://logoeps.com/wp-content/uploads/2013/03/adidas-vector-logo.png').classes('h-8 w-8')
                    ui.label('ADIDAS STORE').classes('text-xl font-bold')
                
                # Search bar
                with ui.row().classes('flex-1 max-w-md mx-8'):
                    search_input = ui.input(placeholder='Search shoes...').classes('flex-1')
                    search_input.on('keydown.enter', lambda: self.search_products(search_input.value))
                    ui.button(icon='search', on_click=lambda: self.search_products(search_input.value)).classes('bg-orange-500 hover:bg-orange-600')
                
                # Cart button
                with ui.row().classes('items-center gap-2'):
                    cart_button = ui.button(icon='shopping_cart', on_click=self.toggle_cart).classes('bg-orange-500 hover:bg-orange-600 relative')
                    self.cart_badge = ui.badge(str(cart_service.get_item_count())).classes('absolute -top-2 -right-2 bg-red-500 text-white text-xs')
    
    def create_category_nav(self):
        """Create category navigation"""
        categories = ["All", "Running", "Lifestyle", "Basketball", "Training"]
        
        with ui.row().classes('w-full bg-gray-100 px-4 py-3 justify-center gap-4'):
            for category in categories:
                category_value = None if category == "All" else category
                button_classes = 'px-4 py-2 rounded-lg font-medium transition-colors'
                if self.current_category == category_value:
                    button_classes += ' bg-black text-white'
                else:
                    button_classes += ' bg-white text-black hover:bg-gray-200'
                
                ui.button(
                    category, 
                    on_click=lambda cat=category_value: self.filter_by_category(cat)
                ).classes(button_classes)
    
    def create_product_card(self, product: Product):
        """Create a product card"""
        with ui.card().classes('w-72 h-96 cursor-pointer hover:shadow-xl transition-shadow'):
            # Product image
            with ui.card_section().classes('p-0 h-48 overflow-hidden'):
                ui.image(product.image_url or 'https://via.placeholder.com/300x200?text=No+Image').classes('w-full h-full object-cover')
            
            # Product info
            with ui.card_section().classes('p-4 flex-1 flex flex-col justify-between'):
                ui.label(product.name).classes('text-lg font-bold text-gray-800 mb-1')
                ui.label(product.category).classes('text-sm text-gray-500 mb-2')
                ui.label(f'${product.price:.2f}').classes('text-xl font-bold text-black mb-3')
                
                # Add to cart button
                ui.button(
                    'View Details', 
                    on_click=lambda p=product: self.show_product_details(p)
                ).classes('w-full bg-black text-white hover:bg-gray-800')
    
    def show_product_details(self, product: Product):
        """Show product details in a dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
            with ui.row().classes('w-full gap-8'):
                # Product image
                with ui.column().classes('w-1/2'):
                    ui.image(product.image_url or 'https://via.placeholder.com/400x300?text=No+Image').classes('w-full rounded-lg')
                
                # Product details
                with ui.column().classes('w-1/2 gap-4'):
                    ui.label(product.name).classes('text-3xl font-bold')
                    ui.label(f'${product.price:.2f}').classes('text-2xl font-bold text-black')
                    ui.label(product.description).classes('text-gray-600 leading-relaxed')
                    
                    # Size selection
                    ui.label('Size:').classes('font-semibold mt-4')
                    size_select = ui.select(
                        options=product.sizes,
                        value=product.sizes[0] if product.sizes else None
                    ).classes('w-full')
                    
                    # Color selection
                    ui.label('Color:').classes('font-semibold mt-4')
                    color_select = ui.select(
                        options=product.colors,
                        value=product.colors[0] if product.colors else None
                    ).classes('w-full')
                    
                    # Quantity
                    ui.label('Quantity:').classes('font-semibold mt-4')
                    quantity_input = ui.number(value=1, min=1, max=10).classes('w-24')
                    
                    # Stock info
                    ui.label(f'In Stock: {product.stock}').classes('text-green-600 font-medium')
                    
                    # Add to cart button
                    with ui.row().classes('gap-4 mt-6'):
                        ui.button(
                            'Add to Cart',
                            on_click=lambda: self.add_to_cart(
                                product, 
                                size_select.value, 
                                color_select.value, 
                                int(quantity_input.value or 1),
                                dialog
                            )
                        ).classes('bg-black text-white px-8 py-3 text-lg hover:bg-gray-800')
                        
                        ui.button('Close', on_click=dialog.close).classes('bg-gray-300 text-black px-8 py-3 text-lg hover:bg-gray-400')
        
        dialog.open()
    
    def add_to_cart(self, product: Product, size: str, color: str, quantity: int, dialog):
        """Add product to cart"""
        try:
            cart_service.add_item(product.id, quantity, size, color)
            self.update_cart_badge()
            ui.notify(f'Added {product.name} to cart!', type='positive')
            dialog.close()
        except Exception as e:
            ui.notify(f'Error adding to cart: {str(e)}', type='negative')
            logger.error(f"Error adding to cart: {e}")
    
    def update_cart_badge(self):
        """Update cart badge count"""
        if self.cart_badge:
            count = cart_service.get_item_count()
            self.cart_badge.text = str(count)
            self.cart_badge.visible = count > 0
    
    def toggle_cart(self):
        """Toggle cart sidebar"""
        self.show_cart()
    
    def show_cart(self):
        """Show cart in a dialog"""
        cart_items = cart_service.get_cart_items()
        
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
            ui.label('Shopping Cart').classes('text-2xl font-bold mb-4')
            
            if not cart_items:
                ui.label('Your cart is empty').classes('text-gray-500 text-center py-8')
            else:
                # Cart items
                with ui.column().classes('w-full gap-4 max-h-96 overflow-y-auto'):
                    for item in cart_items:
                        product = product_service.get_product(item.product_id)
                        if product:
                            with ui.row().classes('w-full items-center gap-4 p-4 border rounded-lg'):
                                ui.image(product.image_url or 'https://via.placeholder.com/80x60').classes('w-20 h-15 object-cover rounded')
                                
                                with ui.column().classes('flex-1'):
                                    ui.label(product.name).classes('font-semibold')
                                    ui.label(f'Size: {item.size}, Color: {item.color}').classes('text-sm text-gray-500')
                                    ui.label(f'${product.price:.2f} x {item.quantity}').classes('font-medium')
                                
                                ui.button(
                                    icon='delete',
                                    on_click=lambda item_id=item.id: self.remove_from_cart(item_id, dialog)
                                ).classes('bg-red-500 text-white hover:bg-red-600')
                
                # Cart total
                total = cart_service.get_cart_total()
                ui.separator()
                with ui.row().classes('w-full justify-between items-center py-4'):
                    ui.label('Total:').classes('text-xl font-bold')
                    ui.label(f'${total:.2f}').classes('text-xl font-bold')
                
                # Checkout button
                ui.button(
                    'Proceed to Checkout',
                    on_click=lambda: self.checkout(dialog)
                ).classes('w-full bg-black text-white py-3 text-lg hover:bg-gray-800')
            
            ui.button('Close', on_click=dialog.close).classes('w-full bg-gray-300 text-black py-2 mt-4 hover:bg-gray-400')
        
        dialog.open()
    
    def remove_from_cart(self, item_id: int, dialog):
        """Remove item from cart"""
        try:
            cart_service.remove_item(item_id)
            self.update_cart_badge()
            ui.notify('Item removed from cart', type='positive')
            dialog.close()
            # Reopen cart to show updated items
            self.show_cart()
        except Exception as e:
            ui.notify(f'Error removing item: {str(e)}', type='negative')
            logger.error(f"Error removing from cart: {e}")
    
    def checkout(self, dialog):
        """Handle checkout process"""
        try:
            total = cart_service.get_cart_total()
            cart_service.clear_cart()
            self.update_cart_badge()
            dialog.close()
            
            # Show success message
            with ui.dialog() as success_dialog, ui.card().classes('w-full max-w-md text-center'):
                ui.icon('check_circle', size='4rem').classes('text-green-500 mx-auto mb-4')
                ui.label('Order Successful!').classes('text-2xl font-bold mb-2')
                ui.label(f'Total: ${total:.2f}').classes('text-lg mb-4')
                ui.label('Thank you for your purchase!').classes('text-gray-600 mb-4')
                ui.button('Continue Shopping', on_click=success_dialog.close).classes('bg-black text-white px-6 py-2')
            
            success_dialog.open()
            
        except Exception as e:
            ui.notify(f'Checkout error: {str(e)}', type='negative')
            logger.error(f"Checkout error: {e}")
    
    def filter_by_category(self, category: Optional[str]):
        """Filter products by category"""
        self.current_category = category
        self.load_products()
    
    def search_products(self, query: str):
        """Search products"""
        self.search_query = query
        self.load_products()
    
    def load_products(self):
        """Load and display products"""
        try:
            # Get filtered products
            if self.search_query:
                products = product_service.search_products(self.search_query)
            elif self.current_category:
                products = product_service.get_products_by_category(self.current_category)
            else:
                products = product_service.get_all_products()
            
            # Clear and rebuild products container
            if self.products_container:
                self.products_container.clear()
                
                with self.products_container:
                    if not products:
                        ui.label('No products found').classes('text-gray-500 text-center py-8 text-xl')
                    else:
                        with ui.row().classes('w-full gap-6 flex-wrap justify-center'):
                            for product in products:
                                self.create_product_card(product)
        
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            ui.notify('Error loading products', type='negative')

# Global store instance
store = AdidasStore()

@ui.page('/')
def index():
    """Main store page"""
    ui.add_head_html('''
        <style>
            .nicegui-content { padding: 0 !important; }
            body { margin: 0; background-color: #f5f5f5; }
        </style>
    ''')
    
    # Header
    store.create_header()
    
    # Category navigation
    store.create_category_nav()
    
    # Main content
    with ui.column().classes('w-full min-h-screen bg-gray-50'):
        # Hero section
        with ui.row().classes('w-full bg-gradient-to-r from-black to-gray-800 text-white py-16 px-8 justify-center'):
            with ui.column().classes('text-center max-w-4xl'):
                ui.label('IMPOSSIBLE IS NOTHING').classes('text-5xl font-bold mb-4')
                ui.label('Discover the latest Adidas footwear collection').classes('text-xl mb-8')
                ui.button('Shop Now', on_click=lambda: ui.run_javascript('window.scrollTo(0, 400)')).classes('bg-orange-500 text-white px-8 py-3 text-lg hover:bg-orange-600')
        
        # Products section
        with ui.column().classes('w-full px-8 py-8'):
            ui.label('Featured Products').classes('text-3xl font-bold text-center mb-8')
            
            # Products container
            store.products_container = ui.row().classes('w-full gap-6 flex-wrap justify-center')
            
            # Load initial products
            store.load_products()

if __name__ in {"__main__", "__mp_main__"}:
    # This will be called by main.py, so we don't need to run here
    pass
```