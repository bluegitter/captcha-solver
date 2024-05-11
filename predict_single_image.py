import os
import numpy as np
from keras.models import load_model
from PIL import Image

# 数据目录和文件名
file_path = '/Users/yanfei/Downloads/code.jpeg'
image_size = (120, 38)  # 假设图像尺寸为50x200
characters = '0123456789abcdefghijklmnopqrstuvwxyz'  # 包括所有可能字符
num_classes = len(characters)

# 创建字符到索引的映射
index_to_char = {idx: char for idx, char in enumerate(characters)}

# 读取单个图像
def load_single_image(file_path, image_size):
    img = Image.open(file_path).convert('L')  # 转换为灰度图像
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0  # 归一化
    img_array = img_array.reshape(1, image_size[0], image_size[1], 1)  # 添加批次维度
    return img_array

# 加载图像
x_test = load_single_image(file_path, image_size)

print(x_test)
# 加载模型
model_path = './model/captcha_model-v30000.h5'
model = load_model(model_path)

# 预测
predictions = model.predict(x_test)
predicted_labels = [np.argmax(predictions[i], axis=1) for i in range(5)]

# 将预测标签转换回字符
predicted_labels_chars = ''.join([index_to_char[idx] for idx in np.array(predicted_labels).flatten()])

print(f'Predicted label: {predicted_labels_chars}')
