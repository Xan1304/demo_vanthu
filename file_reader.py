import os
import shutil
import uuid
import docx
from datetime import datetime

INBOX_DIR = "data/inbox"
PROCESSED_DIR = "data/processed"

def read_pending_files():
    """
    Reads .txt and .docx files from the inbox directory.
    Returns a list of document objects.
    Moves processed files to the processed directory.
    """
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    docs = []
    
    for filename in os.listdir(INBOX_DIR):
        if not (filename.endswith(".txt") or filename.endswith(".docx")):
            continue
            
        filepath = os.path.join(INBOX_DIR, filename)
        content = ""
        
        try:
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            elif filename.endswith(".docx"):
                doc = docx.Document(filepath)
                content = "\n".join([para.text for para in doc.paragraphs])
                
            # Create a mock document object based on file content
            # We use filename as so_ky_hieu, and content as trich_yeu
            doc_id = f"doc_{uuid.uuid4().hex[:8]}"
            so_ky_hieu = filename.rsplit(".", 1)[0]
            
            docs.append({
                "doc_id": doc_id,
                "so_ky_hieu": so_ky_hieu,
                "ngay_van_ban": datetime.now().strftime("%d/%m/%Y"),
                "co_quan": "Cơ quan gửi (Từ File)",
                "nguoi_ky": "Người ký (Từ File)",
                "do_khan": "Thường",
                "trang_thai": "cho_tiep_nhan",
                "trich_yeu": content.strip() or "Không có nội dung"
            })
            
            # Move to processed
            shutil.move(filepath, os.path.join(PROCESSED_DIR, filename))
            
        except Exception as e:
            print(f"Lỗi khi đọc file {filename}: {e}")

    return docs
