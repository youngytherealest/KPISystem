from ..config import create_connection
import datetime

conn = create_connection()
cursor = conn.cursor()

# bảng công ty

def insert_user(idus: str, idpb: str,idtk:str, hoten: str, ngaysinh: datetime, diachi: str, sodienthoai: str, email: str, gioitinh: str, ghichu: str, chucvu: str,) -> bool:
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
def get_all_danh_muc_tai_khoan_by_tai_khoan(taikhoan: str):
    try:
        result = cursor.execute("EXEC GetDanhMucTaiKhoanByTaiKhoan ?", id).fetchall()
        data = [{'idtk': i[0], 'taikhoan': i[1], 'trangthai': i[2], 'ghichu': i[3],} for i in result]
        return data
    except Exception as e:
        return e
def get_all_user_by():
    try:
        result = cursor.execute("EXEC GetUserBy ?", id).fetchall()
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
def capnhat_phan_quyen(idus: str, idvt: str, trangthai: bool, ghichu:str):
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
        result = cursor.execute("EXEC InsertKyThucTap ?, ?", idqh, idxp,tenxp)
        conn.commit()
        return True
    except Exception as e:
        return e
def capnhat_vai_tro(idvt: str, tenvt: str, trangthai: bool, ghichu:str):
    try:
        result = cursor.execute("EXEC InsertKyThucTap ?, ?, ?", idvt, tenvt, trangthai,ghichu)
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
"""def update_xoa_phan_quyen_by_idus(idus: str):
    try:
        result = cursor.execute("EXEC UpdateXoaPhanQuyenByIDUS ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e"""
def update_xoa_tai_khoan_by_idtk(idtk: str):
    try:
        result = cursor.execute("EXEC UpdateXoaTaiKhoanByIDTK ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_xoa_vai_tro_by_idvt(idvt: str):
    try:
        result = cursor.execute("EXEC UpdateXoaVaiTroByIDVT ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_xoa_tinh_by_idtinh(idtinh: str):
    try:
        result = cursor.execute("EXEC UpdateXoaTinhByIdtinh ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_xoa_quan_huyen_by_idqh(idqh: str):
    try:
        result = cursor.execute("EXEC UpdateXoaQHByIdqh ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_xoa_xa_phuong_by_idxp(idxp: str):
    try:
        result = cursor.execute("EXEC UpdateXoaXPByIdxp ?", id)
        conn.commit()
        return True
    except Exception as e:
        return e
class CreateAccountRequest:
    def __init__(self, taikhoan: str, matkhau: str, trangthai: str):
        self.taikhoan = taikhoan
        self.matkhau = matkhau
        self.trangthai = trangthai
def create_account(request: CreateAccountRequest):
    try:
        result = cursor.execute("EXEC INSERTtk ?, ?, ?", request.taikhoan, request.matkhau, request.trangthai)
        r = result.fetchone()[0]
        conn.commit()  # Use conn.commit() instead of cursor.commit()
        return r
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return None  # Return None or an appropriate value in case of an exception
class LogoutRequest:
    def __init__(self, taikhoan: str):
        self.taikhoan = taikhoan
def logout(request: LogoutRequest):
    try: 
        result = cursor.execute("EXEC SPLOGOUT ?", request.taikhoan)
        r = result.fetchone()[0]
        conn.commit()  # Use conn.commit() instead of cursor.commit()
        return r
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return None  # Return None or an appropriate value in case of an exception
class LoginRequest:
    def __init__(self, taikhoan: str, matkhau: str):
        self.taikhoan = taikhoan
        self.matkhau = matkhau


def login(request: LoginRequest):
    try: 
        result = cursor.execute("EXEC SPLOGIN ?, ?", request.taikhoan, request.matkhau)
        r = result.fetchone()[0]
        conn.commit()  # Use conn.commit() instead of cursor.commit()
        return r
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return None  # Return None or an appropriate value in case of an exception

