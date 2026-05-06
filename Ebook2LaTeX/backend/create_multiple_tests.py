import os
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

# Danh sách các công thức toán học đa dạng để test
formulas = [
    r"$E = mc^2$",
    r"$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
    r"$a^2 + b^2 = c^2$",
    r"$e^{i\pi} + 1 = 0$",
    r"$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$",
    r"$\lim_{x \to 0} \frac{\sin x}{x} = 1$",
    r"$\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}$",
    r"$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$",
    r"$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$",
    r"$\sin^2 \theta + \cos^2 \theta = 1$",
    r"$A = \pi r^2$",
    r"$\frac{d}{dx} e^x = e^x$",
    r"$V = \frac{4}{3}\pi r^3$",
    r"$\det(A - \lambda I) = 0$",
    r"$\oint_C \mathbf{B} \cdot d\mathbf{l} = \mu_0 I$"
]

def create_pdf_with_formulas(filename, start_idx, end_idx):
    output_path = rf"D:\Dich-vu-web-DLU\Ebook2LaTeX\{filename}"
    c = canvas.Canvas(output_path)
    c.drawString(100, 800, f"File Test OCR: {filename}")
    
    y_pos = 730
    for i in range(start_idx, end_idx):
        if i >= len(formulas):
            break
            
        formula = formulas[i]
        temp_img = f"temp_formula_{i}.png"
        
        # Vẽ công thức thành ảnh
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.text(0.5, 0.5, formula, size=20, ha='center', va='center')
        ax.axis('off')
        plt.savefig(temp_img, bbox_inches='tight', dpi=300)
        plt.close()
        
        # Chèn vào PDF
        c.drawString(100, y_pos + 10, f"Cong thuc #{i + 1}:")
        c.drawImage(temp_img, 100, y_pos - 80, height=80, preserveAspectRatio=True)
        y_pos -= 130
        
        # Xóa file ảnh tạm
        os.remove(temp_img)
        
    c.save()
    print(f"Da tao thanh cong: {output_path}")

# Tạo 3 file PDF, mỗi file 5 công thức
create_pdf_with_formulas("test_math_set1.pdf", 0, 5)
create_pdf_with_formulas("test_math_set2.pdf", 5, 10)
create_pdf_with_formulas("test_math_set3.pdf", 10, 15)

print("Hoan thanh tao tat ca cac file test!")
