from PIL import Image, ImageDraw, ImageFont

# 画像サイズと背景色を設定する
width, height = 200, 50
background_color = (255, 255, 255)

# 画像を生成する
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# フォントを設定する
font_size = 40
font = ImageFont.truetype('learn/num_only.ttf', font_size)

print(font.getbbox("0"))

# 文字を描画する
text = '1234'
new_box = draw.textbbox((0, 0), text, font)
text_width = new_box[2] - new_box[0]  # bottom-top
text_height = new_box[3] - new_box[1]  # right-left
x = width - text_width - 5  # 右揃えにする
y = (height - text_height) / 2
spacing = -1000
draw.text((x, y), text, fill=(0, 0, 0), font=font, spacing=spacing)

# 画像を保存する
image.save('learn/image-5.png')