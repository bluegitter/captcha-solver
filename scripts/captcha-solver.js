// ==UserScript==
// @name         CAPTCHA Solver
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Solve CAPTCHA and autofill the result
// @author       Your Name
// @match        *://192.168.63.56:9090/*
// @require      https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 等待页面加载完成
    $(document).ready(function() {
        // 定义验证码图片和输入框的选择器
        const imgSelector = '.login-code-img';
        const inputSelector = 'input.el-input__inner[placeholder="请输入验证码"]';

        // 获取验证码图片的 Blob 数据
        function getCaptchaImage() {
            const img = $(imgSelector)[0];
            if (img) {
                // 创建一个 Canvas 元素
                const canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                const ctx = canvas.getContext('2d');

                // 将图像绘制到 Canvas 上
                ctx.drawImage(img, 0, 0);

                return new Promise((resolve, reject) => {
                    // 将 Canvas 内容转换为 Blob
                    canvas.toBlob(blob => {
                        if (blob) {
                            resolve(new File([blob], 'captcha.jpeg', { type: 'image/jpeg' }));
                        } else {
                            reject('Canvas to Blob conversion failed');
                        }
                    }, 'image/jpeg');
                });
            } else {
                return Promise.reject('Captcha image not found');
            }
        }

        // 调用 Flask 服务器的预测接口
        function predictCaptcha(imageFile) {
            const formData = new FormData();
            formData.append('file', imageFile);
            return $.ajax({
                url: 'http://localhost:5000/predict',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false
            });
        }

        // 手动触发 Vue.js 输入框的 input 事件
        function triggerVueInput(element, value) {
            const inputEvent = new Event('input', { bubbles: true });
            element.value = value;
            element.dispatchEvent(inputEvent);
        }

        // 自动填写验证码
        function autofillCaptcha() {
            getCaptchaImage().then(imageFile => {
                predictCaptcha(imageFile).then(response => {
                    if (response.predicted_label) {
                        const inputElement = document.querySelector(inputSelector);
                        if (inputElement) {
                            triggerVueInput(inputElement, response.predicted_label);
                        } else {
                            console.error('Input element not found');
                        }
                    } else {
                        console.error('Prediction failed:', response);
                    }
                }).catch(error => {
                    console.error('Error in prediction:', error);
                });
            }).catch(error => {
                console.error('Error in getting captcha image:', error);
            });
        }

        // 延迟执行验证码识别和填充
        setTimeout(() => {
            // 监听验证码图片的加载事件
            $(imgSelector).on('load', autofillCaptcha);

            // 初始调用
            autofillCaptcha();
        }, 3000); // 等待3秒
    });
})();
