import os
import csv
from typing import List, Optional


class ImagePathIterator:

    def __init__(self, source: str):
        self.source = source
        self.file_paths: List[str] = []
        self.current_index = 0

        if os.path.isfile(source) and source.endswith('.csv'):
            self._load_from_annotation(source)
        else:
            raise ValueError("Источник должен быть CSV-файлом аннотации")

    def _load_from_annotation(self, annotation_file: str) -> None:
        try:
            with open(annotation_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'absolute_path' in row and os.path.exists(row['absolute_path']):
                        self.file_paths.append(row['absolute_path'])
            print(f"Загружено {len(self.file_paths)} путей из аннотации")
        except FileNotFoundError:
            print(f"Файл аннотации не найден: {annotation_file}")
        except Exception as e:
            print(f"Ошибка при чтении аннотации: {e}")

    def __iter__(self) -> 'ImagePathIterator':
        self.current_index = 0
        return self

    def __next__(self) -> str:
        if self.current_index < len(self.file_paths):
            path = self.file_paths[self.current_index]
            self.current_index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        return len(self.file_paths)

    def get_current_index(self) -> int:
        return self.current_index

    def get_total_count(self) -> int:
        return len(self.file_paths)

    def reset(self) -> None:
        self.current_index = 0

    def get_path_at(self, index: int) -> Optional[str]:
        if 0 <= index < len(self.file_paths):
            return self.file_paths[index]
        return None