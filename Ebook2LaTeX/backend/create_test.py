import os
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

output_path = r"D:\Dich-vu-web-DLU\Ebook2LaTeX\test_math.pdf"
temp_img = "temp_formula.png"

# Tạo ảnh chứa công thức toán học bằng matplotlib
fig, ax = plt.subplots(figsize=(4, 1))
formula = r"$f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$"
ax.text(0.5, 0.5, formula, size=20, ha='center', va='center')
ax.axis('off')
plt.savefig(temp_img, bbox_inches='tight', dpi=300)
plt.close()

# Tạo PDF và chèn ảnh vào
c = canvas.Canvas(output_path)
c.drawString(100, 800, "Day la file PDF test chua cong thuc toan hoc")

c.drawString(100, 750, "Cong thuc so 1 (Tich phan Gauss):")
c.drawImage(temp_img, 100, 680, width=300, preserveAspectRatio=True)

c.save()
os.remove(temp_img)
print(f"Da tao thanh cong file test tai: {output_path}")
