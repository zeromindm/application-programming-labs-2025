import argparse
import os
from data_loader import load_data_from_annotation, save_dataframe
from dataframe_operations import add_file_size_column, sort_by_column, filter_by_column
from plot_generator import plot_sizes


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Анализ размеров файлов изображений'
    )
    
    parser.add_argument(
        '--annotation',
        type=str,
        default='annotation.csv',
        help='Путь к файлу аннотации CSV (по умолчанию: annotation.csv)'
    )
    
    parser.add_argument(
        '--output_folder',
        type=str,
        default='.',
        help='Папка для сохранения результатов (по умолчанию: текущая папка)'
    )
    
    parser.add_argument(
        '--min_size',
        type=float,
        default=None,
        help='Минимальный размер файла для фильтрации в байтах (например: 50000)'
    )
    
    parser.add_argument(
        '--max_size',
        type=float,
        default=None,
        help='Максимальный размер файла для фильтрации в байтах (например: 200000)'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    output_csv = os.path.join(args.output_folder, 'processed_image_data.csv')
    output_plot = os.path.join(args.output_folder, 'file_sizes_plot.png')
    
    df = load_data_from_annotation(args.annotation)

    df = add_file_size_column(df)

    sorted_df = sort_by_column(df, 'Размер_файла_байты')

    filtered_df = filter_by_column(
        sorted_df, 
        'Размер_файла_байты', 
        min_value=args.min_size, 
        max_value=args.max_size
    )
    
    plot_sizes(sorted_df, output_plot)

    save_dataframe(filtered_df, output_csv)
    
    if args.min_size is not None:
        print(f"  Минимальный размер: {args.min_size} байт")
    if args.max_size is not None:
        print(f"  Максимальный размер: {args.max_size} байт")


if __name__ == "__main__":
    main()
