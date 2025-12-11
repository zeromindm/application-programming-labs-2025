import matplotlib.pyplot as plt


def plot_sizes(df: pd.DataFrame, output_image: str = 'file_sizes_plot.png'):
    sorted_df = df.sort_values('Размер_файла_байты').reset_index(drop=True)
    
    plt.figure(figsize=(12, 6))
    
    image_numbers = list(range(1, len(sorted_df) + 1))
    file_sizes = sorted_df['Размер_файла_байты'].tolist()
    
    plt.plot(image_numbers, file_sizes, 'b-', linewidth=2, marker='o', markersize=4)
    
    plt.title('Размеры файлов изображений', fontsize=14, fontweight='bold')
    plt.xlabel('Номер изображения (отсортированный)', fontsize=12)
    plt.ylabel('Размер файла (байты)', fontsize=12)
    
    plt.grid(True, alpha=0.3)
    plt.xlim(0, len(sorted_df) + 1)
    
    if file_sizes:
        plt.ylim(0, max(file_sizes) * 1.1)
    
    plt.tight_layout()
    plt.savefig(output_image, dpi=150)
    plt.show()