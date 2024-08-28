from PIL import Image
import torch
import numpy as np


class ImageMask2PNG:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "remove_background"
    CATEGORY = "🌊ImageMask2PNG"

    def tensor_to_numpy(self, tensor):
        # 移除批次维度和通道维度
        if tensor.ndim == 4:
            tensor = tensor.squeeze(0)
        elif tensor.ndim == 3:
            tensor = tensor.squeeze(0)

        # 确保张量在 [0, 255] 范围内
        tensor = tensor.mul(255).byte()

        # 将张量转换为 numpy 数组
        array = tensor.numpy()

        return array

    def numpy_to_tensor(self, array):
        # 将 NumPy 数组转换为 PyTorch 张量
        tensor = torch.from_numpy(array).float().div(255)

        # 调整张量形状为 (batch_size, channels, height, width)
        if tensor.ndim == 3:
            tensor = tensor.permute(2, 0, 1).unsqueeze(0)
        elif tensor.ndim == 2:
            tensor = tensor.unsqueeze(0).unsqueeze(0)

        return tensor

    def remove_background(self, mask, image):
        # 如果输入是 torch.Tensor，则将其转换为 NumPy 数组
        if isinstance(image, torch.Tensor):
            image = self.tensor_to_numpy(image)
        if isinstance(mask, torch.Tensor):
            mask = self.tensor_to_numpy(mask)

        # 打印图像和掩码的尺寸以进行调试
        print(f"Image shape: {image.shape}")
        print(f"Mask shape: {mask.shape}")

        # 确保图像和掩码的尺寸相同
        if image.shape[:2] != mask.shape[:2]:
            print("Resizing mask to match image size")
            mask = np.array(
                Image.fromarray(mask).resize(image.shape[1::-1], Image.LANCZOS)
            )

        # 将掩码应用到图像上
        image = Image.fromarray(image).convert("RGBA")
        mask = Image.fromarray(mask).convert("L")  # 转换掩码为灰度图
        output_image = Image.new("RGBA", image.size)
        output_image.paste(image, (0, 0), mask)

        # 将处理后的图像转换为 NumPy 数组
        output_image_array = np.array(output_image)

        # 将处理后的图像转换为 PyTorch 张量
        output_image_tensor = self.numpy_to_tensor(output_image_array)

        # 返回处理后的图像
        return (output_image_tensor,)


NODE_CLASS_MAPPINGS = {
    "ImageMask2PNG": ImageMask2PNG,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageMask2PNG": "🌊ImageMask2PNG",
}
