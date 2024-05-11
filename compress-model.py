import os
import gzip
import shutil
from keras.models import load_model

# 加载模型
model_path = './model/captcha_model-v30000.h5'
model = load_model(model_path)

# 保存原始模型
model_save_path = os.path.join('./model', 'captcha_model-v30000.h5')


# 压缩模型文件
compressed_model_save_path = model_save_path + '.gz'
with open(model_save_path, 'rb') as f_in:
    with gzip.open(compressed_model_save_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f'Compressed model saved to {compressed_model_save_path}')
