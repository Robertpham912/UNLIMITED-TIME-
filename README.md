# UNLIMITED-TIME-
# 🎮 UNLIMITED TIME - MULTIPLAYER GAME LOBBY SYSTEM

**Unlimited Time** là một tựa game multiplayer trực tuyến đa nền tảng. Dự án này tập trung vào việc xây dựng hệ thống **Sảnh chờ (Lobby System)** và **Phòng kết nối thời gian thực**, cho phép người chơi tự tạo Server riêng, phân quyền Chủ phòng (Host) để điều phối trận đấu, kết hợp với khu vực Chợ Đen (Marketplace) để các game thủ giao dịch vật phẩm trước khi lâm trận.

Giao diện game được tối ưu hóa Responsive bằng Tailwind CSS, giúp trải nghiệm mượt mà trên cả Máy tính, Điện thoại và máy tính bảng (iPad).

---

## 🛠️ CẤU TRÚC THƯ MỤC CỐT LÕI

Game được tối ưu hóa cấu trúc gọn nhẹ, sạch sẽ để dễ dàng quản lý và nâng cấp trên GitHub:
```text
unlimited-time/
├── server.py              # Bộ điều phối Game Server, Quản lý WebSocket & Database
├── database.db            # Cơ sở dữ liệu SQLite lưu trữ thông tin phòng và vật phẩm
└── templates/             # Thư mục chứa giao diện đồ họa của Game
    ├── base.html          # Khung nền móng Responsive tự co giãn theo thiết bị
    ├── home.html          # Menu chính của Game (Đặt tên, Tạo/Tham gia Server)
    ├── marketplace.html   # Chợ Đen giao dịch vật phẩm trước trận đấu
    └── chat.html          # Sảnh chờ (Lobby) và Kênh chat thế giới thời gian thực
