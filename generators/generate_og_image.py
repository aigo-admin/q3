from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os

width, height = 1200, 630

# Base dark void
img = Image.new('RGB', (width, height), color='#040507')
draw = ImageDraw.Draw(img)

# Deep space particles & star dust
random.seed(1337)
for _ in range(160):
    x = random.randint(0, width)
    y = random.randint(0, height)
    bright = random.randint(70, 240)
    size = random.choice([1, 1, 1, 2, 2, 3])
    # Slight lime / cyan tint on some stars
    color = (bright, bright, bright)
    if random.random() < 0.2:
        color = (int(bright * 0.75), bright, int(bright * 0.3))
    draw.ellipse([x, y, x + size, y + size], fill=color)

# Subtle vignette / glow
glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
# Center lime beam
for r in range(450, 0, -15):
    alpha = int(22 * (1 - r / 450))
    glow_draw.ellipse([width//2 - r, height//2 - int(r*0.5) - 30, width//2 + r, height//2 + int(r*0.5) - 30], fill=(186, 236, 67, alpha))

glow = glow.filter(ImageFilter.GaussianBlur(50))
img.paste(Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB'))
draw = ImageDraw.Draw(img)

# Anamorphic horizontal streak
streak = Image.new('RGBA', (width, height), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(streak)
for x in range(width):
    dist = abs(x - width//2) / (width//2)
    alpha = max(0, int(180 * (1 - dist**1.4)))
    s_draw.line([(x, 305), (x, 305)], fill=(186, 236, 67, alpha), width=2)
    s_draw.line([(x, 304), (x, 306)], fill=(186, 236, 67, int(alpha*0.4)), width=1)
streak = streak.filter(ImageFilter.GaussianBlur(1.2))
img.paste(Image.alpha_composite(img.convert('RGBA'), streak).convert('RGB'))
draw = ImageDraw.Draw(img)

# Fonts
font_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_regular = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

f_badge = ImageFont.truetype(font_bold, 18)
f_title = ImageFont.truetype(font_bold, 78)
f_accent = ImageFont.truetype(font_bold, 78)
f_date = ImageFont.truetype(font_bold, 30)
f_meta = ImageFont.truetype(font_bold, 20)
f_links = ImageFont.truetype(font_regular, 18)

# 1. Top Logo
logo_path = 'sponsorship_brochure/assets/SecLeaf_Dark_BG.png'
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert('RGBA')
    logo.thumbnail((95, 95), Image.Resampling.LANCZOS)
    img.paste(logo, (width//2 - logo.width//2, 55), logo)

# 2. Pill Badge: FLAGSHIP CYBER OPERATIONS
badge_text = "FLAGSHIP CYBER OPERATIONS"
bbox = f_badge.getbbox(badge_text)
bw = bbox[2] - bbox[0]
bx1, by1 = width//2 - bw//2 - 18, 175
bx2, by2 = width//2 + bw//2 + 18, 207
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, fill=(18, 24, 34), outline=(186, 236, 67, 120), width=1)
draw.text((width//2 - bw//2, 180), badge_text, font=f_badge, fill=(186, 236, 67))

# 3. Main Title: "SECLEAF Q3 2027 CTF"
# Draw "SECLEAF " in White and "Q3 2027 CTF" in Lime
t1 = "SECLEAF "
t2 = "Q3 2027 CTF"
bbox1 = f_title.getbbox(t1)
bbox2 = f_accent.getbbox(t2)
w1 = bbox1[2] - bbox1[0]
w2 = bbox2[2] - bbox2[0]
total_w = w1 + w2
start_x = width//2 - total_w//2
draw.text((start_x, 245), t1, font=f_title, fill=(255, 255, 255))
draw.text((start_x + w1, 245), t2, font=f_accent, fill=(186, 236, 67))

# 4. Date & Time
date_text = "24 JULY 12:00 PM  –  25 JULY 12:00 PM IST"
d_box = f_date.getbbox(date_text)
dw = d_box[2] - d_box[0]
draw.text((width//2 - dw//2, 355), date_text, font=f_date, fill=(240, 243, 248))

# 5. Metadata line
meta_text = "24-HOUR GLOBAL COMPETITION  •  JEOPARDY FORMAT  •  OPEN WORLDWIDE"
m_box = f_meta.getbbox(meta_text)
mw = m_box[2] - m_box[0]
draw.text((width//2 - mw//2, 415), meta_text, font=f_meta, fill=(148, 163, 184))

# 6. Bottom Domain Badges: ctf.secleaf.xyz • q3.secleaf.xyz • ctf.secleaf.tech • q3.secleaf.tech
domains = "ctf.secleaf.xyz   •   q3.secleaf.xyz   •   ctf.secleaf.tech   •   q3.secleaf.tech"
dom_box = f_links.getbbox(domains)
dom_w = dom_box[2] - dom_box[0]
draw.line([(width//2 - 250, 480), (width//2 + 250, 480)], fill=(40, 48, 64), width=1)
draw.text((width//2 - dom_w//2, 505), domains, font=f_links, fill=(186, 236, 67))

# Save
img.save('og-image.png', format='PNG', quality=95)
print("Saved 1200x630 og-image.png successfully!")
