from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hashlib import sha3_256
from .controllers.controller import *

import os
import jwt
import datetime
import pandas as pd
import zipfile
import shutil

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.mount("/dist", StaticFiles(directory=os.path.join(os.getcwd(),"app","templates","dist")), name="dist")
app.mount("/plugins", StaticFiles(directory=os.path.join(os.getcwd(),"app","templates","plugins")), name="plugins")

templates = Jinja2Templates(directory=os.path.join(os.getcwd(),"app","templates"))


class UserCredentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DanhGiaSVByID(BaseModel):
    id: str
    ythuckyluat_number: float
    ythuckyluat_text: str
    tuanthuthoigian_number: float
    tuanthuthoigian_text: str
    kienthuc_number: float
    kienthuc_text: str
    kynangnghe_number: float
    kynangnghe_text: str
    khanangdoclap_number: float
    khanangdoclap_text: str
    khanangnhom_number: float
    khanangnhom_text: str
    khananggiaiquyetcongviec_number: float
    khananggiaiquyetcongviec_text: str
    danhgiachung_number: float

class ThongTinSV(BaseModel):
    mssv: str
    hoten: str
    gioitinh: int
    sdt: str
    email: str
    diachi: str
    malop: str
    truong: str
    nganh: str
    khoa: int

SECRET_KEY = "BN3298"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*6
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_user_route(credentials: UserCredentials):
    return verify_user_controller(username=credentials.username, password=sha3_256(bytes(credentials.password, 'utf-8')).hexdigest())

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return username

