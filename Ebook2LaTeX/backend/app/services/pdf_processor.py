"""
PDF Processing Service using PyMuPDF (fitz).
"""
import io
import logging

import fitz  # PyMuPDF
from PIL import Image

logger = logging.getLogger(__name__)


def extract_formula_images_from_pdf(pdf_path: str) -> list[Image.Image]:
    """
    Mở file PDF và trích xuất các hình ảnh được nhúng bên trong.
    
    Trong một hệ thống Ebook2LaTeX nâng cao, bước này có thể dùng thêm mô hình 
    Layout Analysis (như LayoutLM) để phát hiện và cắt (crop) các vùng chứa 
    công thức toán từ trang PDF được render. 
    
    Trong phạm vi nền tảng này, chúng ta sẽ mô phỏng việc trích xuất bằng cách 
    lấy ra tất cả các hình ảnh được nhúng trong PDF (thường các công thức phức tạp 
    trong PDF scan hoặc ebook cũ được lưu dưới dạng ảnh).
    
    Args:
        pdf_path (str): Đường dẫn tuyệt đối đến file PDF trên server.
        
    Returns:
        list[Image.Image]: Danh sách các đối tượng PIL Image chứa công thức/hình ảnh.
    """
    extracted_images = []
    
    try:
        # Mở tài liệu PDF
        doc = fitz.open(pdf_path)
        logger.info(f"Đã mở PDF: {pdf_path} (Tổng số trang: {len(doc)})")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Lấy danh sách các object hình ảnh trên trang hiện tại
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                
                # Trích xuất dữ liệu byte của hình ảnh
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                try:
                    # Chuyển đổi byte array thành PIL Image để pix2tex dễ xử lý
                    img = Image.open(io.BytesIO(image_bytes))
                    
                    # Bộ lọc cơ bản: Bỏ qua các ảnh quá nhỏ (như icon, dot, separator)
                    if img.width >= 30 and img.height >= 30:
                        # Convert sang RGB vì pix2tex (dựa trên ViT) yêu cầu input RGB
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        extracted_images.append(img)
                        
                except Exception as img_err:
                    logger.warning(f"Bỏ qua ảnh lỗi tại trang {page_num}, xref {xref}: {img_err}")
                    
        doc.close()
        logger.info(f"Đã trích xuất thành công {len(extracted_images)} hình ảnh từ PDF.")
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý file PDF {pdf_path}: {e}")
        raise RuntimeError(f"Không thể xử lý PDF: {str(e)}")
        
    return extracted_images
