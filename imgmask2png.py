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

    def tensor_to_pil(self, tensor):
        # 移除批次维度和通道维度
        if tensor.ndim == 4:
            tensor = tensor.squeeze(0).squeeze(0)
        elif tensor.ndim == 3:
            tensor = tensor.squeeze(0)

        # 确保张量在 [0, 255] 范围内
        tensor = tensor.mul(255).byte()

        # 将张量转换为 numpy 数组
        array = tensor.numpy()

        # 将 numpy 数组转换为 PIL 图像
        return Image.fromarray(array)

    def remove_background(self, mask, image):
        # 如果输入是 torch.Tensor，则将其转换为 PIL.Image
        if isinstance(image, torch.Tensor):
            image = self.tensor_to_pil(image)
        if isinstance(mask, torch.Tensor):
            mask = self.tensor_to_pil(mask)

        # 打印图像和掩码的尺寸以进行调试
        print(f"Image size: {image.size}")
        print(f"Mask size: {mask.size}")

        # 确保图像和掩码的尺寸相同
        if image.size != mask.size:
            print("Resizing mask to match image size")
            mask = mask.resize(image.size, Image.LANCZOS)

        # 将掩码应用到图像上
        image = image.convert("RGBA")
        mask = mask.convert("L")  # 转换掩码为灰度图
        output_image = Image.new("RGBA", image.size)
        output_image.paste(image, (0, 0), mask)

        # 返回处理后的图像
        return (output_image,)


NODE_CLASS_MAPPINGS = {
    "ImageMask2PNG": ImageMask2PNG,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageMask2PNG": "🌊ImageMask2PNG",
}
