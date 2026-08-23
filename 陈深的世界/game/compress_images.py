# 图片压缩优化：把所有图片压到适合网页游戏的体积，显著缩小 EXE。
# 规则：长边>1800 缩到 1800；JPEG 质量 75；PNG 重新优化；原文件名保留。
import os, sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # 允许大图

root = os.path.dirname(os.path.abspath(__file__))
targets = [os.path.join(root, 'photos'), os.path.join(root, 'assets')]
MAX_SIDE = 1800
JQ = 75

def process(p):
    ext = os.path.splitext(p)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
        return None
    before = os.path.getsize(p)
    try:
        im = Image.open(p)
        im.load()
    except Exception as e:
        print('SKIP(open fail)', p, e)
        return None
    # 转 RGB（去 alpha 用于 jpg；png 保留）
    has_alpha = (im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info)
    if ext in ('.jpg', '.jpeg'):
        im = im.convert('RGB')
    # 缩放长边
    w, h = im.size
    if max(w, h) > MAX_SIDE:
        ratio = MAX_SIDE / float(max(w, h))
        im = im.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    # 保存
    try:
        if ext in ('.jpg', '.jpeg'):
            im.save(p, 'JPEG', quality=JQ, optimize=True, progressive=True)
        elif ext == '.png':
            im.save(p, 'PNG', optimize=True)
        elif ext == '.webp':
            im.save(p, 'WEBP', quality=JQ)
    except Exception as e:
        print('SKIP(save fail)', p, e)
        return None
    after = os.path.getsize(p)
    return (before, after)

total_before = 0
total_after = 0
count = 0
for t in targets:
    if not os.path.isdir(t):
        continue
    for fn in sorted(os.listdir(t)):
        p = os.path.join(t, fn)
        if not os.path.isfile(p):
            continue
        r = process(p)
        if r:
            count += 1
            total_before += r[0]
            total_after += r[1]
print('COMPRESSED files=%d before=%.1fMB after=%.1fMB saved=%.1fMB (%.0f%%)' % (
    count, total_before/1048576, total_after/1048576, (total_before-total_after)/1048576,
    100*(1-total_after/max(total_before,1))))
