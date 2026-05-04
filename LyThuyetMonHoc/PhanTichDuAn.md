# 1. Yêu cầu hệ thống

## 1.1 Sơ đồ hệ thống
![[Pasted image 20260406154637.png]]

## 1.2. Mô tả yêu cầu

[FR1] Hệ thống đọc tài liệu Ebook toán học dạng PDF, chỉ đọc các công thức toán học, đưa lên Giao diện

[FR2] Trên Giao diện: chuyển công thức toán từ ebook sang dạng LateX và dạng biểu thức toán học tương ứng, cho phép người dùng sửa nội dung trên giao diện. Khi sửa nội dung bên LateX thì bên Mathlive Symbol sẽ cập nhật theo, và ngược lại, sửa bên Mathlive Symbol thì bên LateX cũng cập nhật 

[FR3] Khi người dùng bấm nút Submit, nội dung LateX sẽ được lưu xuống Database

## 1.3. Lựa chọn công nghệ 

- Loại ứng dụng: Web app

- Back-end: Python (FastAPI)

- Front-end: React

- Database: PostgreSQL
# 2. Phân tích hệ thống
## 2.1. Cấu trúc thư mục dự án

Ebook2LateX/
├── .git/                   # Thư mục ẩn của Git
├── .gitignore              # Khai báo các tập không đưa vào Git
├── docker-compose.yml       # File điều phối toàn bộ hệ thống Docker
├── backend/                # Python (FastAPI)
│   ├── Dockerfile          # Cách đóng gói Backend
│   ├── app/
│   │   ├── main.py         # Điểm khởi đầu của API
│   │   ├── api/            # Các endpoint (upload, process, save)
│   │   ├── core/           # Cấu hình hệ thống, OCR model loading
│   │   ├── models/         # Định nghĩa bảng database (SQLAlchemy)
│   │   ├── services/       # Logic xử lý PDF & OCR (Parse tool)
│   │   └── schemas/        # Pydantic models (Validation dữ liệu)
│   ├── uploads/            # Lưu tạm file PDF người dùng gửi lên
│   ├── requirements.txt
│   └── .env                # Biến môi trường (DB_URL, API_KEY)
├── frontend/               # React (Vite)
│   ├── Dockerfile          # Cách đóng gói Frontend
│   ├── src/
│   │   ├── components/     # MathLiveEditor, PDFUploader, Preview
│   │   ├── hooks/          # Custom hooks xử lý logic LaTeX
│   │   ├── services/       # Kết nối API tới Backend
│   │   └── App.jsx
│   ├── package.json
│   └── public/

## 2.2 Các thành phần logic chính

## a) Back-end

- Xử lý PDF: Dùng thư viện PyMuPDF (fitz) để trích xuất hình ảnh từ PDF

- OCR Toán học: Để chuyển hình ảnh công thức sang LaTeX, sử dụng mô hình pix2tex (LaTeX-OCR)

- API: Khi nhận tập tin PDF, Backend sẽ cắt các vùng chứa công thức, chạy qua model OCR và trả về chuỗi LaTeX cho Frontend
## b) Front-end
- MathLive: Sử dụng thư viện mathlive (JavaScript). 
- Logic đồng bộ: Tạo một State trong React (ví dụ: latexContent)

    + Khi người dùng gõ vào ô Textarea (LaTeX): Cập nhật State -> MathField render lại

    + Khi người dùng sửa trên MathField: Lấy giá trị .value (dạng latex) -> Cập nhật State -> Textarea cập nhật theo
## c) Database
- Bảng dữ liệu cơ bản: Documents (ID, FileName, CreatedAt) và FormulaEntries (ID, DocumentID, RawLatex, Status)

## 2.3 Công nghệ chi tiết
- Backend Framework: FastAPI. Framework này chạy nhanh, hỗ trợ xử lý bất đồng bộ tốt khi gọi các model AI nặng

- OCR Library: pix2tex hoặc sử dụng API của Mathpix (nếu muốn độ chính xác tuyệt đối mà không cần tự train model)

- Frontend UI: Tailwind CSS (để dàn trang giao diện chỉnh sửa nhanh chóng)

