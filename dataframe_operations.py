import pandas as pd
import os
from typing import Optional


def add_file_size_column(df: pd.DataFrame) -> pd.DataFrame:
    sizes = []
    
    for path in df['Абсолютный_путь']:
        try:
            if os.path.exists(path):
                size = os.path.getsize(path)
                sizes.append(size)
            else:
                sizes.append(0)
        except Exception:
            sizes.append(0)
    
    df = df.copy()
    df['Размер_файла_байты'] = sizes
    return df


def sort_by_column(df: pd.DataFrame, column_name: str, ascending: bool = True) -> pd.DataFrame:
    if column_name not in df.columns:
        raise ValueError(f"Колонка '{column_name}' не существует в DataFrame")
    
    return df.sort_values(by=column_name, ascending=ascending).reset_index(drop=True)


def filter_by_column(df: pd.DataFrame, column_name: str, 
                     min_value: Optional[float] = None, 
                     max_value: Optional[float] = None) -> pd.DataFrame:
    if column_name not in df.columns:
        raise ValueError(f"Колонка '{column_name}' не существует в DataFrame")
    
    filtered_df = df.copy()
    
    if min_value is not None:
        filtered_df = filtered_df[filtered_df[column_name] >= min_value]
    
    if max_value is not None:
        filtered_df = filtered_df[filtered_df[column_name] <= max_value]
    
    return filtered_df.reset_index(drop=True)