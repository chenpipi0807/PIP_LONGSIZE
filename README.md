## PIP 长边调整节点 PIP 长边调整节点

#### 简介 简介
PIP 长边调整节点是一个用于 ComfyUI 的自定义节点，它可以调整图像的大小，同时保持图像的宽高比。这个节点主要调整图像的最长边，使其符合指定的尺寸，同时相应地调整短边以保持原始宽高比。PIP 长边调整节点是一个用于 ComfyUI 的自定义节点，它可以调整图像的大小，同时保持图像的宽高比。这个节点主要调整图像的最长边，使其符合指定的尺寸，同时相应地调整短边以保持原始宽高比。

## 功能
- 调整图像大小，保持原始宽高比 调整图像大小，保持原始宽高比
- 支持批量处理图像 支持批量处理图像
- 提供三种压缩选项：无损输出、中档压缩、最小文件 提供三种压缩选项：无损输出、中档压缩、最小文件
- 默认将最长边调整为 996 像素 默认将最长边调整为 996 像素

## 安装
1. 确保您已经安装了 ComfyUI。 确保您已经安装了 ComfyUI。
2. 将此节点的文件夹复制到 ComfyUI 的  将此节点的文件夹复制到 ComfyUI 的 ``custom_nodes` 目录中。 目录中。
3. 安装所需的依赖： 安装所需的依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方法
1. 在 ComfyUI 中，您会看到一个名为 "PIP 长边调整" 的新节点。 在 ComfyUI 中，您会看到一个名为 "PIP 长边调整" 的新节点。
2. 将图像输入连接到此节点。 将图像输入连接到此节点。
3. 设置所需的最大尺寸（默认为 996）。 设置所需的最大尺寸（默认为 996）。
4. 选择压缩级别。 选择压缩级别。
5. 运行工作流程以获得调整大小后的图像。 运行工作流程以获得调整大小后的图像。

## 参数说明
- `image`：输入图像：输入图像
- `max_dimension`：最长边的目标尺寸（默认 996，范围 1-8192）：最长边的目标尺寸（默认 996，范围 1-8192）
- `compression`：压缩级别（无损输出、中档压缩、最小文件）：压缩级别（无损输出、中档压缩、最小文件）

## 注意事项
- 此节点使用 Lanczos 重采样算法进行图像调整，以保持较高的图像质量。 此节点使用 Lanczos 重采样算法进行图像调整，以保持较高的图像质量。
- 输出图像始终为 PNG 格式，以确保最佳质量。 输出图像始终为 PNG 格式，以确保最佳质量。

## 贡献
欢迎提出问题、建议或贡献代码来改进这个节点。欢迎提出问题、建议或贡献代码来改进这个节点。
