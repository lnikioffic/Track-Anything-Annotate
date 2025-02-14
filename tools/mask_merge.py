import cv2
import numpy as np


def merge_masks(masks, method='max'):
    if isinstance(masks, list):
        masks = np.array(masks)

    # Убедимся, что маски имеют корректную форму
    if len(masks.shape) != 3:
        raise ValueError(
            "Маски должны быть представлены в виде массива размерности (N, H, W)."
        )
    N, H, W = masks.shape

    # Создаем пустое цветное изображение
    mask_colored = np.zeros((H, W, 3), dtype=np.uint8)

    # Создаем список случайных цветов для каждой маски
    colors = [tuple(np.random.randint(0, 255, size=3)) for _ in range(N)]

    # Создаем уникальную индексированную маску
    unique_mask = np.zeros((H, W), dtype=np.uint8)

    for i in range(N):
        # Создаем цветную маску для текущей области
        color_mask = np.zeros_like(mask_colored)
        color_mask[masks[i] > 0] = colors[i]

        # Накладываем цветную маску на общее изображение
        mask_colored = cv2.addWeighted(mask_colored, 1, color_mask, 1, 0.0)

        # Присваиваем уникальные значения для текущей области в индексированной маске
        unique_mask[masks[i] > 0] = (
            i + 1
        )  # Используем i+1, чтобы избежать нулевого значения

    return mask_colored, unique_mask
