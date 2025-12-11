import argparse
import cv2
import os
from pathlib import Path

from image_processing import (
    get_image_info,
    crop_image_from_top_left,
    get_all_images_in_dir,
)

from image_visualization import show_comparison


def parse_args() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Обрезка всех изображений в папке до заданных размеров"
    )

    parser.add_argument(
        "-i", "--input_dir", 
        type=str, 
        required=True, 
        help="Путь к папке с изображениями"
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        required=True,
        help="Папка для сохранения результатов",
    )

    parser.add_argument(
        "-w",
        "--width",
        type=int,
        required=True,
        help="Ширина обрезки в пикселях",
    )

    parser.add_argument(
        "-he",
        "--height",
        dest="height",
        type=int,
        required=True,
        help="Высота обрезки в пикселях",
    )

    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        
        image_files = get_all_images_in_dir(args.input_dir)
        
        if not image_files:
            print(f"В папке {args.input_dir} не найдено изображений")
            return
        
        print(f"Найдено {len(image_files)} изображений")
        
        for i, img_path in enumerate(image_files, 1):
            filename = os.path.basename(img_path)
            print(f"[{i}/{len(image_files)}] Обработка: {filename}")
            
            img = cv2.imread(img_path)
            if img is None:
                print(f"  Ошибка загрузки: {filename}")
                print()
                continue
            
            width, height, channels = get_image_info(img)
            
            cropped = crop_image_from_top_left(img, args.width, args.height)
            
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_cropped{ext}"
            output_path = os.path.join(args.output_dir, output_filename)
            
            cv2.imwrite(output_path, cropped)
            print(f"  Сохранено: {output_filename}")
            
            show_comparison(
                img, 
                cropped, 
                f"Исходное: {filename} ({width}x{height})",
                f"Обрезанное: {filename} ({args.width}x{args.height})"
            )
            
            print()
            
        print(f"Готово! Все изображения сохранены в: {args.output_dir}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()