- Frontend Framework: React.js — Dùng để quản lý trạng thái (State) của công thức toán học và điều khiển luồng dữ liệu giữa các thành phần

- Math Library: MathLive — Thư viện chuyên biệt nhúng vào React để hiển thị và chỉnh sửa ký hiệu toán học trực quan

- ORM: SQLAlchemy (để làm việc với PostgreSQL một cách chuyên nghiệp)

# 3. Các giai đoạn thực hiện

## 3.1 Thiết lập nền tảng và Cơ sở dữ liệu

Giai đoạn này chuẩn bị môi trường để thực hiện yêu cầu [FR3]

**_Khởi tạo dự án_**

- Tạo thư mục dự án Ebook2LateX

- Khởi tạo Git

- Tạo file: .gitignore

- Tạo repo trên Github

_**Cài đặt cơ sở dữ liệu**_

- Cài đặt PostgreSQL

- Tạo database

- Cấu hình chuỗi kết nối trong tập tin .env

- Tạo các bảng dữ liệu

- Nhập dữ liệu mẫu

**_Cấu hình Backend_**

- Cài đặt FastAPI và SQLAlchemy. Kết nối thành công từ Python đến PostgreSQL để sẵn sàng ghi dữ liệu

**_Cấu hình Frontend_**

_**Docker hóa môi trường phát triển**_

- Tạo Dockerfile cho Backend: Định nghĩa môi trường chạy Python, cài đặt các thư viện OCR và FastAPI

- Tạo Dockerfile cho Frontend: Định nghĩa môi trường chạy Node.js để build ứng dụng React

- Tạo docker-compose.yml: Đây là "nhạc trưởng" điều phối 3 dịch vụ: db: Chạy hình ảnh của PostgreSQL; backend: Chạy mã FastAPI; frontend: Chạy mã React

## 3.2 Xây dựng "Parse tool" (Xử lý PDF & OCR)

Giai đoạn này tập trung vào việc giải quyết yêu cầu [FR1]

[GD2.1] Trích xuất hình ảnh từ PDF: Sử dụng thư viện PyMuPDF để đọc tập tin PDF và cắt ra các vùng chứa công thức toán học

[GD2.2] Tích hợp Model OCR: Cài đặt mô hình pix2tex (LaTeX-OCR) vào thư mục services/

[GD2.3] Tạo API xử lý: Viết endpoint trong FastAPI để nhận tập tin PDF từ người dùng, chạy qua quy trình OCR và trả về chuỗi ký tự LaTeX

## 3.3 Phát triển Giao diện và Logic đồng bộ

Giai đoạn này hiện thực hóa yêu cầu [FR2] về tính tương tác

[GD3.1] Khởi tạo Frontend: Sử dụng React (Vite) và Tailwind CSS để dựng giao diện cơ bản gồm khu vực tải tập tin và khu vực biên tập

[GD3.2] Tích hợp MathLive: Nhúng thành phần <math-field> vào ứng dụng để hiển thị công thức trực quan

[GD3.3] Lập trình đồng bộ hai chiều:

    + Tạo State latexContent trong React

    + Viết logic để khi sửa ô văn bản (LaTeX raw), công thức trong MathLive tự động cập nhật

    + Ngược lại, khi sửa bằng biểu tượng trong MathLive, nội dung text LaTeX cũng thay đổi tương ứng
  
 ## 3.4 Hoàn thiện quy trình dữ liệu (Submit)
 
Kết nối các thành phần lại để hoàn tất yêu cầu [FR3]

[GD4.1] Kết nối Front-End và Back-End: Sử dụng thư viện axios để gửi nội dung LaTeX cuối cùng từ giao diện về API của FastAPI

[GD4.2] Xử lý lưu trữ: Backend nhận dữ liệu và sử dụng SQLAlchemy để lưu bản ghi vào PostgreSQL

## 3.5 Kiểm thử và Triển khai

[GD5.1] Kiểm thử (Testing): Thử nghiệm với các tập tin PDF toán học có độ phức tạp khác nhau để tinh chỉnh model OCR

[GD5.1] Đóng gói dự án: Viết tập tin docker-compose.yml để có thể chạy toàn bộ hệ thống (Web, API, DB) chỉ bằng một câu lệnh

