from ..config import create_connection
import datetime
from pydantic import BaseModel

conn = create_connection()
cursor = conn.cursor()

# bảng công ty


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class LoginRequest(BaseModel):
    taikhhoan: str
    matkhau: str


class LogoutRequest(BaseModel):
    taikhhoan: str
    matkhau: str


class CreateAccountRequest(BaseModel):
    old_password: str
    new_password: str


def insert_user(
    idus: str,
    idpb: str,
    idtk: str,
    hoten: str,
    ngaysinh: datetime,
    diachi: str,
    sodienthoai: str,
    email: str,
    gioitinh: str,
    ghichu: str,
    chucvu: str,
) -> bool:
    try:
        i = cursor.execute(
            "EXEC InsertUser ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
            idus,
            idpb,
            idtk,
            hoten,
            ngaysinh,
            diachi,
            sodienthoai,
            email,
            gioitinh,
            ghichu,
            chucvu,
        ).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False


def insert_vai_tro(
    idvt: str,
    tenvt: str,
    trangthai: bool,
    ghichu: str,
) -> bool:
    try:
        i = cursor.execute(
            "EXEC InsertUser ?, ?, ?, ?", idvt, tenvt, trangthai, ghichu
        ).fetchone()
        result = i[0]
        conn.commit()
        return result
    except Exception as e:
        print(e)
        return False


def insert_tai_khoan(
    idtk: str,
    taikhoan: str,
    matkhau: str,
    ngaytao: datetime,
    ngaycapnhat: datetime,
) -> bool:
    try:
        i = cursor.execute(
            "EXEC InsertUser ?, ?, ?, ?", idvt, tenvt, trangthai, ghichu
        ).fetchone()
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
        data = [
            {
                "idtk": i[0],
                "taikhoan": i[1],
                "trangthai": i[2],
                "ghichu": i[3],
            }
            for i in result
        ]
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


def capnhat_phan_quyen(idus: str, idvt: str, trangthai: bool, ghichu: str):
    try:
        result = cursor.execute(
            "EXEC InsertKyThucTap ?, ?, ?", idus, idvt, trangthai, ghichu
        )
        conn.commit()
        return True
    except Exception as e:
        return e


def capnhat_vai_tro(idvt: str, tenvt: str, trangthai: bool, ghichu: str):
    try:
        result = cursor.execute(
            "EXEC InsertKyThucTap ?, ?, ?", idvt, tenvt, trangthai, ghichu
        )
        conn.commit()
        return True
    except Exception as e:
        return e


def doi_mk(request: UpdatePasswordRequest):
    try:
        result = cursor.execute(
            "EXEC UpdateMatKhau ?, ?", request.taikhoan, request.new_password
        )
        conn.commit()
        return True
    except Exception as e:
        return e


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


def create_account(request: CreateAccountRequest):
    try:
        result = cursor.execute(
            "EXEC INSERTtk ?, ?, ?",
            request.taikhoan,
            request.matkhau,
            request.trangthai,
        )
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
