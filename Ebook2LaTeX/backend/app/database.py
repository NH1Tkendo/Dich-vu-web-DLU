import os

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
print(settings.DATABASE_URL)

# Tải các biến môi trường từ tập tin .env

# load_dotenv()


# 1. Lấy chuỗi kết nối từ biến môi trường (qua file config đã setup sẵn)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 2. Tạo Engine: Đây là "nguồn" kết nối chính tới Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# 3. Tạo SessionLocal: Mỗi thực thể của lớp này sẽ là một phiên làm việc database

# autocommit=False: Đảm bảo dữ liệu chỉ được lưu khi ta ra lệnh commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Tạo Base class: Các models (User, Document...) sẽ kế thừa từ đây

Base = declarative_base()