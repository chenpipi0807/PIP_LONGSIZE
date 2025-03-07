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
        print(f"输入图像尺寸: {image.shape}")  # 调试信息

        # 1. 获取图像的宽和高
        print(f"原始图像尺寸: 宽={width}, 高={height}")

        # 2. 比较原始宽高数值，取最长边数值
        longest_side = max(width, height)
        print(f"最长边: {longest_side}")

        # 3. 计算原始图像宽高比例
        aspect_ratio = width / height
        print(f"原始宽高比: {aspect_ratio:.4f}")

        # 4. 根据用户输入的新的最长边的数值
        new_longest_side = max_dimension
        print(f"新的最长边: {new_longest_side}")

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
        print(f"调整后的图像尺寸: {new_width}x{new_height}")

        # 设置压缩级别
        compression_level = {"无损输出": 0, "中档压缩": 4, "最小文件": 9}[compression]

        # 调整图像大小
        resized_images = []
        for i in range(batch_size):
            img = image[i]
            
            # 打印输入图像的一些像素值
            print(f"输入图像的一些像素值: {img[0:5, 0:5, :]}")
            
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
            
            # 打印输出图像的一些像素值
            print(f"输出图像的一些像素值: {resized_tensor[0:5, 0:5, :]}")
            
            resized_images.append(resized_tensor)

        resized_image_batch = torch.stack(resized_images, dim=0)

        print(f"最终输出图像尺寸: {resized_image_batch.shape}")  # 调试信息
        print(f"输出图像的数据类型: {resized_image_batch.dtype}")
        print(f"输出图像的值范围: [{resized_image_batch.min()}, {resized_image_batch.max()}]")

        return (resized_image_batch, new_width, new_height)

# 包含所有要导出的节点的字典，以及它们的名称
NODE_CLASS_MAPPINGS = {
    "PIP_longsize": PIP_longsize
}

# 包含节点的友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_longsize": "PIP 长边调整"
}
