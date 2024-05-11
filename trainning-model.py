import os
from PIL import Image
import numpy as np
from keras import Input, Model # 导入Keras模型, 和各种神经网络的层
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# 数据目录
data_dir = 'data'
image_size = (120, 38)  # 假设图像尺寸为50x200
characters = '0123456789abcdefghijklmnopqrstuvwxyz'  # 包括所有可能字符
num_classes = len(characters)

# 创建字符到索引的映射
char_to_index = {char: idx for idx, char in enumerate(characters)}
index_to_char = {idx: char for char, idx in char_to_index.items()}

# 读取图像和标签
def load_data(data_dir, image_size, num_classes):
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
            
            # 提取标签
            label = file_name.split('.')[0]
            label_array = [to_categorical(char_to_index[char], num_classes) for char in label]
            labels.append(label_array)
    
    images = np.array(images).reshape(-1, image_size[0], image_size[1], 1)
    labels = np.array(labels)
    return images, labels



# 模型定义
def build_model(input_shape, num_classes):
    model_input = Input(shape=input_shape)
    x = Conv2D(32, (3, 3), activation='relu')(model_input)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    
    # 对每个字符分别构建全连接层
    outputs = [Dense(num_classes, activation='softmax')(x) for _ in range(5)]

    model = Model(inputs=model_input, outputs=outputs)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

# 加载数据
data_x, data_y = load_data(data_dir, image_size, num_classes)
input_shape = data_x.shape[1:]

# 训练与测试集划分
x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2, random_state=42)

# 模型构建
model = build_model(input_shape, num_classes)

# 模型训练
model.fit(x_train, [y_train[:, i] for i in range(5)], epochs=5, batch_size=32, validation_split=0.2)

# 创建模型保存目录
model_save_dir = './model'
os.makedirs(model_save_dir, exist_ok=True)

# 保存模型
model_save_path = os.path.join(model_save_dir, 'captcha_model-v30000.h5')
model.save(model_save_path)
print(f'Model saved to {model_save_path}')
