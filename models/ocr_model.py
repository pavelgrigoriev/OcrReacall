import os

import numpy as np
from datetime import datetime
import pyscreenshot as ImageGrab
import easyocr
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


class OcrModel():
    def __init__(self, image_folder):
        self.image_folder = image_folder + "/images"
        # Создаем папку для изображений, если она не существует
        os.makedirs(self.image_folder, exist_ok=True)
        # Инициализация модели OCR
        self.reader = easyocr.Reader(['ru', 'en'], gpu=True)

    def take_screenshot(self):
        """Захватываем полный экран."""
        return ImageGrab.grab()

    def images_are_different(self, img1, img2, threshold=0.01):
        """Сравниваем два изображения и определяем, отличаются ли они на заданный порог."""
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)

        diff = np.abs(np_img1 - np_img2)
        diff_mean = np.mean(diff)
        diff_max = np.max(diff)
        diff_normalized = diff_mean / diff_max

        # print(
        #     f"Mean difference: {diff_mean}, Normalized difference: {diff_normalized}")

        return diff_normalized > threshold

    def save_screenshot(self, image):
        """Сохраняем изображение в файл с уникальным именем."""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(
            self.image_folder, f"fullscreen_{timestamp}.png")
        image.save(filename)
        # print(f"Screenshot saved as {filename}")
        return filename

    def process_image(self, image_path):
        """Обрабатываем изображение с помощью OCR и помещаем результат в очередь."""
        result = self.reader.readtext(image_path, detail=0)
        result_queue.put(result)
