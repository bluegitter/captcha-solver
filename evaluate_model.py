import os
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
from PIL import Image

# 数据目录
data_dir = 'data'
image_size = (120, 38)  # 假设图像尺寸为50x200
characters = '0123456789abcdefghijklmnopqrstuvwxyz'  # 包括所有可能字符
num_classes = len(characters)

# 创建字符到索引的映射
char_to_index = {char: idx for idx, char in enumerate(characters)}
index_to_char = {idx: char for char, idx in char_to_index.items()}

# 读取图像和标签
def load_data(data_dir, image_size, char_to_index, num_classes):
    images = []
    labels = []
    
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.jpeg'):
            # 加载图像
            img_path = os.path.join(data_dir, file_name)
            img = Image.open(img_path).convert('L')  # 转换为灰度图像
            img = img.resize(image_size)
            img_array = np.array(img) / 255.0  # 归一化
            images.append(img_array)
            
            # 提取标签并转换为独热编码
            label = file_name.split('.')[0]
            label_array = [to_categorical(char_to_index[char], num_classes) for char in label]
            labels.append(label_array)
    
    images = np.array(images).reshape(-1, image_size[0], image_size[1], 1)
    labels = np.array(labels)
    return images, labels

# 加载数据
data_x, data_y = load_data(data_dir, image_size, char_to_index, num_classes)

# 划分验证集
from sklearn.model_selection import train_test_split
_, x_test, _, y_test = train_test_split(data_x, data_y, test_size=0.2, random_state=42)

# 确保标签的形状与模型的输出对齐
y_test = [y_test[:, i] for i in range(5)]

# 加载模型
model_path = './model/captcha_model.h5'
model = load_model(model_path)

# 评估模型
results = model.evaluate(x_test, y_test)
print(f'Overall Test loss: {results[0]}')

# 打印每个输出的准确性
for i in range(1, 6):
    print(f'Accuracy of output {i}: {results[i]}')

# 预测示例并打印真实和预测的标签
predictions = model.predict(x_test[:5])
predicted_labels = [np.argmax(predictions[i], axis=1) for i in range(5)]

# 将预测标签和真实标签转换回字符
predicted_labels_chars = [''.join([index_to_char[idx] for idx in pred]) for pred in np.array(predicted_labels).T]
true_labels_chars = [''.join([index_to_char[np.argmax(y_test[i][j])] for j in range(5)]) for i in range(5)]

print(f'Predicted labels: {predicted_labels_chars}')
print(f'True labels: {true_labels_chars}')
