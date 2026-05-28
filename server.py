import sqlite3
import random
import string
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel

app = FastAPI()

# Cấu hình thư mục chứa giao diện HTML
templates = Jinja2Templates(directory="templates")

# Khởi tạo cơ sở dữ liệu SQLite
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Bảng lưu trữ sản phẩm của Chợ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketplace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bảng lưu trữ danh sách Chủ sở hữu của từng Server ID
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_rooms (
            server_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            is_started INTEGER DEFAULT 0
        )
    """)
    
    # Bảng lưu lịch sử tin nhắn chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

# Khai báo cấu trúc dữ liệu nhận từ Form Đăng bán sản phẩm
class ProductCreate(BaseModel):
    title: str
    description: str
    price: float

# Bộ quản lý kết nối WebSocket theo từng Server ID riêng biệt
class RoomManager:
    def __init__(self):
        # Cấu trúc: { server_id: [danh_sách_các_websocket_đang_connect] }
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, server_id: str):
        await websocket.accept()
        if server_id not in self.rooms:
            self.rooms[server_id] = []
        self.rooms[server_id].append(websocket)

    def disconnect(self, websocket: WebSocket, server_id: str):
        if server_id in self.rooms:
            self.rooms[server_id].remove(websocket)
            if not self.rooms[server_id]:
                del self.rooms[server_id]

    async def broadcast(self, server_id: str, message: str):
        if server_id in self.rooms:
            for connection in self.rooms[server_id]:
                await connection.send_text(message)

manager = RoomManager()

# ==========================================
# CÁC ĐƯỜNG DẪN ĐIỀU HƯỚNG (ROUTES)
# ==========================================

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/marketplace")
async def get_marketplace(request: Request):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM marketplace ORDER BY date_posted DESC")
    products = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("marketplace.html", {"request": request, "products": products})

@app.post("/api/marketplace")
async def add_product(product: ProductCreate):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO marketplace (title, description, price) VALUES (?, ?, ?)",
        (product.title, product.description, product.price)
    )
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success"})

@app.get("/chat")
async def get_chat(request: Request, server_id: str = Query(...), role: str = Query("player"), username: str = Query("User")):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM server_rooms WHERE server_id = ?", (server_id,))
    room = cursor.fetchone()
    
    # Nếu là người bấm nút Tạo Server và Server ID này chưa có ai thầu
    if role == "owner" and not room:
        cursor.execute("INSERT INTO server_rooms (server_id, owner_name) VALUES (?, ?)", (server_id, username))
        conn.commit()
        is_owner = True
        is_started = 0
    else:
        # Nếu vào sau hoặc phòng đã tồn tại
        if room:
            is_owner = (room[1] == username or role == "owner")
            is_started = room[2]
        else:
            # Trường hợp tự gõ bừa ID ngoài Menu thì tạm coi như tạo phòng mới luôn
            cursor.execute("INSERT INTO server_rooms (server_id, owner_name) VALUES (?, ?)", (server_id, username))
            conn.commit()
            is_owner = True
            is_started = 0
            
    conn.close()
    
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "server_id": server_id, 
        "is_owner": is_owner,
        "is_started": is_started,
        "username": username
    })

# ==========================================
# CỔNG ĐƯỜNG TRUYỀN REAL-TIME (WEBSOCKET)
# ==========================================

@app.websocket("/ws/chat/{server_id}")
async def websocket_endpoint(websocket: WebSocket, server_id: str):
    await manager.connect(websocket, server_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Xử lý lệnh Bắt đầu trận đấu/mở phòng từ Chủ Server gửi lên
            if data == "__START_ROOM__":
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE server_rooms SET is_started = 1 WHERE server_id = ?", (server_id,))
                conn.commit()
                conn.close()
                # Phát tín hiệu bắt đầu cho toàn bộ thành viên trong phòng biết
                await manager.broadcast(server_id, "__ROOM_HAS_STARTED__")
            else:
                # Phát tin nhắn chat bình thường cho mọi người cùng phòng
                await manager.broadcast(server_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, server_id)
