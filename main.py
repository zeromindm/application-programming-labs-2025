from data_loader import load_data_from_annotation, save_dataframe
from dataframe_operations import add_file_size_column, sort_by_column, filter_by_column
from plot_generator import plot_sizes
from data_saver import save_dataframe


def main():
    df = load_data_from_annotation('annotation.csv')
    
    df = add_file_size_column(df)
    
    sorted_df = sort_by_column(df, 'Размер_файла_байты', ascending=True)
    
    filtered_df = filter_by_column(
        sorted_df, 
        'Размер_файла_байты', 
        min_value=50000, 
        max_value=200000
    )
    
    plot_sizes(sorted_df, 'file_sizes_plot.png')
    
    save_dataframe(sorted_df, 'processed_image_data.csv')


if __name__ == "__main__":
    main()