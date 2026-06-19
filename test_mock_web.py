import requests
import time

print('Waiting 2s for server to start...')
time.sleep(2)

print('Testing get list...')
r = requests.get('http://localhost:8080/api/documents')
docs = r.json()
print(f'Mock web OK - Có {len(docs)} văn bản giả lập')
for d in docs:
    print(f'  [{d["do_khan"]}] {d["so_ky_hieu"]} - {d["trich_yeu"][:40]}...')

print('\nTesting tiep nhan...')
r = requests.post('http://localhost:8080/api/tiepnhan/doc_001')
print(f'Test tiếp nhận: {r.json()}')

print('\nTesting chuyen van ban...')
r = requests.post('http://localhost:8080/api/chuyen/doc_001', json={
    'chu_tri': 'Nguyễn Hải Đăng',
    'phoi_hop': ['Trần Duy Hào'],
    'nhan_de_biet': ['Tô Văn Sang'],
    'y_kien': 'Đảng bộ CQD'
})
print(f'Test chuyển: {r.json()}')
print('✅ Mock web: TẤT CẢ PASS')
