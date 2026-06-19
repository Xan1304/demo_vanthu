from excel_writer import write_to_excel
docs = [
    {'so_ky_hieu':'3737-CV/VPTU','ngay_van_ban':'04/06/2026',
     'co_quan':'VP Thanh uy TPHCM','nguoi_ky':'Le Ngoc Khanh',
     'trich_yeu':'V/v trien khai QD 176','do_mat':'Thuong',
     'do_khan':'Hoa toc','chu_tri':'Nguyen Hai Dang'},
    {'so_ky_hieu':'307-CV/DU','ngay_van_ban':'04/06/2026',
     'co_quan':'Dang uy Phuong Tay Nam','nguoi_ky':'To Van Sang',
     'trich_yeu':'V/v trien khai CT 14-CT/TU','do_mat':'Thuong',
     'do_khan':'Thuong','chu_tri':'To Van Sang'}
]
for i, d in enumerate(docs):
    write_to_excel(d, 1895+i)
    print(f'Da ghi: {d["so_ky_hieu"]}')
print('Test Excel: PASS')
