from ..models.models import *
from ..utils.export_report import *

import datetime

def insert_sinh_vien_controller(MSSV, HoTen: str, GioiTinh: int, SDT: str, Email: str, DiaChi: str, MaLop: str, Truong: str, Nganh: str, Khoa: int) -> bool:
    result = insert_sinh_vien(MSSV, HoTen, GioiTinh, SDT, Email, DiaChi, MaLop, Truong, Nganh, Khoa)
    return result

def get_all_sinh_vien_controller():
    return get_all_sinh_vien()

def get_all_list_sinh_vien_controller():
    return get_all_list_sinh_vien()

def get_ds_sinh_vien_by_id_controller(kythuctap: str, detai: str, nguoihuongdan: str):
    return get_ds_sinh_vien_by_id(kythuctap, detai, nguoihuongdan)

def count_all_sinh_vien_controller():
    return count_all_sinh_vien()

def get_so_luong_sinh_vien_theo_truong_controller():
    return get_so_luong_sinh_vien_theo_truong()

def get_so_luong_sinh_vien_theo_nganh_controller():
    return get_so_luong_sinh_vien_theo_nganh()

def get_user_info_by_username_controller(username: str):
    return get_user_info_by_username(username)

def ti_le_sinh_vien_da_danh_gia_controller():
    return ti_le_sinh_vien_da_danh_gia()

def so_luong_sinh_vien_dat_ket_qua_controller():
    return so_luong_sinh_vien_dat_ket_qua()

def get_all_de_tai_thuc_tap_controller():
    return get_all_de_tai_thuc_tap()

def get_all_truong_controller():
    return get_all_truong()

def get_all_nganh_controller():
    return get_all_nganh()

def get_all_nguoi_huong_dan_controller():
    return get_all_nguoi_huong_dan()

def get_chi_tiet_de_tai_by_id_controller(id: str):
    return get_chi_tiet_de_tai_by_id(id)

def update_chi_tiet_de_tai_by_id_controller(id: str, ten: str, mota: str, isDeleted: int):
    return update_chi_tiet_de_tai_by_id(id, ten, mota, isDeleted)

def update_xoa_de_tai_by_id_controller(id: str):
    return update_xoa_de_tai_by_id(id)

def get_nhom_thuc_tap_by_user_id_controller(id: str):
    return get_nhom_thuc_tap_by_user_id(id)

def them_de_tai_thuc_tap_controller(ten: str, mota: str, isDeleted: int):
    return them_de_tai_thuc_tap(ten, mota, isDeleted)

def get_all_ky_thuc_tap_controller():
    return get_all_ky_thuc_tap()

def get_all_truong_controller():
    return get_all_truong()

def get_all_nganh_by_id_truong_controller(id: str):
    return get_all_nganh_by_id_truong(id)

def get_chi_tiet_ky_thuc_tap_by_id_controller(id: str):
    return get_chi_tiet_ky_thuc_tap_by_id(id)

def get_chi_tiet_truong_by_id_controller(id: str):
    return get_chi_tiet_truong_by_id(id)

def get_chi_tiet_nganh_by_id_controller(id: str):
    return get_chi_tiet_nganh_by_id(id)

def update_chi_tiet_ky_thuc_tap_by_id_controller(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int):
    return update_chi_tiet_ky_thuc_tap_by_id(id, ngaybatdau, ngayketthuc, isDeleted)

def update_chi_tiet_truong_by_id_controller(id: str, tentruong: str, kyhieu: str, isDeleted: int):
    return update_chi_tiet_truong_by_id(id, tentruong, kyhieu, isDeleted)

def update_chi_tiet_nganh_by_id_controller(id: str, tennganh: str, kyhieu: str, isDeleted: int, id_truong: int):
    return update_chi_tiet_nganh_by_id(id, tennganh, kyhieu, isDeleted, id_truong)

def them_ky_thuc_tap_controller(ngaybatdau: str, ngayketthuc: str, isDeleted: int):
    return them_ky_thuc_tap(ngaybatdau, ngayketthuc, isDeleted)

def them_truong_controller(tentruong: str, kyhieu: str, isDeleted: int):
    return them_truong(tentruong, kyhieu, isDeleted)

def them_nganh_controller(tennganh: str, kyhieu: str, isDeleted: int, id_truong: int):
    return them_nganh(tennganh, kyhieu, isDeleted, id_truong)

def update_xoa_ky_thuc_tap_by_id_controller(id: str):
    return update_xoa_ky_thuc_tap_by_id(id)

def update_xoa_truong_by_id_controller(id: str):
    return update_xoa_truong_by_id(id)

def update_xoa_nganh_by_id_controller(id: str):
    return update_xoa_nganh_by_id(id)

def get_ds_nhom_thuc_tap_controller():
    result = get_ds_nhom_thuc_tap()
    return result

def get_chi_tiet_nhom_thuc_tap_by_id_controller(id: str):
    result = get_chi_tiet_nhom_thuc_tap_by_id(id)
    return result

def get_chi_tiet_chinh_sua_nhom_controller():
    return get_chi_tiet_chinh_sua_nhom()

