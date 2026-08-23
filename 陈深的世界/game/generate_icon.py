# 生成应用图标 app.ico（暗紫底 + 金色月牙）
import os
from PIL import Image, ImageDraw

root = os.path.dirname(os.path.abspath(__file__))
sizes = [16, 24, 32, 48, 64, 128, 256]
imgs = []
for s in sizes:
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # 圆形底
    d.ellipse([0, 0, s-1, s-1], fill=(20, 14, 40, 255), outline=(201, 179, 126, 255), width=max(1, s//32))
    # 月牙
    r = s * 0.26
    cx, cy = s * 0.5, s * 0.5
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(244, 215, 138, 255))
    # 用小圆切出月牙
    d.ellipse([cx-r*0.42, cy-r*0.55, cx+r*0.85, cy+r*0.85], fill=(20, 14, 40, 255))
    imgs.append(im)

out = os.path.join(root, 'app.ico')
imgs[0].save(out, format='ICO', sizes=[(s, s) for s in sizes])
print('icon written:', out)
