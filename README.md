# Hệ Thống Phân Thư Tự Động
## Đảng Ủy Phường Tây Nam

### 1. Giới thiệu & Các công cụ sử dụng
Hệ thống giúp tự động tiếp nhận, phân loại và chuyển tiếp các văn bản/thư đến một cách thông minh, tiết kiệm thời gian cho người quản lý.

**Các công cụ & Công nghệ sử dụng:**
- **Python (Flask):** Xây dựng máy chủ xử lý logic cốt lõi và cung cấp giao diện quản lý (Dashboard).
- **Ollama AI (phi3:mini):** Trí tuệ nhân tạo có khả năng đọc hiểu tiếng Việt, giúp tự động phân tích ngữ cảnh văn bản để xếp loại (Kinh tế, Văn hóa, Xã hội).
- **Node.js (WhatsApp Web JS):** Tạo Chatbot kết nối với WhatsApp, cho phép lãnh đạo duyệt thư từ xa qua điện thoại.
- **Python-docx & Openpyxl:** Trích xuất dữ liệu từ file Word (`.docx`) và tự động ghi chép thông tin vào Sổ đăng ký Excel (`.xlsx`).
- **Playwright:** Công cụ điều khiển trình duyệt tự động (RPA) để thao tác thay thế con người trên các trang web nội bộ.

### 2. Nguyên lý hoạt động
1. **Đầu vào (Input):** Hệ thống thu thập các văn bản chờ xử lý (hiện tại là đọc file từ thư mục `inbox`).
2. **Xử lý (Process):**
   - Đọc bóc tách nội dung (Số ký hiệu, Trích yếu).
   - Đưa qua bộ lọc 2 tầng: Tầng 1 (tìm từ khóa cứng) và Tầng 2 (Nhờ AI đọc hiểu văn cảnh) để đề xuất người phụ trách (Chủ trì, Phối hợp).
   - Tự động ghi thông tin thư vào "Sổ đăng ký" Excel để lưu vết.
3. **Phê duyệt (Approve):** Hệ thống tổng hợp thành một tin nhắn tóm tắt và gửi vào WhatsApp của Lãnh đạo. Lãnh đạo chỉ cần nhắn tin trả lời lại bằng các mã lệnh ngắn (Ví dụ: `OK 1`).
4. **Đầu ra (Output):** Khi có lệnh phê duyệt từ Lãnh đạo, hệ thống sẽ chốt thông tin và kết thúc quy trình. Các thư đã duyệt sẽ được chuyển tiếp qua thư mục khác.

---

### 3. Cách hoạt động khi ÁP DỤNG THẬT (Môi trường thực tế)
Khi hệ thống được liên kết hoàn toàn vào trang quản lý văn bản nội bộ của cơ quan (ví dụ: `dhtn.dcs.vn`), quy trình sẽ "tự động hóa 100%":
- Thay vì bạn phải tải file thả vào thư mục `inbox`, con Bot sẽ **tự động đăng nhập** vào trang web cơ quan để quét lấy danh sách các "Thư chờ xử lý".
- Sau khi bạn bấm duyệt `OK 1` trên điện thoại, con Bot sẽ tự động **mở một trình duyệt web ngầm**, truy cập vào đúng bức thư đó trên hệ thống web cơ quan, **tự động đánh dấu tick** vào tên cán bộ Chủ trì/Phối hợp mà AI đã đề xuất, **tự động gõ lời phê** (Ví dụ: "Đảng bộ CQD") và bấm nút **"Chuyển xử lý"**.
- Toàn bộ thao tác click chuột/gõ phím rườm rà trên máy tính được thay thế hoàn toàn bằng 1 tin nhắn 3 ký tự trên điện thoại của Lãnh đạo.

---

### 4. Cài đặt ban đầu
Mở file `config.py` (tại `D:\demo_phanthu`) và điền số điện thoại nhận thông báo vào biến:
`WHATSAPP_PHONE = "+84xxxxxxxxx"`

### 5. Cách sử dụng (Chế độ đọc File)
1. **Khởi động:** Chạy file `start.bat`.
2. **Nạp thư:** Copy các file văn bản (`.txt` hoặc `.docx`) thả vào thư mục `D:\demo_phanthu\data\inbox`.
3. **Quét thư:** Mở web `http://localhost:5000` và bấm nút **"KIỂM TRA THƯ MỚI"**.
4. **Duyệt:** Kiểm tra tin nhắn WhatsApp và trả lời (reply) để chốt. Lịch sử duyệt sẽ được cập nhật trên web.

### 6. Các lệnh duyệt nhanh trên WhatsApp
Chỉ cần nhắn lại tin nhắn của bot với các lệnh sau:
- `OK 1` -> `OK 5`: Duyệt thư kèm ý kiến chỉ đạo mẫu (Xem/sửa mẫu trong `config.py`).
- `SỬA CT [tên]`: Đổi người Chủ trì (Ví dụ: `SỬA CT Nguyễn Văn A`).
- `SỬA PH [tên]`: Thêm người Phối hợp (Ví dụ: `SỬA PH Trần Văn B`).
- `BỎ`: Hủy/bỏ qua thư này.

### 7. Lưu ý
- Các thư đã đọc sẽ tự động bị dời sang thư mục `data/processed`.
- Nếu AI phân loại sai thường xuyên, bạn có thể dạy AI thêm từ khóa ở biến `RULES` trong `config.py`.
- Nếu file Excel `so_dang_ky.xlsx` đang được mở bằng phần mềm khác, hệ thống sẽ không ghi được dữ liệu. Hãy tắt file đó đi trước khi "Kiểm tra thư".
