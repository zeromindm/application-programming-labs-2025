import pandas as pd


def load_data_from_annotation(annotation_file: str) -> pd.DataFrame:
    df = pd.read_csv(annotation_file)
    
    result_df = pd.DataFrame({
        'Абсолютный_путь': df['absolute_path'],
        'Относительный_путь': df['relative_path']
    })
    
    return result_df


def save_dataframe(df: pd.DataFrame, output_file: str = 'processed_data.csv'):
    df.to_csv(output_file, index=False, encoding='utf-8')