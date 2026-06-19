class MockScraper:
    def __init__(self):
        pass

    def start_browser(self):
        print("Mock: Bắt đầu browser")

    def get_pending_documents(self):
        print("Mock: Lấy danh sách văn bản chờ...")
        return [
            {
                "doc_id": "doc_1",
                "so_ky_hieu": "3737-CV/VPTU",
                "ngay_van_ban": "04/06/2026",
                "co_quan": "VP Thành ủy TPHCM",
                "nguoi_ky": "Lê Ngọc Khánh",
                "trich_yeu": "V/v triển khai QĐ 176 về thủ tục hành chính",
                "do_mat": "Thường",
                "do_khan": "Hỏa tốc"
            },
            {
                "doc_id": "doc_2",
                "so_ky_hieu": "307-CV/DU",
                "ngay_van_ban": "04/06/2026",
                "co_quan": "Đảng ủy Phường Tây Nam",
                "nguoi_ky": "Tô Văn Sang",
                "trich_yeu": "V/v triển khai chỉ thị",
                "do_mat": "Thường",
                "do_khan": "Thường"
            },
            {
                "doc_id": "doc_3",
                "so_ky_hieu": "402-KT-HTDT",
                "ngay_van_ban": "05/06/2026",
                "co_quan": "Phòng Kinh tế",
                "nguoi_ky": "Nguyễn Văn C",
                "trich_yeu": "Đăng ký tập huấn kế toán tài chính",
                "do_mat": "Thường",
                "do_khan": "Thường"
            }
        ]

    def get_document_detail(self, doc_id):
        return {"doc_id": doc_id, "detail": "Chi tiết mock"}

    def forward_document(self, doc_id, chu_tri, phoi_hop, nhan_de_biet, y_kien):
        print(f"Mock: Chuyển văn bản {doc_id} cho {chu_tri}")
        return True

    def close_browser(self):
        print("Mock: Đóng browser")
