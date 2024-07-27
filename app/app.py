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

class DanhGiaNVByID(BaseModel):
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

class ThongTinUser(BaseModel):
    idus: str
    idbp: str
    hoten: str
    ngaysinh:str
    diachi: str
    sdt: str
    email: str
    gioitinh: int
    chucvu: str
    trangthai: bool
SECRET_KEY = "BN3298"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*6
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_user_route(credentials: UserCredentials):
    return verify_user_controller(username=credentials.username, password=Us_123(bytes(credentials.password, 'utf-8')).hexdigest())

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
                tong_sinh_vien: int = count_all_user_controller()
                return templates.TemplateResponse('index.html', context={'request': request, 'dashboard_tonguser': tong_user, 'dashboard_tiledadanhgia': ti_le_da_danh_gia, 'dashboard_soluongdat': so_luong_ket_qua['dat'], 'dashboard_soluongkhongdat': so_luong_ket_qua['khong_dat']})
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

@app.get('/users')
async def nhap_thong_tin_user(request: Request):
    return templates.TemplateResponse('staff.html', context={'request': request})

@app.get('/chonbophan')
async def chon_bo_phan(request: Request):
    return templates.TemplateResponse('select_part.html', context={'request': request})

@app.get('/danhgiausers')
async def danhgiausers(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('staff_review.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/danhsachuser')
async def danhsachuser(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('list_staff.html', context={'request': request})            
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/danhsachcongty')
async def danhsachcongty(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dscty.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmbophan')
async def danhsachcongty(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmbophan.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmphongban')
async def danhsachcongty(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmphongban.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmvaitro')
async def danhsachcongty(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmvaitro.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/dmtaikhoan')
async def dmtaikhoan(request: Request, token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return templates.TemplateResponse('dmtaikhoan.html', context={'request': request})
                
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_dm_tai_khoan_profile')
async def get_dm_tai_khoan_profile(taikhoan: str):
    return JSONResponse(status_code=200, content=get_danh_muc_tai_khoan_by_tai_khoan_controller(taikhoan))

@app.get('/get_so_luong_users_theo_bo_phan')
async def get_so_luong_users_theo_bo_phan_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_so_luong_users_theo_bo_phan_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_so_luong_users_theo_vai_tro')
async def get_so_luong_users_theo_vai_tro_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_so_luong_users_theo_vai_tro_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_so_luong_users_theo_phong_ban')
async def get_so_luong_users_theo_phong_ban_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                return get_so_luong_users_theo_phong_ban_controller()
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')

@app.get('/get_all_users')
async def get_all_users_route(token: str = Cookie(None)):
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                result = get_all_users_controller()
                ds: list = [{'idus': i[0], 'idpb': i[1], 'hoten': i[2], 'ngaysinh': i[3], 'diachi': i[4], 'sodienthoai': i[5], 'emai': i[6], 'gioitinh': i[7], 'chucvu': i[8], 'trangthai': i[9]} for i in result]
                return JSONResponse(status_code=200, content=ds)
        except jwt.PyJWTError:
            pass
    return RedirectResponse('/login')