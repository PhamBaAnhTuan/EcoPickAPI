# vercel_app.py

# Thay 'EcoPickAPI' bằng tên thư mục chứa file settings.py và asgi.py của bạn
from app.asgi import application

app = application
