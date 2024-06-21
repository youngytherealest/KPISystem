import pymongo
from typing import Union, Any
from datetime import datetime
import json
from bson import ObjectId

client = pymongo.MongoClient('mongodb+srv://giangphan028:ThanhGiang2808@cluster0.vzpfca2.mongodb.net/')
database = client['SinhVienThucTap']

danhgia = database['DanhGia']
detai = database['DeTai']
kythuctap = database['KyThucTap']
nganhhoc = database['NganhHoc']
nguoihuongdan = database['NguoiHuongDan']
nhomhuongdan = database['NhomHuongDan']
sinhvien = database['SinhVien']
truong = database['Truong']
xaphuong = database['XaPhuong']
lienhe = database['LienHe']
log = database['LogHoatDong']
conf = database['CauHinh']

result = nhomhuongdan.aggregate([
    {
        '$lookup': {
            'from': 'NguoiHuongDan',
            'localField': 'instructor',
            'foreignField': '_id',
            'as': 'instructor'
        }
    },
    {
        '$unwind': '$instructor'
    },
    {
        '$lookup': {
            'from': 'DeTai',
            'localField': 'project',
            'foreignField': '_id',
            'as': 'project'
        }
    },
    {
        '$unwind': '$project'
    },
    {
        '$lookup': {
            'from': 'KyThucTap',
            'localField': 'internship',
            'foreignField': '_id',
            'as': 'internship'
        }
    },
    {
        '$unwind': '$internship'
    },
    {
        '$lookup': {
            'from': 'SinhVien',
            'localField': '_id',
            'foreignField': 'intern_group',
            'as': 'student'
        }
    },
    {
        '$unwind': '$student'
    },
    {
        '$project':{
            'username': '$instructor.username',
            'nhd': '$instructor.id',
            'kytt': '$internship.start',
            'detai': '$project.id',
            '_id': 0,
            'id': 1,
            'mssv': '$student.student_id'
        }
    }
])

data: list = []

for i in result:
    data.append(i)

with open(f"nhomtt.json", encoding="utf8", mode="w") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))