from PIL import Image, ImageDraw, ImageFont

def draw_guides(image: Image.Image) -> Image.Image:
    """
    在输入的PIL图片上绘制辅助线和刻度。

    参数:
    image (PIL.Image.Image): 输入的PIL图片对象。

    返回:
    PIL.Image.Image: 带有辅助线和刻度的PIL图片对象。
    """
    # 获取图片的宽度和高度
    width, height = image.size
    
    # 创建一个ImageDraw对象，用于绘制
    draw = ImageDraw.Draw(image)
    
    # 计算水平和竖直方向的中间位置
    mid_x = width // 2
    mid_y = height // 2
    
    # 绘制水平和竖直方向的辅助线
    draw.line([(0, mid_y), (width, mid_y)], fill="black", width=2)
    draw.line([(mid_x, 0), (mid_x, height)], fill="black", width=2)
    
    # 加载字体，用于绘制刻度值
    font = ImageFont.load_default()
    
    # 绘制水平方向的刻度
    for i in range(0, 1001, 100):
        x = (i / 1000) * width
        draw.line([(x, mid_y - 5), (x, mid_y + 5)], fill="blue", width=1)
        draw.text((x, mid_y + 10), str(i), fill="blue", font=font)
    
    # 绘制竖直方向的刻度
    for i in range(0, 1001, 100):
        if i == 500:
            continue
        y = (i / 1000) * height
        draw.line([(mid_x - 5, y), (mid_x + 5, y)], fill="blue", width=1)
        draw.text((mid_x + 10, y), str(i), fill="blue", font=font)
    
    return image

def draw_rectangles_with_labels(image, coordinates_list, labels):
    """
    在图像上绘制多个矩形并在合适的位置写上标签。

    :param image: PIL图像对象
    :param coordinates_list: 包含多个坐标列表或元组的列表或元组，每个坐标列表或元组包含四个数字，表示矩形的左上和右下相对坐标 (x1, y1, x2, y2)，归一化到1000
    :param labels: 包含多个字符串的列表或元组，表示矩形框出东西的类别
    :return: 处理后的PIL图像对象
    """
    # 确保输入的坐标列表和标签列表是有效的
    if not isinstance(coordinates_list, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise ValueError("coordinates_list 和 labels 必须是一个列表或元组")
    
    if len(coordinates_list) != len(labels):
        raise ValueError("coordinates_list 和 labels 的长度必须相同")
    
    # 获取图像的宽度和高度
    width, height = image.size
    
    # 创建一个ImageDraw对象
    draw = ImageDraw.Draw(image)
    
    # 计算字体大小，根据图像的宽度和高度动态调整
    font_size = int(min(width, height) / 50)  # 字体大小为图像宽度和高度的1/50
    
    # 加载支持中文的字体（例如宋体）
    font = ImageFont.truetype("/mnt/c/Windows/Fonts/simhei.ttf", 16)

    
    # 遍历每个坐标和标签
    for coordinates, label in zip(coordinates_list, labels):
        # 确保每个坐标是有效的
        if not isinstance(coordinates, (list, tuple)) or len(coordinates) != 4:
            raise ValueError("每个坐标必须是一个包含四个数字的列表或元组")
        
        x1, y1, x2, y2 = coordinates
        
        # 确保坐标在0到1000之间
        if not (0 <= x1 <= 1000 and 0 <= y1 <= 1000 and 0 <= x2 <= 1000 and 0 <= y2 <= 1000):
            raise ValueError("坐标必须在0到1000之间")
        
        # 将相对坐标转换为实际像素坐标
        x1 = int(x1 * width / 1000)
        y1 = int(y1 * height / 1000)
        x2 = int(x2 * width / 1000)
        y2 = int(y2 * height / 1000)
        
        # 绘制矩形
        draw.rectangle([x1, y1, x2, y2], outline="black", width=2)
        
        # 计算标签的宽度
        (font_width,font_height), (_ ,_) = font.font.getsize(label)
        
        # 尝试不同的位置放置标签，避免与矩形重合
        positions = [
            (x1, y1 - font_height - 5),  # 上方
            (x1, y2 + 5),  # 下方
            (x1 - font_width - 5, y1),  # 左侧
            (x2 + 5, y1)  # 右侧
        ]
        
        # 选择一个合适的位置
        for pos in positions:
            if (0 <= pos[0] <= width - font_width and 0 <= pos[1] <= height - font_height):
                draw.text(pos, label, fill="black", font=font)
                break
    
    return image

