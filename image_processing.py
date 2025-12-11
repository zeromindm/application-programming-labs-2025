import cv2
import numpy as np
import os


def get_image_info(img: np.ndarray) -> tuple:
    height, width = img.shape[:2]
    channels = img.shape[2] if len(img.shape) == 3 else 1
    
    return width, height, channels


def crop_image_from_top_left(img: np.ndarray, crop_width: int, crop_height: int) -> np.ndarray:
    height, width = img.shape[:2]
    
    actual_width = min(crop_width, width)
    actual_height = min(crop_height, height)
    
    return img[0:actual_height, 0:actual_width]


def get_all_images_in_dir(input_dir: str) -> list:
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    image_files = []
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    
    return sorted(image_files)