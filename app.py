from flask import Flask, render_template, request, jsonify
import time
import requests
from datetime import datetime
import colorlog
import logging
from config import LOG_FILE, CAN_BO, MAU_Y_KIEN, WHATSAPP_PHONE

# Các module xử lý
from scraper import PlaywrightScraper
from ai_classifier import classify_document
from excel_writer import write_to_excel
from file_reader import read_pending_files

app = Flask(__name__)

# Cài đặt logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
))
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = colorlog.getLogger('app')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)

# State toàn cục
pending_docs = {}   
# { doc_id: { doc_info, ai_result, status, timestamp } }
history_today = []  
# Lịch sử xử lý trong ngày
tong_hom_nay = 0

# Hàng đợi gửi tin nhắn WA
wa_pending_queue = []
current_wa_doc_id = None

WA_SERVER_URL = "http://localhost:3000"

def send_next_wa_message():
    global current_wa_doc_id
    
    # Nếu đang có tin nhắn chờ phản hồi thì không gửi thêm
    if current_wa_doc_id is not None:
        return
        
    # Nếu hàng đợi rỗng thì thôi
    if not wa_pending_queue:
        return
        
    # Lấy văn bản tiếp theo
    next_doc_id = wa_pending_queue.pop(0)
    current_wa_doc_id = next_doc_id
    doc_entry = pending_docs.get(next_doc_id)
    
    if not doc_entry:
        current_wa_doc_id = None
        send_next_wa_message() # Thử văn bản kế tiếp
        return
        
    doc = doc_entry['doc_info']
    ai_result = doc_entry['ai_result']
    
    # Xây dựng danh sách reply OK động
    reply_options = ""
    for i, mau in enumerate(MAU_Y_KIEN):
        reply_options += f"👉 OK {i+1}: {mau}\n"
    
    message = (
        f"📄 CÓ THƯ MỚI: {doc['so_ky_hieu']}\n"
        f"🏢 Cơ quan: {doc['co_quan']}\n"
        f"📝 Trích yếu: {doc['trich_yeu']}\n\n"
        f"🤖 AI đề xuất:\n"
        f"- Chủ trì: {ai_result['chu_tri']}\n"
        f"- Phối hợp: {', '.join(ai_result.get('phoi_hop', []))}\n"
        f"- Nhận để biết: {', '.join(ai_result.get('nhan_de_biet', []))}\n"
        f"💡 Lĩnh vực: {ai_result['ten_linh_vuc']} ({ai_result['ly_do']})\n\n"
        f"Vui lòng reply:\n"
        f"{reply_options}"
        f"👉 SỬA CT [tên] để đổi chủ trì\n"
        f"👉 BỎ để bỏ qua"
    )
    
    try:
        wa_res = requests.post(f"{WA_SERVER_URL}/send", json={
            "phone": WHATSAPP_PHONE,
            "message": message,
            "doc_id": next_doc_id
        }, timeout=10)
        wa_data = wa_res.json()
        if not wa_data.get('success'):
            logger.error(f"Lỗi gửi WA cho {next_doc_id}: Full response: {wa_res.text}")
    except Exception as e:
        logger.error(f"Lỗi kết nối WA server: {e}")

@app.route('/')
def index():
    cho_xu_ly = sum(1 for d in pending_docs.values() if d['status'] == 'cho_xu_ly')
    cho_xac_nhan = sum(1 for d in pending_docs.values() if d['status'] == 'cho_xac_nhan')
    da_xu_ly = sum(1 for d in pending_docs.values() if d['status'] == 'da_xu_ly')
    
    return render_template('index.html',
                           tong_hom_nay=tong_hom_nay,
                           cho_xu_ly=cho_xu_ly,
                           da_xu_ly=da_xu_ly,
                           cho_xac_nhan=cho_xac_nhan,
                           pending_docs=list(pending_docs.values()))