def update_chi_tiet_nhom_thuc_tap_by_id_controller(id: str, kytt: str, nguoihd: str, detai: str, isDeleted: int):
    return update_chi_tiet_nhom_thuc_tap_by_id(id, kytt, nguoihd, detai, isDeleted)

def update_xoa_nhom_thuc_tap_by_id_controller(id: str):
    return update_xoa_nhom_thuc_tap_by_id(id)

def them_nhom_thuc_tap_controller(nguoihd: str, kytt: str, detai: str, isDeleted: int):
    return them_nhom_thuc_tap(nguoihd, kytt, detai, isDeleted)

def get_chi_tiet_sinh_vien_by_id_controller(id: str):
    return get_chi_tiet_sinh_vien_by_id(id)

def get_trang_thai_sinh_vien_by_id_controller(id: str):
    return get_trang_thai_sinh_vien_by_id(id)

def get_chi_tiet_sinh_vien_chua_co_nhom_controller(id: str):
    return get_chi_tiet_sinh_vien_chua_co_nhom(id)

def get_chi_tiet_sinh_vien_da_co_nhom_controller(id: str):
    return get_chi_tiet_sinh_vien_da_co_nhom(id)

def get_chi_tiet_sinh_vien_da_danh_gia_controller(id: str):
    return get_chi_tiet_sinh_vien_da_danh_gia(id)

def verify_user_controller(username: str, password: str):
    return verify_user(username, password)

def get_ds_sinh_vien_by_username_controller(username: str, kythuctap: str):
    return get_ds_sinh_vien_by_username(username, kythuctap)

def get_chi_tiet_danh_gia_sv_by_id_controller(id: str):
    return get_chi_tiet_danh_gia_sv_by_id(id)

def get_chi_tiet_sv_by_id_controller(id: str):
    return get_chi_tiet_sv_by_id(id)

def update_danh_gia_sv_by_id_controller(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    return update_danh_gia_sv_by_id(sinhvienid, nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)

def update_danh_gia_sv_by_mssv_controller(mssv: str, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float):
    return update_danh_gia_sv_by_mssv(mssv, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)

def get_id_nhom_by_sv_id_controller(id: str):
    return get_id_nhom_by_sv_id(id)

def xuat_phieu_danh_gia_controller(id: str):
    try:
        result = get_chi_tiet_sinh_vien_da_danh_gia(id)
        return result
    except Exception as e:
        return e
    
def get_ds_nhom_chua_co_cong_viec_controller():
    return get_ds_nhom_chua_co_cong_viec()

def get_ds_nhom_da_co_cong_viec_controller():
    return get_ds_nhom_da_co_cong_viec()

def get_ds_cong_viec_by_id_nhom_controller(id: int):
    return get_ds_cong_viec_by_id_nhom(id)

def them_cong_viec_nhom_controller(id: int, tungaytuan_1: str, denngaytuan_1: str, congviectuan_1: str, tungaytuan_2: str, denngaytuan_2: str, congviectuan_2: str, tungaytuan_3: str, denngaytuan_3: str, congviectuan_3: str, tungaytuan_4: str, denngaytuan_4: str, congviectuan_4: str, tungaytuan_5: str, denngaytuan_5: str, congviectuan_5: str, tungaytuan_6: str, denngaytuan_6: str, congviectuan_6: str, tungaytuan_7: str, denngaytuan_7: str, congviectuan_7: str, tungaytuan_8: str, denngaytuan_8: str, congviectuan_8: str):
    return them_cong_viec_nhom(id, tungaytuan_1, denngaytuan_1, congviectuan_1, tungaytuan_2, denngaytuan_2, congviectuan_2, tungaytuan_3, denngaytuan_3, congviectuan_3, tungaytuan_4, denngaytuan_4, congviectuan_4, tungaytuan_5, denngaytuan_5, congviectuan_5, tungaytuan_6, denngaytuan_6, congviectuan_6, tungaytuan_7, denngaytuan_7, congviectuan_7, tungaytuan_8, denngaytuan_8, congviectuan_8)

def get_goi_y_xa_phuong_controller(q: str):
    return get_goi_y_xa_phuong(q)

def get_danh_sach_nganh_controller():
    return get_danh_sach_nganh()

def get_danh_sach_truong_controller():
    return get_danh_sach_truong()

def insert_thong_tin_sinh_vien_controller(mssv: str, hoten: str, gioitinh: int, sdt: str, email: str, diachi: str, malop: str, truong: str, nganh: str, khoa: int):
    return insert_sinh_vien(mssv, hoten, gioitinh, sdt, email, diachi, malop, truong, nganh, khoa)

def update_nhom_thuc_tap_by_sv_id_controller(idsinhvien: int, idnhom: int):
    return update_nhom_thuc_tap_by_sv_id(idsinhvien, idnhom)

def get_dssv_da_danh_gia_by_nguoi_huong_dan_controller(username: str, kythuctap: int):
    return get_dssv_da_danh_gia_by_nguoi_huong_dan(username=username, kythuctap=kythuctap)

def xoa_sinh_vien_by_sv_id_controller(idsinhvien: int):
    return xoa_sinh_vien_by_sv_id(idsinhvien)