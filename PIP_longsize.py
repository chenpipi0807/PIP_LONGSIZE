import torch
from PIL import Image
import numpy as np
import io

class PIP_longsize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "max_dimension": ("INT", {
                    "default": 996,
                    "min": 1,
                    "max": 8192,
                    "step": 1
                }),
                "compression": (["无损输出", "中档压缩", "最小文件"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width_int", "height_int")
    FUNCTION = "resize_image"
    CATEGORY = "图像处理"

    def resize_image(self, image, max_dimension, compression):
        # 确保图像是正确的维度 (batch_size, height, width, channels)
        if image.dim() == 3:
            image = image.unsqueeze(0)  # 添加批次维度

        batch_size, height, width, channels = image.shape
        # 1. 获取图像的宽和高

        # 2. 比较原始宽高数值，取最长边数值
        longest_side = max(width, height)

        # 3. 计算原始图像宽高比例
        aspect_ratio = width / height

        # 4. 根据用户输入的新的最长边的数值
        new_longest_side = max_dimension

        # 5. 根据新的最长边计算新的宽和高
        if width >= height:
            new_width = new_longest_side
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = new_longest_side
            new_width = int(new_height * aspect_ratio)

        # 6. 确保新的宽和高都是整数
        new_width = int(new_width)
        new_height = int(new_height)

        # 设置压缩级别
        compression_level = {"无损输出": 0, "中档压缩": 4, "最小文件": 9}[compression]

        # 调整图像大小
        resized_images = []
        for i in range(batch_size):
            img = image[i]
            
            # 处理输入图像
            
            # 确保图像数据在0-1范围内
            img = img.float() / 255.0 if img.dtype == torch.uint8 else img.float()
            img = torch.clamp(img, 0, 1)
            
            # 转换为PIL图像
            img_np = (img.cpu().numpy() * 255).astype(np.uint8)
            img_pil = Image.fromarray(img_np, mode='RGB')
            
            # 调整大小
            resized_pil = img_pil.resize((new_width, new_height), Image.LANCZOS)
            
            # 将PIL图像保存为PNG格式的字节流
            buffer = io.BytesIO()
            resized_pil.save(buffer, format="PNG", compress_level=compression_level)
            buffer.seek(0)
            
            # 从字节流中读取PNG图像
            png_image = Image.open(buffer)
            
            # 转回PyTorch张量，保持原始的维度顺序
            resized_np = np.array(png_image).astype(np.float32) / 255.0
            resized_tensor = torch.from_numpy(resized_np)
            
            # 处理完成
            
            resized_images.append(resized_tensor)

        resized_image_batch = torch.stack(resized_images, dim=0)

        # 返回处理后的图像和尺寸

        return (resized_image_batch, new_width, new_height)

class PIP_ProportionalCrop:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "aspect_ratio": (["1:1", "4:3", "3:4", "16:9", "9:16", "2:1", "1:2", "3:2", "2:3", "5:4", "4:5", "21:9", "9:21", "1:1.41 (A系列)", "1.41:1 (A系列)", "1:1.618 (黄金比例)", "1.618:1 (黄金比例)"],),
                "maintain_direction": (["中心", "上", "下", "左", "右"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width_int", "height_int")
    FUNCTION = "crop_image"
    CATEGORY = "图像处理"

    def crop_image(self, image, aspect_ratio, maintain_direction):
        # 确保图像是正确的维度 (batch_size, height, width, channels)
        if image.dim() == 3:
            image = image.unsqueeze(0)  # 添加批次维度

        batch_size, height, width, channels = image.shape
        print(f"输入图像尺寸: {image.shape}")  # 调试信息

        # 1. 获取图像的宽和高
        print(f"原始图像尺寸: 宽={width}, 高={height}")

        # 2. 解析目标宽高比例
        aspect_map = {
            "1:1": 1.0,
            "4:3": 4/3,
            "3:4": 3/4,
            "16:9": 16/9,
            "9:16": 9/16,
            "2:1": 2.0,
            "1:2": 0.5,
            "3:2": 3/2,
            "2:3": 2/3,
            "5:4": 5/4,
            "4:5": 4/5,
            "21:9": 21/9,
            "9:21": 9/21,
            "1:1.41 (A系列)": 1/1.41,
            "1.41:1 (A系列)": 1.41,
            "1:1.618 (黄金比例)": 1/1.618,
            "1.618:1 (黄金比例)": 1.618
        }
        target_ratio = aspect_map[aspect_ratio]

        # 3. 计算裁切区域的尺寸
        current_ratio = width / height
        
        if target_ratio > current_ratio:
            # 目标比例比当前比例宽，需要减少高度
            new_height = int(width / target_ratio)
            new_width = width
        else:
            # 目标比例比当前比例窄，需要减少宽度
            new_width = int(height * target_ratio)
            new_height = height
            
        # 计算裁切后的尺寸
        
        # 4. 计算裁切的起始位置
        x_start = 0
        y_start = 0
        
        if new_width < width:
            # 需要在水平方向裁切
            if maintain_direction == "左":
                x_start = 0
            elif maintain_direction == "右":
                x_start = width - new_width
            else:  # 中心、上、下
                x_start = (width - new_width) // 2
                
        if new_height < height:
            # 需要在垂直方向裁切
            if maintain_direction == "上":
                y_start = 0
            elif maintain_direction == "下":
                y_start = height - new_height
            else:  # 中心、左、右
                y_start = (height - new_height) // 2
                
        # 确定裁切起始位置

        # 5. 裁切图像
        cropped_images = []
        for i in range(batch_size):
            img = image[i]
            # 裁切图像
            cropped = img[y_start:y_start+new_height, x_start:x_start+new_width, :]
            cropped_images.append(cropped)

        # 6. 将裁切后的图像组合成批次
        cropped_batch = torch.stack(cropped_images, dim=0)
        
        # 准备返回裁切后的图像
        
        return (cropped_batch, new_width, new_height)

# 包含所有要导出的节点的字典，以及它们的名称
NODE_CLASS_MAPPINGS = {
    "PIP_longsize": PIP_longsize,
    "PIP_ProportionalCrop": PIP_ProportionalCrop
}

# 包含节点的友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_longsize": "PIP 长边调整",
    "PIP_ProportionalCrop": "PIP 等比例裁切"
}