@app.route('/check', methods=['POST'])
def check_new():
    global tong_hom_nay
    try:
        # Thay vì dùng scraper, chúng ta đọc file từ thư mục data/inbox
        docs = read_pending_files()
        processed = 0
        errors = []
        
        for doc in docs:
            doc_id = doc['doc_id']
            if doc_id in pending_docs:
                continue
                
            tong_hom_nay += 1
            
            # 1. Phân loại
            ai_result = classify_document(doc)
            
            # 2. Ghi Excel
            # Tạm tính số đến = tong_hom_nay + 1000 để mock
            so_den = 1000 + tong_hom_nay
            write_to_excel(doc, so_den)
            
            
            # Không gửi WA ngay tại đây nữa, mà đưa vào queue
            wa_pending_queue.append(doc_id)

            # 4. Lưu pending
            pending_docs[doc_id] = {
                "doc_id": doc_id,
                "doc_info": doc,
                "ai_result": ai_result,
                "status": "cho_xac_nhan",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        # Mồi gửi tin nhắn đầu tiên (nếu hàng đợi đang trống và không có tin nào đang chờ)
        send_next_wa_message()
        
        return jsonify({"found": len(docs), "processed": processed, "errors": errors})
    except Exception as e:
        logger.error(f"Lỗi trong quá trình check: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/confirm', methods=['POST'])
def confirm():
    global current_wa_doc_id
    
    data = request.json
    doc_id = data.get('doc_id')
    action = data.get('action')
    mau_index = data.get('mau_index', -1)
    ten = data.get('ten', '').strip()
    
    if doc_id not in pending_docs:
        return jsonify({"success": False, "error": "Không tìm thấy thư"}), 404
        
    doc = pending_docs[doc_id]
    
    is_completed = False
    
    if action == 'confirm':
        y_kien = MAU_Y_KIEN[mau_index] if 0 <= mau_index < len(MAU_Y_KIEN) else "Triển khai"
        
        # Tạm tắt đoạn code gọi bot tự động mở trình duyệt web vì mình đang dùng file
        # Nếu dùng Web thật (hoặc đồng bộ Web) thì mới mở lại
        # try:
        #     scraper = PlaywrightScraper()
        #     scraper.start_browser()
        #     scraper.forward_document(
        #         doc_id, 
        #         doc['ai_result']['chu_tri'], 
        #         doc['ai_result'].get('phoi_hop', []), 
        #         doc['ai_result'].get('nhan_de_biet', []), 
        #         y_kien
        #     )
        #     scraper.close_browser()
        # except Exception as e:
        #     logger.error(f"Lỗi khi chuyển thư qua scraper: {e}")
        
        doc['status'] = 'da_xu_ly'
        history_today.append(doc)
        
        # Gửi WA báo thành công
        requests.post(f"{WA_SERVER_URL}/send", json={
            "phone": WHATSAPP_PHONE,
            "message": f"✅ Đã chuyển thư [{doc['doc_info']['so_ky_hieu']}] cho {doc['ai_result']['chu_tri']}.",
            "doc_id": doc_id
        })
        is_completed = True
        
    elif action == 'change_ct':
        doc['ai_result']['chu_tri'] = ten
        requests.post(f"{WA_SERVER_URL}/send", json={
            "phone": WHATSAPP_PHONE,
            "message": f"🔄 Đã cập nhật chủ trì thành: {ten}. Vui lòng reply OK [số] để tiếp tục chuyển.",
            "doc_id": doc_id
        })
        
    elif action == 'change_ph':
        if 'phoi_hop' not in doc['ai_result']:
            doc['ai_result']['phoi_hop'] = []
        doc['ai_result']['phoi_hop'].append(ten)
        requests.post(f"{WA_SERVER_URL}/send", json={
            "phone": WHATSAPP_PHONE,
            "message": f"🔄 Đã thêm {ten} vào phối hợp. Vui lòng reply OK [số] để tiếp tục.",
            "doc_id": doc_id
        })
        
    elif action == 'skip':
        doc['status'] = 'da_bo_qua'
        history_today.append(doc)
        requests.post(f"{WA_SERVER_URL}/send", json={
            "phone": WHATSAPP_PHONE,
            "message": f"⏭️ Đã bỏ qua/hủy thư [{doc['doc_info']['so_ky_hieu']}].",
            "doc_id": doc_id
        })
        is_completed = True
        
    # Nếu văn bản đã xử lý xong (confirm hoặc skip), giải phóng current_wa_doc_id và gửi tiếp văn bản khác
    if is_completed:
        if current_wa_doc_id == doc_id:
            current_wa_doc_id = None
        # Tự động gửi tin nhắn tiếp theo
        send_next_wa_message()
        
    return jsonify({"success": True})

@app.route('/status', methods=['GET'])
def status():
    cho_xu_ly = sum(1 for d in pending_docs.values() if d['status'] == 'cho_xu_ly')
    cho_xac_nhan = sum(1 for d in pending_docs.values() if d['status'] == 'cho_xac_nhan')
    da_xu_ly = sum(1 for d in pending_docs.values() if d['status'] == 'da_xu_ly' or d['status'] == 'da_bo_qua')
    
    # Sort history latest first
    sorted_docs = sorted(pending_docs.values(), key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({
        "tong_hom_nay": tong_hom_nay,
        "cho_xu_ly": cho_xu_ly,
        "da_xu_ly": da_xu_ly,
        "cho_xac_nhan": cho_xac_nhan,
        "pending_docs": sorted_docs,
        "last_updated": datetime.now().strftime("%H:%M:%S")
    })

@app.route('/history', methods=['GET'])
def history():
    return jsonify(history_today)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
