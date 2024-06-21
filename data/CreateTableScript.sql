CREATE TABLE SinhVien (
	ID int IDENTITY(1,1) PRIMARY KEY,
	MSSV varchar(10) NOT NULL,
	HoTen nvarchar(128) NOT NULL,
	GioiTinh int,
	SDT varchar(11) NOT NULL,
	Email varchar(128),
	DiaChi nvarchar(255),
	MaLop varchar(10) NOT NULL,
	Truong nvarchar(128) NOT NULL,
	Nganh nvarchar(128) NOT NULL,
	Khoa int NOT NULL,
	NhomHuongDan int 
);

CREATE TABLE NguoiHuongDan (
	ID int IDENTITY(1,1) PRIMARY KEY,
	HoTen nvarchar(255) NOT NULL,
	SDT varchar(11) NOT NULL,
	Email varchar(128),
	ChucDanh nvarchar(255),
	Phong nvarchar(255) NOT NULL,
	Username varchar(24) NOT NULL,
	Password varchar(MAX) NOT NULL,
	Zalo varchar(11),
	Facebook varchar(255),
	Github varchar(255)
);

CREATE TABLE KyThucTap (
	ID INT IDENTITY(1,1) PRIMARY KEY,
	NgayBatDau DATE NOT NULL,
	NgayKetThuc DATE NOT NULL,
	isDeleted int NOT NULL
);

CREATE TABLE NhomHuongDan (
    ID int IDENTITY(1,1) PRIMARY KEY,
    NguoiHuongDanID int REFERENCES NguoiHuongDan(ID),
    KyThucTapID int REFERENCES KyThucTap(ID),
	isDeleted int NOT NULL
);


CREATE TABLE DanhGia (
	ID int IDENTITY(1,1) PRIMARY KEY,
    SinhVienID int NOT NULL REFERENCES SinhVien(ID),
	NhomHuongDanID int NOT NULL REFERENCES NhomHuongDan(ID),
	YThucKyLuat_number float NOT NULL,
	YThucKyLuat_text nvarchar(max),
	TuanThuThoiGian_number float NOT NULL,
	TuanThuThoiGian_text nvarchar(max),
	KienThuc_number float NOT NULL,
	KienThuc_text nvarchar(max),
	KyNangNghe_number float NOT NULL,
	KyNangNghe_text nvarchar(max),
	KhaNangDocLap_number float NOT NULL,
	KhaNangDocLap_text nvarchar(max),
	KhaNangNhom_number float NOT NULL,
	KhaNangNhom_text nvarchar(max),
	KhaNangGiaiQuyetCongViec_number float NOT NULL,
	KhaNangGiaiQuyetCongViec_text nvarchar(max),
	DanhGiaChung_number float NOT NULL
);

CREATE TABLE DeTai (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Ten nvarchar(max) NOT NULL,
	MoTa ntext,
	isDeleted int NOT NULL
);

-- Tao bang truong
CREATE TABLE Truong (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Ten nvarchar(max) NOT NULL,
	KyHieu varchar(10) NOT NULL,
);

-- Tao Nganh
CREATE TABLE Nganh (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Ten nvarchar(max) NOT NULL,
	KyHieu varchar(10) NOT NULL
);

ALTER TABLE SinhVien
ADD NhomHuongDan int REFERENCES NhomHuongDan(ID)

CREATE TABLE XaPhuong (
	ID int IDENTITY(1,1) PRIMARY KEY,
	DiaChi nvarchar(max) NOT NULL
)