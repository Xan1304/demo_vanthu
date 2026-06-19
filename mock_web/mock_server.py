from flask import Flask, render_template, request, jsonify, redirect, url_for
import time
from mock_data import MOCK_DOCUMENTS, MOCK_CAN_BO, MOCK_MAU_Y_KIEN

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    return redirect('/inbox')

@app.route('/inbox', methods=['GET'])
def inbox():
    return render_template('inbox.html', documents=MOCK_DOCUMENTS)

@app.route('/document/<doc_id>', methods=['GET'])
def document_detail(doc_id):
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    if not doc:
        return "Not found", 404
    return render_template('detail.html', doc=doc)

@app.route('/api/tiepnhan/<doc_id>', methods=['POST'])
def api_tiepnhan(doc_id):
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    if doc:
        doc['trang_thai'] = 'cho_xu_ly'
        return jsonify({"success": True, "so_den": doc['so_den']})
    return jsonify({"success": False, "error": "Not found"}), 404

@app.route('/api/popup_tiepnhan/<doc_id>', methods=['GET'])
def popup_tiepnhan(doc_id):
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    return render_template('components/popup_tiepnhan.html', doc=doc)

@app.route('/api/popup_chuyen/<doc_id>', methods=['GET'])
def popup_chuyen(doc_id):
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    return render_template('components/popup_chuyen.html', doc=doc, can_bo_list=MOCK_CAN_BO, mau_y_kien=MOCK_MAU_Y_KIEN)

@app.route('/api/chuyen/<doc_id>', methods=['POST'])
def api_chuyen(doc_id):
    data = request.json
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    if doc:
        doc['trang_thai'] = 'da_chuyen'
        return jsonify({
            "success": True,
            "message": "Đồng chí đã chuyển công văn thành công"
        })
    return jsonify({"success": False, "error": "Not found"}), 404

@app.route('/api/documents', methods=['GET'])
def get_documents():
    return jsonify(MOCK_DOCUMENTS)

@app.route('/api/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    doc = next((d for d in MOCK_DOCUMENTS if d['id'] == doc_id), None)
    if doc:
        return jsonify(doc)
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
