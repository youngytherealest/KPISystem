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
    
def insert_tai_khoan(idtk:str, taikhoan: str, matkhau: str, ngaytao: datetime, ngaycapnhat: datetime, ) -> bool:
    try:
        i = cursor.execute("EXEC InsertUser ?, ?, ?, ?", idvt, tenvt, trangthai, ghichu).fetchone()
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
    
def get_all_users():
    try:
        result = cursor.execute("EXEC GetDSVTDashboard").fetchall()
        return result
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
def capnhat_phan_quyen_by_idus(idus: str, idvt: str, trangthai: bool, ghichu:str):
    try:
        result = cursor.execute("EXEC Insertphanquyen ?, ?, ?", idus, idvt, trangthai,ghichu)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def capnhat_quan_huyen_by_idquan(idquan: str, tenqh: str, idtinh: str):
    try:
        result = cursor.execute("EXEC Insertquanhuyen ?, ?, ?", idquan, tenqh, idtinh)
        conn.commit()
        return True
    except Exception as e:
        return e

def capnhat_tinh_tp_by_idtinh(idtinh: str, ten: str):
    try:
        result = cursor.execute("EXEC Inserttinh ?, ?", idtinh, ten)
        conn.commit()
        return True
    except Exception as e:
        return e

def capnhat_users_by_idus(idus: str, idpb: str,idtk:str, hoten: str, ngaysinh: datetime, diachi: str, sodienthoai: str, email: str, gioitinh: str, ghichu: str, chucvu: str):
    try:
        result = cursor.execute("EXEC InsertUser ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", idus, idpb,idtk, hoten, ngaysinh, diachi, sodienthoai, email, gioitinh, ghichu, chucvu)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def capnhat_xa_phuong_by_idxa(idxa: str, tenxp: str, idquan: str):
    try:
        result = cursor.execute("EXEC InsertUser ?, ?, ?", idxa, tenxp, ididquan)
        conn.commit()
        return True
    except Exception as e:
        return e

def capnhat_vai_tro_by_idvt(idvt: str, tenvt: str, trangthai: bool, ghichu:str):
    try:
        result = cursor.execute("EXEC Insertvaitro ?, ?, ?", idvt, tenvt, trangthai,ghichu)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_matkhau(request: UpdatePasswordRequest):
    try:
        result = cursor.execute("EXEC UpdateMatKhau ?, ?",  request.taikhoan, request.new_password)
        conn.commit()
        return True
    except Exception as e:
        return e

def update_xoa_tai_khoan_by_idtk(idtk: str):
    try:
        result = cursor.execute("EXEC UpdateXoaTaiKhoanByIDTK ?", idtk)
        conn.commit()
        return True
    except Exception as e:
        return e
def update_xoa_users_by_idus(idus: str):
    try:
        result = cursor.execute("EXEC UpdateXoausersbyidus ?", idus)
        conn.commit()
        return True
    except Exception as e:
        return e

def update_xoa_quan_huyen_by_idquan(idquan: str):
    try:
        result = cursor.execute("EXEC UpdateXoaquanhuyenbyidquan ?", idquan)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def update_xoa_tinh_by_idtinh(idtinh: str):
    try:
        result = cursor.execute("EXEC Updatexoatinhbyidtinh ?", idtinh)
        conn.commit()
        return True
    except Exception as e:
        return e
    
def update_xoa_xa_phuong_by_idxa(idxa: str):
    try:
        result = cursor.execute("EXEC Updatexoaxaphuongbyidxa ?", idxa)
        conn.commit()
        return True
    except Exception as e:
        return e

def update_xoa_vai_tro_by_idvt(idvt: str):
    try:
        result = cursor.execute("EXEC UpdateXoaVaiTroByIDVT ?", idvt)
        conn.commit()
        return True
    except Exception as e:
        return e
def create_account(request: CreateAccountRequest):
    try:
        result = cursor.execute("EXEC INSERTtk ?, ?, ?", request.taikhoan, request.matkhau, request.trangthai)
        r = result.fetchone()[0]
        cursor.commit()
        return r
    except Exception as e:
        return e
def logout(request: LogoutRequest):
    try: 
        result = cursor.execute("EXEC SPLOGOUT ?", request.taikhoan)
        r = result.fetchone()[0]
        cursor.commit()
        return r
    except Exception as e:
        return e
    
def login(request: LoginRequest):
    try: 
        result = cursor.execute("EXEC SPLOGIN ?, ?", request.taikhoan, request.matkhau)
        r = result.fetchone()[0]
        cursor.commit()
        return r
    except Exception as e:
        return e