# Middleware để bắt lỗi 404 và xử lý
@app.middleware("http")
async def catch_404(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return templates.TemplateResponse('404.html', context={'request': request})
    return response

@app.post("/token", response_model=Token)
async def login_for_access_token(credentials: UserCredentials):
    if verify_user_route(credentials):
        access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": credentials.username}, expires_delta=access_token_expires)
        response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
        response.set_cookie("token", access_token, httponly=False)
        response.set_cookie("username", credentials.username, httponly=False)
        return response
    raise HTTPException(status_code=400, detail="Incorrect username or password")

def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/logout")
async def logout(token: str = Cookie(None)):
    response = RedirectResponse('/login')
    response.delete_cookie("token")
    return response

@app.get('/')
async def home(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                tong_sinh_vien: int = count_all_sinh_vien_controller()
                ti_le_da_danh_gia: float = ti_le_sinh_vien_da_danh_gia_controller()
                so_luong_ket_qua: int = so_luong_sinh_vien_dat_ket_qua_controller()
                return templates.TemplateResponse('index.html', context={'request': request, 'dashboard_tongsinhvien': tong_sinh_vien, 'dashboard_tiledadanhgia': ti_le_da_danh_gia, 'dashboard_soluongdat': so_luong_ket_qua['dat'], 'dashboard_soluongkhongdat': so_luong_ket_qua['khong_dat']})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/login')
async def login(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return RedirectResponse(url='/')
        except jwt.PyJWTError:
            pass
    else:
        return templates.TemplateResponse('login.html', context={'request': request})

@app.get('/sinhvien')
async def nhap_thong_tin_sinh_vien(request: Request):
    return templates.TemplateResponse('student.html', context={'request': request})

@app.get('/chonnhomthuctap')
async def chon_nhom_thuc_tap(request: Request):
    return templates.TemplateResponse('select_group.html', context={'request': request})

@app.get('/hosonguoihuongdan')
async def hosonguoihuongdan(request: Request, id: str):
    result = get_user_info_by_username(id)
    profile = {'hoten': result[0], 'sdt': result[1], 'email': result[2], 'chucdanh': result[3], 'phong': result[4], 'zalo': result[5], 'facebook': result[6], 'github': result[7], 'avatar': result[8]}
    return templates.TemplateResponse('profile.html', context={'request': request, 'profile': profile})

@app.get('/danhgiasinhvien')
async def danhgiasinhvien(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('student_review.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/danhsachsinhvien')
async def danhsachsinhvien(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('list_student.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')


@app.get('/giaoviec')
async def giaoviec(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('assign.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')
@app.get('/danhsachdetai')
async def danhsachdetai(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('projects.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/danhsachkythuctap')
async def danhsachkythuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('internships.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmtruong')
async def danhsachkythuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmtruong.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmnganh')
async def danhsachkythuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmnganh.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/danhsachnhomthuctap')
async def danhsachnhomthuctap(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('groups.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_de_tai_profile')
async def get_ds_de_tai_profile(id: str):
    return JSONResponse(status_code=200, content=get_nhom_thuc_tap_by_user_id_controller(id))

@app.get('/get_so_luong_sinh_vien_theo_truong')
async def get_so_luong_sinh_vien_theo_truong_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_so_luong_sinh_vien_theo_truong_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_so_luong_sinh_vien_theo_nganh')
async def get_so_luong_sinh_vien_theo_nganh_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_so_luong_sinh_vien_theo_nganh_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_sinh_vien')
async def get_all_sinh_vien_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_all_sinh_vien_controller()
                ds: list = [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'Nam' if i[3]==1 else 'Nữ', 'nganh': i[4], 'truong': i[5], 'trangthai': i[6], 'luuy': i[7]} for i in result]
                return JSONResponse(status_code=200, content=ds)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_list_sinh_vien')
async def get_all_list_sinh_vien_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_all_list_sinh_vien_controller()
                ds: list = [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': 'Nam' if i[3]==1 else 'Nữ', 'nganh': i[4], 'truong': i[5], 'khoa': i[6], 'trangthai': i[7], 'luuy': i[8], 'id_nhd': i[9], 'id_ktt': i[10], 'id_dtai': i[11]} for i in result]
                return JSONResponse(status_code=200, content=ds)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_sinh_vien_by_id')
async def get_ds_sinh_vien_by_id_route(kythuctap: str, detai: str, nguoihuongdan: str,token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_ds_sinh_vien_by_id_controller(kythuctap, detai, nguoihuongdan)
                ds: list = [{'id': i[0], 'mssv': i[1], 'hoten': i[2], 'gioitinh': i[3], 'sdt': i[4], 'email': i[5], 'diachi': i[6], 'malop': i[7], 'id_truong': i[8], 'id_nganh': i[9], 'khoa': i[10], 'luuy': i[12], 'tennganh': i[13], 'tentruong': i[14], 'trangthai': i[15], 'id_nhd': i[16], 'id_ktt': i[17], 'id_dtai': i[18]} for i in result]
                return JSONResponse(status_code=200, content=ds)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_user_info_by_username')
async def get_user_info_by_username_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_user_info_by_username_controller(username)
                if result:
                    return JSONResponse(status_code=200, content={'hoten': result[0], 'sdt': result[1], 'email': result[2], 'chucdanh': result[3], 'phong': result[4], 'zalo': result[5], 'facebook': result[6], 'github': result[7], 'avatar': result[8]})
                else:
                    return JSONResponse(status_code=400, content={'status': 'User not found'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_de_tai')
async def get_all_de_tai(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_de_tai_thuc_tap_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_truong')
async def get_all_truong(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_truong_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_nganh')
async def get_all_nganh(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_nganh_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_nganh_by_id_truong')
async def get_all_nganh_by_id_truong_route(id:str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_nganh_by_id_truong_controller(id))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_nguoi_huong_dan')
async def get_all_nguoi_huong_dan(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_nguoi_huong_dan_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_de_tai_by_id')
async def get_chi_tiet_de_tai_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_chi_tiet_de_tai_by_id_controller(id))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_chi_tiet_de_tai_by_id')
async def update_chi_tiet_de_tai_by_id_route(id: str, ten: str, mota: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_chi_tiet_de_tai_by_id_controller(id, ten, mota, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_xoa_de_tai_by_id')
async def update_xoa_de_tai_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_xoa_de_tai_by_id_controller(id)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_de_tai_thuc_tap')
async def them_de_tai_thuc_tap_route(ten: str, mota: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_de_tai_thuc_tap_controller(ten, mota, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_ky_thuc_tap')
async def get_all_ky_thuc_tap_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_ky_thuc_tap_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_truong')
async def get_all_truong_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_all_truong_controller())
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_ky_thuc_tap_by_id')
async def get_chi_tiet_ky_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_chi_tiet_ky_thuc_tap_by_id_controller(id))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_truong_by_id')
async def get_chi_tiet_truong_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_chi_tiet_truong_by_id_controller(id))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_nganh_by_id')
async def get_chi_tiet_nganh_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_chi_tiet_nganh_by_id_controller(id))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_chi_tiet_ky_thuc_tap_by_id')
async def update_chi_tiet_ky_thuc_tap_by_id_route(id: str, ngaybatdau: str, ngayketthuc: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_chi_tiet_ky_thuc_tap_by_id_controller(id, ngaybatdau, ngayketthuc, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_chi_tiet_truong_by_id')
async def update_chi_tiet_truong_by_id_route(id: str, tentruong: str, kyhieu: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_chi_tiet_truong_by_id_controller(id, tentruong, kyhieu, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_chi_tiet_nganh_by_id')
async def update_chi_tiet_nganh_by_id_route(id: str, tennganh: str, kyhieu: str, isDeleted: int, id_truong: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_chi_tiet_nganh_by_id_controller(id, tennganh, kyhieu, isDeleted, id_truong)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_ky_thuc_tap')
async def them_ky_thuc_tap_route(ngaybatdau: str, ngayketthuc: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_ky_thuc_tap_controller(ngaybatdau, ngayketthuc, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_truong')
async def them_truong_route(tentruong: str, kyhieu: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_truong_controller(tentruong, kyhieu, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_nganh')
async def them_truong_route(tennganh: str, kyhieu: str, isDeleted: int, id_truong: int,token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_nganh_controller(tennganh, kyhieu, isDeleted, id_truong)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_xoa_ky_thuc_tap_by_id')
async def update_xoa_ky_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_xoa_ky_thuc_tap_by_id_controller(id)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_xoa_truong_by_id')
async def update_xoa_truong_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_xoa_truong_by_id_controller(id)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_xoa_nganh_by_id')
async def update_xoa_nganh_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_xoa_nganh_by_id_controller(id)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/xoa_sinh_vien_by_sv_id')
async def xoa_sinh_vien_by_sv_id_route(idsinhvien: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = xoa_sinh_vien_by_sv_id_controller(idsinhvien)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_nhom_thuc_tap')
async def get_ds_nhom_thuc_tap_route():
    result = get_ds_nhom_thuc_tap_controller()
    return JSONResponse(status_code=200, content=result)

@app.get('/get_ds_nhom_thuc_tap_con_han')
async def get_ds_nhom_thuc_tap_con_han_route():
    result = get_ds_nhom_thuc_tap_controller()
    current_date = datetime.datetime.now().date()
    data: list = []
    for i in result:
        ngay_bat_dau = datetime.datetime.strptime(i['ngaybatdau'], '%d/%m/%Y').date()
        if ngay_bat_dau >= current_date:
            data.append(i)
    return JSONResponse(status_code=200, content=data)

@app.get('/get_ds_nhom_chua_co_cong_viec')
async def get_ds_nhom_chua_co_cong_viec_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_ds_nhom_chua_co_cong_viec_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_nhom_da_co_cong_viec')
async def get_ds_nhom_da_co_cong_viec_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_ds_nhom_da_co_cong_viec_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_cong_viec_nhom')
async def them_cong_viec_nhom_route(id: int, tungaytuan_1: str, denngaytuan_1: str, congviectuan_1: str, tungaytuan_2: str, denngaytuan_2: str, congviectuan_2: str, tungaytuan_3: str, denngaytuan_3: str, congviectuan_3: str, tungaytuan_4: str, denngaytuan_4: str, congviectuan_4: str, tungaytuan_5: str, denngaytuan_5: str, congviectuan_5: str, tungaytuan_6: str, denngaytuan_6: str, congviectuan_6: str, tungaytuan_7: str, denngaytuan_7: str, congviectuan_7: str, tungaytuan_8: str, denngaytuan_8: str, congviectuan_8: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_cong_viec_nhom_controller(id, tungaytuan_1, denngaytuan_1, congviectuan_1, tungaytuan_2, denngaytuan_2, congviectuan_2, tungaytuan_3, denngaytuan_3, congviectuan_3, tungaytuan_4, denngaytuan_4, congviectuan_4, tungaytuan_5, denngaytuan_5, congviectuan_5, tungaytuan_6, denngaytuan_6, congviectuan_6, tungaytuan_7, denngaytuan_7, congviectuan_7, tungaytuan_8, denngaytuan_8, congviectuan_8)
                if result:
                    return JSONResponse(status_code=200, content={'status': 'OK'})
                else:
                    return JSONResponse(status_code=400, content={'status': 'BAD REQUEST'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_cong_viec_by_id_nhom')
async def get_ds_cong_viec_by_id_nhom_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_ds_cong_viec_by_id_nhom_controller(id)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_nhom_thuc_tap_by_id')
async def get_chi_tiet_nhom_thuc_tap_by_id_route(id: str):
    return JSONResponse(status_code=200, content=get_chi_tiet_nhom_thuc_tap_by_id_controller(id))

@app.get('/get_chi_tiet_chinh_sua_nhom')
async def get_chi_tiet_chinh_sua_nhom_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_chi_tiet_chinh_sua_nhom_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_chi_tiet_nhom_thuc_tap_by_id')
async def update_chi_tiet_nhom_thuc_tap_by_id_route(id: str, kytt: str, nguoihd: str, detai: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_chi_tiet_nhom_thuc_tap_by_id_controller(id, kytt, nguoihd, detai, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_xoa_nhom_thuc_tap_by_id')
async def update_xoa_nhom_thuc_tap_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_xoa_nhom_thuc_tap_by_id_controller(id)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/them_nhom_thuc_tap')
async def them_nhom_thuc_tap_route(nguoihd: str, kytt: str, detai: str, isDeleted: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = them_nhom_thuc_tap_controller(nguoihd, kytt, detai, isDeleted)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_sinh_vien_by_id')
async def get_chi_tiet_sinh_vien_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                condition = get_trang_thai_sinh_vien_by_id_controller(id)
                result: dict = {}
                if condition['trangthai']==0:
                    result = get_chi_tiet_sinh_vien_chua_co_nhom_controller(id)
                elif condition['trangthai'] == 1:
                    result = get_chi_tiet_sinh_vien_da_co_nhom_controller(id)
                else:
                    result = get_chi_tiet_sinh_vien_da_danh_gia_controller(id)
                result['trangthai'] = condition['trangthai']
                return JSONResponse(status_code=200, content=result)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_ds_sinh_vien_by_username')
async def get_ds_sinh_vien_by_username_route(kythuctap: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return JSONResponse(status_code=200, content=get_ds_sinh_vien_by_username_controller(username, kythuctap))
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_list_ky_hoc_tap_for_trang_danh_gia_sv')
async def get_list_ky_hoc_tap_for_trang_danh_gia_sv(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return ""
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')


@app.get('/get_chi_tiet_danh_gia_sv_by_id')
async def get_chi_tiet_danh_gia_sv_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_chi_tiet_danh_gia_sv_by_id_controller(id=id)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_chi_tiet_sv_by_id')
async def get_chi_tiet_sv_by_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_chi_tiet_sv_by_id_controller(id=id)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.post('/update_danh_gia_sv_by_id')
async def update_danh_gia_sv_by_id_route(sinhvienid: str, nhomid: int, ythuckyluat_number: float, ythuckyluat_text: str, tuanthuthoigian_number: float, tuanthuthoigian_text: str, kienthuc_number: float, kienthuc_text: str, kynangnghe_number: float, kynangnghe_text: str, khanangdoclap_number: float, khanangdoclap_text: str, khanangnhom_number: float, khanangnhom_text: str, khananggiaiquyetcongviec_number: float, khananggiaiquyetcongviec_text: str, danhgiachung_number: float, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = update_danh_gia_sv_by_id_controller(sinhvienid, nhomid, ythuckyluat_number, ythuckyluat_text, tuanthuthoigian_number, tuanthuthoigian_text, kienthuc_number, kienthuc_text, kynangnghe_number, kynangnghe_text, khanangdoclap_number, khanangdoclap_text, khanangnhom_number, khanangnhom_text, khananggiaiquyetcongviec_number, khananggiaiquyetcongviec_text, danhgiachung_number)
                return JSONResponse(status_code=200, content={'status': 'OK'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_id_nhom_by_sv_id')
async def get_id_nhom_by_sv_id_route(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_id_nhom_by_sv_id_controller(id)
                return JSONResponse(status_code=200, content={'id': result})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/xuat_danh_gia')
async def xuat_danh_gia(id: str, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            tencty: str = 'Trung tâm CNTT - VNPT Vĩnh Long'
            if username:
                i = xuat_phieu_danh_gia_controller(id)
                if i is not TypeError:
                    r = export(username=username, mssv=i['mssv'], sv_hoten=i['hoten'], sv_lop=i['malop'], tt_donvi=tencty, tt_nguoihuongdan=i['nguoihuongdan'], dg_ythuckyluat_number=i['ythuckyluat_number'], dg_ythuckyluat_text=i['ythuckyluat_text'], dg_tuanthuthoigian_number=i['tuanthuthoigian_number'], dg_tuanthuthoigian_text=i['tuanthuthoigian_text'], dg_kienthuc_number=i['kienthuc_number'], dg_kienthuc_text=i['kienthuc_text'], dg_kynangnghe_number=i['kynangnghe_number'], dg_kynangnghe_text=i['kynangnghe_text'], dg_khanangdoclap_number=i['khanangdoclap_number'], dg_khanangdoclap_text=i['khanangdoclap_text'], dg_khanangnhom_number=i['khanangnhom_number'], dg_khanangnhom_text=i['khanangnhom_text'], dg_khananggiaiquyetcongviec_number=i['khananggiaiquyetcongviec_number'], dg_khananggiaiquyetcongviec_text=i['khananggiaiquyetcongviec_text'], dg_danhgiachung_number=i['danhgiachung_number'])
                    if r:
                        with open(r, 'rb') as f:
                            docx_content = f.read()
                        return Response(content=docx_content, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": f"attachment; filename=phieu_danh_gia_{str(i['mssv'])}.docx"})
                    else: 
                        return JSONResponse(status_code=400, content={'status': 'ERR'})
                else:
                    return JSONResponse(status_code=404, content={'status': 'Sinh viên chưa có đánh giá'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/goi_y_dia_chi')
async def goi_y_dia_chi(q: str):
    return JSONResponse(status_code=200, content=get_goi_y_xa_phuong_controller(q))

@app.get('/get_danh_sach_nganh')
async def get_danh_sach_nganh_route():
    return JSONResponse(status_code=200, content=get_danh_sach_nganh_controller())

@app.get('/get_danh_sach_truong')
async def get_danh_sach_truong_route():
    return JSONResponse(status_code=200, content=get_danh_sach_truong_controller())

@app.post('/thong_tin_sinh_vien')
async def thong_tin_sinh_vien_route(sv: ThongTinSV):
    result = insert_sinh_vien_controller(sv.mssv, sv.hoten, sv.gioitinh, sv.sdt, sv.email, sv.diachi, sv.malop, sv.truong, sv.nganh, sv.khoa)
    if result:
        response = JSONResponse(status_code=200, content={'status': 'OK'})
        response.set_cookie('studentid', result, max_age=5356800) # Hạn 2 tháng
        return response
    else:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
    
@app.get('/get_chi_tiet_sinh_vien_moi_nhap_thong_tin')
async def get_chi_tiet_sinh_vien_moi_nhap_thong_tin(id: str):
    return JSONResponse(status_code=200, content=get_chi_tiet_sinh_vien_chua_co_nhom_controller(id))

@app.post('/them_nhom_thuc_tap_sv')
async def them_nhom_thuc_tap_sv_route(idsinhvien: int, idnhom: int):
    result = update_nhom_thuc_tap_by_sv_id_controller(idsinhvien, idnhom)
    if result:
        response = JSONResponse(status_code=200, content={'status': 'OK'})
        response.set_cookie('groupid', result, max_age=5356800)
        return response
    else:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
    
@app.post('/import_danh_gia_sv')
async def import_danh_gia_sv(file: UploadFile = File(...), token: str = Cookie(None)):
    uploaded_folder = os.path.join(os.getcwd(), 'uploaded', 'xlsx')
    os.makedirs(uploaded_folder, exist_ok=True)
    
    file_path = os.path.join(uploaded_folder, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Xử lý file vừa upload
    df = pd.read_excel(file_path)
    try:
        for i in df.itertuples(index=False):
            result = update_danh_gia_sv_by_mssv_controller(i[0], i[4], i[3], i[6], i[5], i[8], i[7], i[10], i[9], i[12], i[11], i[14], i[13], i[16], i[15], i[17])
        os.remove(file_path)
        return JSONResponse(status_code=200, content={'status': 'OK'})
    except Exception as e:
        return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
    
@app.get('/xuat_ds_sinh_vien_da_danh_gia')
async def xuat_ds_sinh_vien_da_danh_gia(kythuctap: int, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                tencty: str = 'Trung tâm CNTT - VNPT Vĩnh Long'
                result = get_dssv_da_danh_gia_by_nguoi_huong_dan(username=username, kythuctap=kythuctap)
                output_path = os.path.join('DOCX', username)
                zip_output = os.path.join('DOCX', f'{username}.zip')
                # Lặp qua danh sách sinh viên có đánh giá, tạo các file docx
                for i in result:
                    r = export(username=username, mssv=i['mssv'], sv_hoten=i['hoten'], sv_lop=i['malop'], tt_donvi=tencty, tt_nguoihuongdan=i['nguoihuongdan'], dg_ythuckyluat_number=i['ythuckyluat_number'], dg_ythuckyluat_text=i['ythuckyluat_text'], dg_tuanthuthoigian_number=i['tuanthuthoigian_number'], dg_tuanthuthoigian_text=i['tuanthuthoigian_text'], dg_kienthuc_number=i['kienthuc_number'], dg_kienthuc_text=i['kienthuc_text'], dg_kynangnghe_number=i['kynangnghe_number'], dg_kynangnghe_text=i['kynangnghe_text'], dg_khanangdoclap_number=i['khanangdoclap_number'], dg_khanangdoclap_text=i['khanangdoclap_text'], dg_khanangnhom_number=i['khanangnhom_number'], dg_khanangnhom_text=i['khanangnhom_text'], dg_khananggiaiquyetcongviec_number=i['khananggiaiquyetcongviec_number'], dg_khananggiaiquyetcongviec_text=i['khananggiaiquyetcongviec_text'], dg_danhgiachung_number=i['danhgiachung_number'])
                
                # Tạo file nén các file docx
                with zipfile.ZipFile(zip_output, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(output_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, output_path)
                            zipf.write(file_path, arcname)
            
                try:
                    # Xoá thư mục chứa các file docx vừa nén
                    shutil.rmtree(output_path, ignore_errors=False, onerror=None)
                    # Download file nén
                    return FileResponse(zip_output, headers={"Content-Disposition": f"attachment; filename=dssv_{username}.zip"})
                except Exception as e:
                    return JSONResponse(status_code=400, content={'status': 'BADDDD REQUEST'})
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')