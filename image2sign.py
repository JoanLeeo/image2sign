from itertools import product
from PIL import Image, ImageEnhance
import sys
import os

def adjust_image(image_path, factors):
    image = Image.open(image_path)
    brightness_factor = factors[0]
    contrast_factor = factors[1]
    sharpness_factor = factors[2]
    color_factor = factors[3]
    # 调整曝光
    # 此类可以用于控制图像的亮度。一增强因子为0.0会产生黑色图像。系数1.0给出原始图像。
    # 0 - ∞
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)  # 将曝光设置到最高

    # 调整对比度
    # 此类可用于控制图像的对比度，类似于
    # 到电视机上的对比度控制。增强因子0.0
    # 给出了一个实心的灰色图像。系数为1.0时会生成原始图像。
    # 0 - ∞
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)  # 将对比度设置到60%

    # 调整清晰度
    # 此类可用于调整图像的清晰度。一
    # 增强因子0.0表示模糊图像，因子1.0表示原始图像，因子2.0表示锐化图像。
    # 0 - ∞  通常建议在0到2之间进行调整
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness_factor)  # 将阴影设置到最高

    # 调整饱和度此类可用于调整图像的颜色平衡，在
    # 其方式类似于彩色电视机上的控制。增强功能
    # 因数0.0给出一个黑白图像。系数1.0给出原始图像。
    # 0 - ∞

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(color_factor)  # 将饱和度设置到最低

    # 处理图片：将图片变透明
    image = remove_background(image)
    image = crop_image(image)

    # # 保存图片
    return image

# 遍历 调整图片的 Brightness，Contrast， Sharpness 和 Color。将图片保存到画布上并且显示出来。
def adjust_image_properties(image_path, save_floder=None):

    brightness_factors = [2.4, 2.5, 2.6, 2.7]
    contrast_factors = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    sharpness_factors = [2]
    color_factors = [0]

    # 组合
    combinations = list(product(brightness_factors, contrast_factors, sharpness_factors, color_factors))
    # 保存路径
    # 如果 有save_floder，在save_floder文件夹下穿件export_sign文件夹，如果没有保存到当前文件夹下创建export_sign文件夹

    if save_floder:
        os.makedirs(save_floder, exist_ok=True)
        save_floder = os.path.join(save_floder, "export_sign")
        os.makedirs(save_floder, exist_ok=True)
    else:
        save_floder = os.path.join(os.getcwd(), "export_sign")
        os.makedirs(save_floder, exist_ok=True)

    for i, combination in enumerate(combinations):
        image = adjust_image(image_path, combination)
        image.save(f"{save_floder}/{combination[0]}_{combination[1]}_{combination[2]}_{combination[3]}.png")
        # 在终端输出进度，取整

        progress = f"{(i+1)/len(combinations) * 100:.0f}%"
        print(f"进度: {progress}")
    print("完成。请选择一个你认为合适的签名图片")
    print("导出位置：", save_floder)



# 处理图片：将图片变透明,输入的图片是jpg格式的。将白色的部分设置为透明，其他不变
def remove_background(img):
    img = img.convert("RGBA")
    width, height = img.size
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:  # 判断像素点是否接近白色
                img.putpixel((x, y), (255, 255, 255, 0))  # 将该像素点设置为透明
    return img


# 剪切图片：将图片周围是空白的区域剪切掉，只留有内容的部分，比如，白色，或者透明色是无内容的了减掉。
# 在 remove_background 后 调用
def crop_image(image):
    image_data = image.load()
    width, height = image.size
    left = width
    top = height
    right = 0
    bottom = 0

    for y in range(height):
        for x in range(width):
            pixel = image_data[x, y]
            if len(pixel) > 3 and pixel[3] != 0:  # 检查透明度值是否不为0
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if left < right and top < bottom:
        # 找到包含内容的区域，进行剪切操作
        cropped_image = image.crop((left, top, right + 1, bottom + 1))
        return cropped_image
    return None



if __name__ == '__main__':
    # 在终端运行 获取参数
    # 图片路径
    image_path = sys.argv[1]
    # 保存路径 是可选的
    save_folder = sys.argv[2] if len(sys.argv) > 2 else None
    adjust_image_properties(image_path, save_folder)
