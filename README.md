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

🚀 HƯỚNG DẪN KHỞI ĐỘNG GAME SERVER (DÀNH CHO CHỦ PHÒNG)
Để tự chạy một máy chủ Local và trải nghiệm game, cậu thực hiện theo các bước sau:

1. Cài đặt môi trường mạng
Mở Terminal / Command Prompt tại thư mục chứa game và cài đặt các thư viện hỗ trợ truyền tải dữ liệu:

Bash


pip install fastapi uvicorn
2. Kích hoạt Game Server
Chạy lệnh sau để bật máy chủ ở chế độ tự động cập nhật dữ liệu (Auto-Reload):

Bash


uvicorn server:app --reload
3. Vào Game
Mở trình duyệt web bất kỳ và truy cập vào sảnh đón tiếp theo đường dẫn:

Plaintext


[http://127.0.0.1:8000](http://127.0.0.1:8000)
🕹️ LUỒNG CHƠI CHÍNH CỦA GAME (GAMEPLAY FLOW)
Menu Chính (home.html): Người chơi tiến hành đặt tên nhân vật (In-game Name). Tại đây có 2 lựa chọn: Ghé thăm Chợ Đen để xem đồ hoặc tiến vào Hệ thống Máy chủ để chuẩn bị chiến đấu.

Cơ chế Tạo & Tham gia Phòng (Lobby Matchmaking):

Tạo Server Mới (Host): Hệ thống tự động cấp một mã ID Server ngẫu nhiên (Ví dụ: UT-A8F2). Người tạo sẽ giữ quyền Chủ Phòng, sở hữu nút KÍCH HOẠT TRẬN ĐẤU (START).

Tham Gia Server (Player): Người chơi khác nhập chính xác mã ID Server của Chủ phòng để dịch chuyển vào chung sảnh chờ. Màn hình của họ sẽ ở trạng thái đóng băng kèm dòng chữ "Đang đợi Chủ Server bắt đầu...".

Kích Hoạt Trận Đấu (chat.html): Ngay khi Chủ Phòng bấm nút START, hệ thống WebSocket sẽ lập tức bắn tín hiệu real-time đến tất cả người chơi trong phòng. Giao diện sảnh chờ sẽ tự động mở khóa, kích hoạt kênh Chat thế giới thời gian thực để mọi người bắt đầu phối hợp chiến thuật.

Hệ Thống Chợ Đen (marketplace.html): Nơi các game thủ treo bán các vật phẩm hiếm của mình hoặc mua thêm trang bị từ người chơi khác bằng cách mở Pop-up đăng bán, dữ liệu sẽ được lưu thẳng vào database của Server.

🔥 Dự án được thiết kế và phát triển bởi một lập trình viên đam mê Robotics và Game Mechanics!
