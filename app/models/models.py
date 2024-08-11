from ..config import create_connection
import datetime

conn = create_connection()
cursor = conn.cursor()

# bảng công ty

def insert_user(idus: str, idpb: str,idtk:str, hoten: str, ngaysinh: datetime, diachi: str, sodienthoai: str, email: str, gioitinh: str, ghichu: str, chucvu: str) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", idus, idpb,idtk, hoten, ngaysinh, diachi, sodienthoai, email, gioitinh, ghichu, chucvu).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
def insert_tinh(idtinh: str, ten: str, ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?", idtinh, ten).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False   
def insert_quan_huyen(idtinh: str, idqh:str, tenqh: str, ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?", idtinh, idqh, tenqh).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False   
def insert_xa_phuong(idqh: str, idxp:str, tenxp: str, ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?", idqh, idxp, tenxp).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False  
def insert_vai_tro(idvt: str, tenvt: str, trangthai: bool, ghichu: str, ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?, ?", idvt, tenvt, trangthai, ghichu).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
def insert_quan_huyen(idquan: str, tenqh: str, idtinh: str ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?", idquan, tenqh, idtinh).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
    
    
def insert_update_phan_quyen(idus: str, idvt: str, role: bool, trangthai: bool ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?, ?", idus, idvt, role, trangthai).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
    
def insert_cong_ty(idct: int, tencongty: str, diachi: str, masothue: str, dienthoai: str, fax: str, email: str) -> bool:
    try:
        i = cursor.execute("EXEC Insercongty ?, ?, ?, ?, ?, ?, ?", idct, tencongty, diachi, masothue,dienthoai, fax, email).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False

def insert_tinh_tp(idtinh: str, ten: str) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?", idtinh, ten).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
    
def insert_xa_phuong(idxa: str, tenxp: str, idquan: str) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?", idxa, tenxp, idquan).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
      
from datetime import datetime

def insert_tai_khoan(idtk: str, taikhoan: str, matkhau: str, ngaytao: datetime, ngaycapnhat: datetime, trangthai: str, ghichu: str) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?, ?, ?, ?, ?", idtk, taikhoan, matkhau, ngaytao, ngaycapnhat, trangthai, ghichu).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False
def verify_tai_khoan(taikhoan: str, matkhau: str):
    try:
        cursor.execute("LoginTaiKhoan ?, ?", taikhoan, matkhau)
        result = cursor.fetchone()

        if not result or not result.IsValidTaiKhoan:
            return False
        return True
    except Exception as e:
        return e

def get_all_users_by_ho_ten(hoten: str):
    try:
        result = cursor.execute("EXEC GetusersByhoten ?", hoten).fetchall()
        data = [{'idus': i[0], 'idpb': i[1], 'hoten': i[2], 'ngaysinh': i[3], 'diachi': i[4], 'sodienthoai': i[5], 'emai': i[6], 'gioitinh': i[7], 'chucvu': i[8], 'trangthai': i[9]} for i in result]
        return data
    except Exception as e:
        return e
    
def get_all_danh_muc_tai_khoan_by_tai_khoan(taikhoan: str):
    try:
        result = cursor.execute("EXEC GetDanhMucTaiKhoanByTaiKhoan ?", id).fetchall()
        data = [{'idtk': i[0], 'taikhoan': i[1], 'trangthai': i[2], 'ghichu': i[3],} for i in result]
        return data
    except Exception as e:
        return e

def get_all_user_by_ht():
    try:
        result = cursor.execute("EXEC GetUserByHT ?", id).fetchall()
        data = [{'idus':i[0], 'idpb':i[1],'idtk':i[2], 'hoten':i[3], 'ngaysinh':i[4], 'diachi':i[5], 'sodienthoai':i[6], 'email':i[7], 'gioitinh':i[8], 'ghichu':i[9], 'chucvu':i[10],} for i in result]
        return data
    except Exception as e:
        return e

def get_all_vai_tro():
    try:
        result = cursor.execute("EXEC GetDSVTDashboard").fetchall()
        return result
    except Exception as e:
        return e
def get_all_phan_quyen():
    try:
        result = cursor.execute("EXEC GetDSPQDashboard").fetchall()
        return result
    except Exception as e:
        return e
def get_all_tai_khoan():
    try:
        result = cursor.execute("EXEC GetDSTKDashboard").fetchall()
        return result
    except Exception as e:
        return e

def get_all_cong_ty():
    try:
        result = cursor.execute("EXEC GetCTYDashboard").fetchall()
        return result
    except Exception as e:
        return e

def get_all_cong_ty_by_tai_khoan(taikhoan: str):
    try:
        result = cursor.execute("EXEC GetallcontyByTaiKhoan ?", id).fetchall()
        data = [{'idct': i[0], 'tencongty': i[1], 'diachi': i[2], 'masothue': i[3], 'dienthoai': i[4], 'fax': i[5], 'email': i[6]} for i in result]
        return data
    except Exception as e:
        return e

def get_all_cong_ty_by_date(date: str):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?, ?,?", idus, idvt, trangthai,ghichu)
        conn.commit()
        return True
    except Exception as e:
        return e
def capnhat_tinh(idtinh: str, ten: str, ):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?", idtinh,ten)
        conn.commit()
        return True
    except Exception as e:
        return e
def capnhat_quan_huyen(idtinh: str,idqh:str, tenqh: str, ):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?", idtinh, idqh,tenqh)
        conn.commit()
        return True
    except Exception as e:
        return e
def capnhat_xa_phuong(idqh: str, idxp:str, tenxp: str, ):
    try:
        result = cursor.execute("EXEC GetallcontyByTaiKhoan ?", id).fetchall()
        data = [{'idct': i[0], 'tencongty': i[1], 'diachi': i[2], 'masothue': i[3], 'dienthoai': i[4], 'fax': i[5], 'email': i[6]} for i in result]
        return data
    except Exception as e:
        return e

        conn.commit()
        return True
    except Exception as e:
        return e
    
def capnhat_congty_by_idct(idct: int, tencongty: str, diachi: str, masothue: str, dienthoai: str, fax: str, email: str):
    try:
        result = cursor.execute("EXEC Insertconty ?, ?, ?, ?, ?, ?, ?", idct, tencongty, diachi, masothue, dienthoai, fax, email)
        conn.commit()
        return True
    except Exception as e:
        return e
      
class UpdatePasswordRequest:
    def __init__(self, taikhoan: str, new_password: str):
        self.taikhoan = taikhoan
        self.new_password = new_password
def doi_mk(request: UpdatePasswordRequest) -> bool:
    try:
        cursor.execute("EXEC UpdateMatKhau ?, ?", request.taikhoan, request.new_password)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
