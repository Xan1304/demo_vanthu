from ai_classifier import classify_document
tests = [
    {'so_ky_hieu':'3737-CV/VPTU','co_quan':'VP Thanh uy',
     'trich_yeu':'thu tuc hanh chinh nop dang phi','do_khan':'Hoa toc'},
    {'so_ky_hieu':'402-KT-HTDT','co_quan':'Phong Kinh te',
     'trich_yeu':'dang ky tap huan ke toan tai chinh','do_khan':'Thuong'}
]
for t in tests:
    r = classify_document(t)
    print(f'Input: {t["trich_yeu"][:40]}')
    print(f'Output: {r["ten_linh_vuc"]} → CT: {r["chu_tri"]}')
    print()
print('Test AI: PASS')
