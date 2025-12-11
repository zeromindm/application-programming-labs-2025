import matplotlib.pyplot as plt
import cv2


def show_comparison(original: np.ndarray, processed: np.ndarray, 
                   title_original: str, title_processed: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    if len(original.shape) == 3:
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    else:
        original_rgb = original
    
    axes[0].imshow(original_rgb)
    axes[0].set_title(title_original)
    axes[0].axis('off')
    
    if len(processed.shape) == 3:
        processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
    else:
        processed_rgb = processed
    
    axes[1].imshow(processed_rgb)
    axes[1].set_title(title_processed)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()