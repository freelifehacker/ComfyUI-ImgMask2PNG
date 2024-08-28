from PIL import Image


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

    def remove_background(self, mask, image):

        # 确保图像和掩码的尺寸相同
        if image.size != mask.size:
            raise ValueError("Image and mask must have the same dimensions")

        # 将掩码应用到图像上
        image = image.convert("RGBA")
        mask = mask.convert("L")  # 转换掩码为灰度图
        output_image = Image.new("RGBA", image.size)
        output_image.paste(image, (0, 0), mask)

        # 返回处理后的图像
        return output_image


NODE_CLASS_MAPPINGS = {
    "ImageMask2PNG": ImageMask2PNG,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageMask2PNG": "🌊ImageMask2PNG",
}
