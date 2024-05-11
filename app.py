import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# 设置参数
image_size = (120, 38)  # 假设图像尺寸为120x38
characters = '0123456789abcdefghijklmnopqrstuvwxyz'  # 包括所有可能字符
num_classes = len(characters)

# 创建字符到索引的映射
index_to_char = {idx: char for idx, char in enumerate(characters)}

# 加载模型
model_path = './model/captcha_model-v30000.h5'
model = load_model(model_path)

# 读取单个图像并进行预处理
def preprocess_image(image, image_size):
    img = Image.open(image).convert('L')  # 转换为灰度图像
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0  # 归一化
    img_array = img_array.reshape(1, image_size[0], image_size[1], 1)  # 添加批次维度
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # 预处理图像
        img_array = preprocess_image(file, image_size)
        
        # 预测
        predictions = model.predict(img_array)
        predicted_labels = [np.argmax(predictions[i], axis=1) for i in range(5)]
        
        # 将预测标签转换回字符
        predicted_labels_chars = ''.join([index_to_char[idx] for idx in np.array(predicted_labels).flatten()])
        print({'predicted_label': predicted_labels_chars})
        return jsonify({'predicted_label': predicted_labels_chars})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
