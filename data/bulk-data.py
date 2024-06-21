import pandas as pd
import pyodbc

server = '10.91.13.128'
database = 'SVTT'
username = 'sa'
password = 'Vnpt@123'

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};CHARSET=UTF8')

# Đối với pyodbc
cursor = conn.cursor()
cursor.execute("UPDATE SinhVien SET NhomHuongDan = 25 WHERE NhomHuongDan=999")
cursor.commit()
# df = pd.DataFrame(pd.read_excel('dssvtt2024.xlsx'))

# for i in df.itertuples(index=False):
#     gioitinh: int = 1
#     if i[2] != 'Nam':
#         gioitinh = 0
#     ins_query = cursor.execute("INSERT INTO SinhVien VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i[0], i[1], gioitinh, i[3], i[5], i[4], i[7], 'VLUTE', i[6], 45, 999)
#     cursor.commit()
#     print(f'inserted {i[1]}')
# Đóng kết nối sau khi hoàn thành
conn.close()
