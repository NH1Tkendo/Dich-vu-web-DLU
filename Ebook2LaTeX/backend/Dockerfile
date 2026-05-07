# Sử dụng Python 3.11 slim để tối ưu dung lượng
FROM python:3.11-slim

# Ngăn Python tạo ra các file .pyc và đảm bảo log được in ra console ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (đặc biệt cho pix2tex và opencv)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tạo thư mục uploads và cấp quyền
RUN mkdir -p uploads && chmod 777 uploads

# Sao chép mã nguồn vào container
COPY . .

# Mở port 8000 (port mặc định của FastAPI)
EXPOSE 8000

# Lệnh khởi chạy ứng dụng
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
