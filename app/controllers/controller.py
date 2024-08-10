from ..models.models import *
from ..utils.export_report import *

import datetime

def insert_users(idus: int, idpb: int, idtk: int,hoten: str, ngaysinh: datetime, diachi: str, sodienthoai: constr(regex=r'^\d{10,15}$'), email: str, gioitinh: bool, chucvu: str) -> bool:
    result = insert_users(idus, idpb, idtk, hoten, ngaysinh, diachi, sodienthoai, email, gioitinh, chucvu)
    return result

def insert_update_phan_quyen(idus: str, idvt: str, role: bool, trangthai: bool ) -> bool:
    result = insert_update_phan_quyen(idus, idvt, role, trangthai)
    return result   

def insert_cong_ty(idct: int, tencongty: str, diachi: str, masothue: str, dienthoai: str, fax: str, email: str) -> bool:
    result = insert_cong_ty(idct, tencongty, diachi, masothue, dienthoai, fax, email)
    return result
 
def insert_vai_tro(idvt: int, tenvaitro: str) -> bool:
    result = insert_vai_tro(idvt, tenvaitro)
    return result

def insert_tai_khoan(idtk: int, taikhoan: str, matkhau: str, ngaytao: datetime, ngaycapnhat: datetime, trangthai: bool) -> bool:
    result = insert_tai_khoan(idtk, taikhoan, matkhau, ngaytao, ngaycapnhat,  trangthai)
    return result

def insert_quan_huyen(idquan: str, tenqh: str, idtinh: str ) -> bool:
    result = insert_quan_huyen(idquan, tenqh, idtinh)
    return result

def insert_tinh_tp(idtinh: str, ten: str) -> bool:
    result = insert_tinh_tp(idtinh, ten)
    return result
    
def insert_xa_phuong(idxa: str, tenxp: str, idquan: str) -> bool:
    result = insert_xa_phuong(idxa, tenxp, idquan)
    return result

def get_all_phan_quyen_controller():
    return get_all_phan_quyen()

def get_all_vai_tro_controller():
    return get_all_vai_tro()

def get_all_cong_ty_controller():
    return get_all_cong_ty()

def get_all_cong_ty_by_tai_khoan_controller(taikhoan: str):
    return get_all_cong_ty_by_tai_khoan(taikhoan)

def get_all_cong_ty_by_date_controller(date: str):
    return get_all_cong_ty_by_date(date)

def get_all_tai_khoan_controller():
    return get_all_tai_khoan()

def get_all_users_controller():
    return get_all_users()

def get_all_danh_muc_tai_khoan_by_tai_khoan_controller(taikhoan: str):
    return get_all_danh_muc_tai_khoan_by_tai_khoan(taikhoan)

def get_all_users_by_ho_ten_controller(hoten: str):
    return get_all_users_by_ho_ten(hoten)

def capnhat_congty_by_idct_controller(idct: int, tencongty: str, diachi: str, masothue: str, dienthoai: str, fax: str, email: str):
    return capnhat_congty_by_idct(idct, tencongty, diachi, masothue, dienthoai, fax, email)

def update_vai_tro_by_idvt_controller(idvt: int, tenvaitro: str):
    return update_vai_tro_by_id(idvt, tenvaitro)

def capnhat_quan_huyen_by_idquan_controller(idquan: str, tenqh: str, idtinh: str):
    return capnhat_quan_huyen_by_idquan(idquan, tenqh, idtinh)

def capnhat_tinh_tp_by_idtinh_controller(idtinh: str, ten: str):
    return capnhat_tinh_tp_by_idtinh(idtinh, ten)

def capnhat_users_by_idus_controller(idus: str, idpb: str,idtk:str, hoten: str, ngaysinh: datetime, diachi: str, sodienthoai: str, email: str, gioitinh: str, ghichu: str, chucvu: str):
    return_users_by_idus(idus, idpb,idtk, hoten, ngaysinh, diachi, sodienthoai, email, gioitinh, ghichu, chucvu)

def capnhat_xa_phuong_by_idxa_controller(idxa: str, tenxp: str, idquan: str):
    return capnhat_xa_phuong_by_idxa(idxa, tenxp, idquan)

def update_matkhau_controller(request: UpdatePasswordRequest):
    return update_matkhau(request)

def update_xoa_users_by_idus_controller(idus: str):
    return update_xoa_users_by_idus(idus)

def update_xoa_quan_huyen_by_idquan_controller(idquan: str):
    return update_xoa_quan_huyen_by_idquan(idquan)

def update_xoa_tinh_by_idtinh_controller(idtinh: str):
    return update_xoa_tinh_by_idtinh(idtinh)

def update_xoa_xa_phuong_by_idxa_controller(idxa: str):
    returnupdate_xoa_xa_phuong_by_idxa(idxa)

def update_xoa_tai_khoan_by_idtk_controller(idtk: int):
    return xoa_tai_khoan_by_idtk(idtk)

def update_xoa_vai_tro_by_idvt_controller(idvt: int):
    return xoa_vai_tro_by_idvt(idvt)

def update_xoa_congty_by_idct_controller(idct: str):
    return xoa_congty_by_idct(idct)

def create_account_controller(request: CreateAccountRequest):
    return create_account(request)
    
def logout_controller(request: LogoutRequest):
    return logout(request)

def login_controller(request: LoginRequest):
    return login(request)