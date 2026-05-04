"""
OCR Service using pix2tex for Math Formula extraction.
"""
import logging
from typing import List
from PIL import Image

# Cố gắng import LatexOCR, nếu lỗi thì bắt ngay để không sập app toàn cục
try:
    from pix2tex.cli import LatexOCR
except ImportError:
    LatexOCR = None

logger = logging.getLogger(__name__)

# Áp dụng mẫu Singleton (Singleton pattern) để lưu trữ mô hình.
# Tránh việc khởi tạo lại mô hình AI nặng nề trên mỗi request.
_model_instance = None


def get_ocr_model():
    """
    Hàm lấy instance của mô hình LatexOCR. Tải mô hình vào RAM lần đầu tiên được gọi.
    """
    global _model_instance
    if _model_instance is None:
        if LatexOCR is None:
            raise RuntimeError("Thư viện 'pix2tex' chưa được cài đặt hoặc lỗi import. Vui lòng kiểm tra requirements.")
            
        logger.info("Đang nạp mô hình pix2tex LatexOCR vào bộ nhớ... (Có thể mất chút thời gian)")
        # Khởi tạo mô hình (model sẽ tự load weights từ local hoặc tải về nếu chưa có)
        _model_instance = LatexOCR()
        logger.info("Nạp mô hình pix2tex LatexOCR thành công!")
        
    return _model_instance


def extract_latex_from_images(images: List[Image.Image]) -> List[str]:
    """
    Đưa một danh sách hình ảnh (chứa công thức) qua mô hình OCR và trả về mảng LaTeX.
    
    Args:
        images (List[Image.Image]): Danh sách các PIL Image (đã được chuyển thành RGB).
        
    Returns:
        List[str]: Danh sách các chuỗi raw LaTeX tương ứng. Trả về chuỗi rỗng nếu có lỗi.
    """
    if not images:
        return []
        
    model = get_ocr_model()
    results = []
    
    for idx, img in enumerate(images):
        try:
            # Chạy mô hình suy luận (inference) trên từng tấm ảnh
            latex_code = model(img)
            results.append(latex_code)
        except Exception as e:
            logger.error(f"Lỗi khi chạy suy luận OCR trên hình ảnh thứ {idx}: {e}")
            # Nếu một ảnh bị lỗi (chất lượng quá thấp, out of memory...), 
            # chúng ta vẫn append chuỗi rỗng để không làm hỏng mảng thứ tự.
            results.append("")
            
    return results
