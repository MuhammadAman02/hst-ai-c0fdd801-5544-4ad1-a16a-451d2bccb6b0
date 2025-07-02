```markdown
# Adidas Shoe Store 🏃‍♂️👟

A modern, responsive e-commerce web application for browsing and purchasing Adidas footwear. Built with NiceGUI for an exceptional user experience and SQLAlchemy for robust data management.

## ✨ Features

- **Product Catalog**: Browse the complete Adidas shoe collection
- **Category Filtering**: Filter by Running, Lifestyle, Basketball, and Training
- **Search Functionality**: Find shoes by name, brand, or description
- **Product Details**: View detailed information, sizes, colors, and stock
- **Shopping Cart**: Add items, manage quantities, and proceed to checkout
- **Responsive Design**: Optimized for desktop and mobile devices
- **Real-time Updates**: Dynamic cart updates and stock management

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd adidas-shoe-store
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8080`

## 🏗️ Project Structure

```
adidas-shoe-store/
├── app/
│   ├── main.py                 # Main NiceGUI application
│   ├── models/
│   │   └── product.py          # Database models
│   ├── services/
│   │   ├── product_service.py  # Product business logic
│   │   └── cart_service.py     # Shopping cart logic
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   ├── database.py        # Database configuration
│   │   └── logging.py         # Logging setup
│   └── api/
│       └── router.py          # API endpoints
├── data/                      # Database files
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🛠️ Technology Stack

- **Frontend**: NiceGUI (Python-based web UI framework)
- **Backend**: FastAPI (High-performance web framework)
- **Database**: SQLAlchemy with SQLite (easily upgradeable to PostgreSQL)
- **Validation**: Pydantic V2 (Data validation and settings)
- **Styling**: Tailwind CSS (via NiceGUI)

## 📱 Features Overview

### Product Catalog
- Browse 8+ premium Adidas shoe models
- High-quality product images
- Detailed descriptions and specifications
- Price and stock information

### Shopping Experience
- Intuitive product browsing
- Advanced filtering and search
- Size and color selection
- Real-time cart updates
- Streamlined checkout process

### Responsive Design
- Mobile-first approach
- Optimized for all screen sizes
- Touch-friendly interface
- Fast loading times

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Adidas Shoe Store |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8080 |
| `DATABASE_URL` | Database connection string | sqlite:///./data/adidas_store.db |
| `SECRET_KEY` | Security key for sessions | (change in production) |
| `DEBUG` | Enable debug mode | False |

### Database Configuration

The application uses SQLite by default for easy setup. For production, you can switch to PostgreSQL:

```bash
# PostgreSQL example
DATABASE_URL=postgresql://user:password@localhost/adidas_store
```

## 🧪 Development

### Running in Development Mode

```bash
# Enable debug mode
export DEBUG=True

# Run with auto-reload
python main.py
```

### Database Management

```python
# Create tables
from app.core.database import create_tables
create_tables()

# Reset database
from app.core.database import drop_tables, create_tables
drop_tables()
create_tables()
```

## 📦 Sample Data

The application comes with pre-loaded sample data including:

- **Ultraboost 22** - Premium running shoes
- **Stan Smith** - Classic tennis shoes
- **Superstar** - Iconic basketball shoes
- **NMD_R1** - Street-style sneakers
- **Gazelle** - Retro suede sneakers
- **Samba OG** - Original indoor soccer shoes
- **Adizero Boston 11** - Lightweight running shoes
- **Forum Low** - Basketball heritage shoes

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-secure-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs in the console
2. Verify your Python version (3.9+)
3. Ensure all dependencies are installed
4. Check the `.env` configuration

For additional support, please open an issue in the repository.

## 🎯 Roadmap

- [ ] User authentication and accounts
- [ ] Order history and tracking
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Payment integration
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Advanced analytics

---

**Built with ❤️ using NiceGUI and FastAPI**
```