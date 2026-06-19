# Hệ Thống Phân Thư Tự Động

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
___________________________________________________________________________________________________________________________________________________________________

Để triển khai hệ thống **Phân Thư Tự Động** này trên một PC mới tinh, bạn cần cài đặt và cấu hình theo các bước chi tiết sau:

### 1. Cài đặt các phần mềm nền tảng (Yêu cầu hệ thống)
Trên PC mới, bạn cần tải và cài đặt 3 công cụ cốt lõi sau:

*   **Python:** Tải và cài đặt [Python](https://www.python.org/downloads/) (khuyến nghị phiên bản 3.10 trở lên). Khi cài đặt, hãy nhớ tích vào ô **"Add Python.exe to PATH"**.
*   **Node.js:** Tải và cài đặt [Node.js](https://nodejs.org/en/) (khuyến nghị phiên bản LTS). Để chạy máy chủ WhatsApp.
*   **Ollama:** Tải và cài đặt [Ollama](https://ollama.com/) dành cho Windows. Công cụ này dùng để chạy mô hình AI cục bộ trên máy bạn.

### 2. Thiết lập Trí tuệ Nhân tạo (Ollama AI)
Sau khi cài đặt xong Ollama, bạn cần tải mô hình AI `phi3:mini` (mô hình ngôn ngữ mà mã nguồn đang sử dụng).
*   Mở **Command Prompt (cmd)** hoặc PowerShell.
*   Chạy lệnh sau và chờ hệ thống tải mô hình về (dung lượng khoảng 2.3GB):
*   
    ollama run phi3:mini
    
    *(Sau khi tải xong nó sẽ hiện ra dấu nhắc lệnh để chat, bạn có thể gõ `/bye` để thoát).*

### 3. Cài đặt thư viện phụ thuộc (Dependencies)
Tiếp theo, bạn cần cài đặt các thư viện mã nguồn mở cho cả Python và Node.js.
Mở Terminal / Command Prompt và di chuyển vào thư mục dự án (ví dụ: `cd D:\demo_phanthu`).

**A. Đối với Python:**
Chạy lần lượt các lệnh sau:

# Cài đặt các thư viện cần thiết
pip install flask requests colorlog openpyxl python-docx playwright

# Cài đặt trình duyệt tự động cho Playwright (dùng để cào dữ liệu web tự động)
playwright install

**B. Đối với Node.js (WhatsApp Web):**
Di chuyển vào thư mục `whatsapp_server` và cài đặt các package:

cd whatsapp_server
npm install


### 4. Cấu hình hệ thống (Setup)
Mở file `config.py` ở thư mục gốc (D:\demo_phanthu) và kiểm tra/điều chỉnh các thông số quan trọng:
*   `WHATSAPP_PHONE`: Điền số điện thoại (có cài WhatsApp) của Lãnh đạo hoặc người phê duyệt để bot gửi thông báo đến. Format bắt đầu bằng `+84...` (Ví dụ: `+84912345678`).
*   Các thông số khác như `WEB_USERNAME`, `WEB_PASSWORD` (nếu dùng thật trên trang `dhtn.dcs.vn`) hoặc các luật lệ tự động (`RULES`) có thể được tùy chỉnh tại đây.

### 5. Khởi chạy hệ thống
Sau khi đã cài đặt xong tất cả, bạn chỉ cần quay lại thư mục gốc của dự án (`D:\demo_phanthu`) và chạy file `start.bat`. File này sẽ tự động:
1.  Khởi động máy chủ web giả lập (Mock Web).
2.  Kiểm tra xem Ollama đã chạy chưa.
3.  Khởi động máy chủ WhatsApp Node.js.
4.  Khởi động ứng dụng lõi Flask.

**Lưu ý trong lần chạy đầu tiên:**
*   Khi cửa sổ **WhatsApp Server** hiện lên, nó sẽ sinh ra một **Mã QR**. Bạn cần mở ứng dụng WhatsApp trên điện thoại (đã đăng nhập số điện thoại dùng làm con Bot), vào phần "Thiết bị liên kết" (Linked Devices) và **quét mã QR này** để đăng nhập Bot.
*   Giao diện quản lý chính sẽ tự động mở trên trình duyệt của bạn tại địa chỉ: `http://localhost:5000`

Từ các lần sau, bạn chỉ cần mở máy, chạy `start.bat` là hệ thống sẽ sẵn sàng làm việc!
