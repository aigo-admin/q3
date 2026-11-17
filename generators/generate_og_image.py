from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os

width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#040507')
draw = ImageDraw.Draw(img)

# Deep space particles & star dust
random.seed(2027)
for _ in range(180):
    x = random.randint(0, width)
    y = random.randint(0, height)
    bright = random.randint(60, 240)
    size = random.choice([1, 1, 1, 2, 2, 3])
    color = (bright, bright, bright)
    if random.random() < 0.22:
        color = (int(bright * 0.72), bright, int(bright * 0.28))
    draw.ellipse([x, y, x + size, y + size], fill=color)

# Ethereal center electric-lime cinematic glow
glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
for r in range(480, 0, -16):
    alpha = int(24 * (1 - r / 480))
    glow_draw.ellipse(
        [width//2 - r, height//2 - int(r*0.55), width//2 + r, height//2 + int(r*0.55)],
        fill=(186, 236, 67, alpha)
    )
glow = glow.filter(ImageFilter.GaussianBlur(60))
img.paste(Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB'))
draw = ImageDraw.Draw(img)

# Subtle anamorphic horizontal streak
streak = Image.new('RGBA', (width, height), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(streak)
for x in range(width):
    dist = abs(x - width//2) / (width//2)
    alpha = max(0, int(140 * (1 - dist**1.3)))
    s_draw.line([(x, 340), (x, 340)], fill=(186, 236, 67, alpha), width=2)
    s_draw.line([(x, 339), (x, 341)], fill=(186, 236, 67, int(alpha * 0.35)), width=1)
streak = streak.filter(ImageFilter.GaussianBlur(1.4))
img.paste(Image.alpha_composite(img.convert('RGBA'), streak).convert('RGB'))
draw = ImageDraw.Draw(img)

# 1. LOGO: Official illuminated cyber-leaf emblem
logo_raw = None
candidates = [
    'Q3/planning/assets/SecLeaf_Dark_BG.png',
    'sponsorship_brochure/assets/SecLeaf_Dark_BG.png',
    'Q3/planning/brochure/assets/SecLeaf_Dark_BG.png'
]
for cp in candidates:
    if os.path.exists(cp):
        logo_raw = Image.open(cp).convert('RGBA')
        break

if logo_raw:
    emblem = logo_raw.crop((0, 0, logo_raw.width, 1640))
    emblem = emblem.crop(emblem.getbbox())
    emblem.thumbnail((125, 125), Image.Resampling.LANCZOS)
    img.paste(emblem, (width//2 - emblem.width//2, 55), emblem)

# Fonts
font_bold = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
f_brand = ImageFont.truetype(font_bold, 38)
f_title = ImageFont.truetype(font_bold, 92)
f_date = ImageFont.truetype(font_bold, 36)

# 2. BRAND: "SecLeaf" ('Sec' in White, 'Leaf' in Electric Lime)
sec_w = f_brand.getbbox('Sec')[2] - f_brand.getbbox('Sec')[0]
leaf_w = f_brand.getbbox('Leaf')[2] - f_brand.getbbox('Leaf')[0]
brand_w = sec_w + leaf_w
bx = width//2 - brand_w//2
draw.text((bx, 195), 'Sec', font=f_brand, fill=(255, 255, 255))
draw.text((bx + sec_w, 195), 'Leaf', font=f_brand, fill=(186, 236, 67))

# 3. TITLE: "Q3 2027 CTF"
t = 'Q3 2027 CTF'
t_box = f_title.getbbox(t)
tw = t_box[2] - t_box[0]
draw.text((width//2 - tw//2 + 2, 282), t, font=f_title, fill=(10, 15, 20))
draw.text((width//2 - tw//2, 280), t, font=f_title, fill=(186, 236, 67))

# 4. DATE: "24 & 25 JULY 2027"
d = '24 & 25 JULY 2027'
d_box = f_date.getbbox(d)
dw = d_box[2] - d_box[0]

pill_pad_x = 32
pill_pad_y = 14
px1 = width//2 - dw//2 - pill_pad_x
py1 = 430
px2 = width//2 + dw//2 + pill_pad_x
py2 = py1 + (d_box[3] - d_box[1]) + pill_pad_y * 2

draw.rounded_rectangle([px1, py1, px2, py2], radius=26, fill=(14, 20, 30), outline=(51, 65, 85), width=1)
draw.text((width//2 - dw//2, py1 + pill_pad_y - 2), d, font=f_date, fill=(241, 245, 249))

# Save
output_path = 'Q3/og-image.png'
img.save(output_path, format='PNG', quality=95)
print(f"Saved {output_path} successfully!")
