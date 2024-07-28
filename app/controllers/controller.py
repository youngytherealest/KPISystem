from ..models.models import *
from ..utils.export_report import *

import datetime


def insert_users(
    idus: int,
    idpb: int,
    idtk: int,
    hoten: str,
    ngaysinh: datetime,
    diachi: str,
    sodienthoai: str,
    email: str,
    gioitinh: bool,
    chucvu: str,
) -> bool:
    result = insert_users(
        idus, idpb, idtk, hoten, ngaysinh, diachi, sodienthoai, email, gioitinh, chucvu
    )
    return result


def insert_vai_tro(idvt: int, tenvaitro: str) -> bool:
    result = insert_vai_tro(idvt, tenvaitro)
    return result


def insert_phan_quyen(idus: int, idvt: int, trangthai: bool, ghichu: str) -> bool:
    result = insert_phan_quyen(idus, idvt, trangthai, ghichu)
    return result


def insert_tai_khoan(
    idtk: int,
    taikhoan: str,
    matkhau: str,
    ngaytao: datetime,
    ngaycapnhat: datetime,
    trangthai: bool,
) -> bool:
    result = insert_tai_khoan(idtk, taikhoan, matkhau, ngaytao, ngaycapnhat, trangthai)
    return result


def get_all_phan_quyen_controller():
    return get_all_phan_quyen()


def get_all_vai_tro_controller():
    return get_all_vai_tro()


def get_all_tai_khoan_controller():
    return get_all_tai_khoan()


def get_all_dmtaikhoan_by_tai_khoan_controller(taikhoan: str):
    return get_all_dmtaikhoan_by_tai_khoan(taikhoan)


def update_phan_quyen_by_id_controller(
    idus: int, idvt: int, trangthai: bool, ghichu: str
):
    return update_phan_quyen_by_id(idus, idvt, trangthai, ghichu)


def update_vai_tro_by_id_controller(idvt: int, tenvaitro: str):
    return update_vai_tro_by_id(idvt, tenvaitro)


def update_matkhau_controller(request: UpdatePasswordRequest):
    return update_matkhau(request)


def xoa_phan_quyen_by_idus_controller(idus: int):
    return xoa_phan_quyen_by_idus(idus)


def xoa_tai_khoan_by_idtk_controller(idtk: int):
    return xoa_tai_khoan_by_idtk(idtk)


def xoa_vai_tro_by_idvt_controller(idvt: int):
    return xoa_vai_tro_by_idvt(idvt)


def create_account_controller(request: CreateAccountRequest):
    return create_account(request)


def logout_controller(request: LogoutRequest):
    return logout(request)


def login_controller(request: LoginRequest):
    return login(request)
