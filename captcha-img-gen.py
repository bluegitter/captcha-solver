from captcha.image import ImageCaptcha
import random
import string
import os

# 创建数据目录
output_dir = './data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化 ImageCaptcha 对象
image_captcha = ImageCaptcha(width=120, height=38)

# 生成随机字符串作为 CAPTCHA 文本
def generate_random_text(length=5):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

# 生成 10000 个 CAPTCHA 图像
for i in range(10000):
    # 生成随机文本
    text = generate_random_text()
    
    # 生成 CAPTCHA 图像
    image = image_captcha.generate_image(text)
    
    # 保存图像
    image_file_path = os.path.join(output_dir, f"{text}.jpeg")
    image.save(image_file_path, format='jpeg')
    
    # 每生成 1000 张图像，打印一次进度
    if i % 1000 == 0:
        print(f"Generated {i} images")

print("Generation completed.")
