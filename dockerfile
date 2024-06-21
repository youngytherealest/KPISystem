FROM laudio/pyodbc:1.0.38

# Đặt thư mục làm thư mục làm việc cho ứng dụng
WORKDIR /app

# Sao chép tất cả các file trong thư mục hiện tại vào thư mục /app trên Docker
COPY . /app

# Cập nhật hệ thống và cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Thêm Microsoft repository key và repository cho msodbcsql17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Cập nhật hệ thống và cài đặt msodbcsql17
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && apt-get install -y unixodbc-dev

# Cài đặt các gói phụ thuộc để chạy ứng dụng
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt 
# Expose cổng 80 để ứng dụng có thể truy cập từ bên ngoài Docker
EXPOSE 10000

# Khởi động ứng dụng FastAPI
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "4"]
