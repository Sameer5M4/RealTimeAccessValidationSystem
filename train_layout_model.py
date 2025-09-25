from ultralytics import YOLO
import os

# --- Configuration ---
# Path to your data.yaml file. This file now controls the automatic split.
DATA_YAML_PATH = 'data.yaml'

# Choose a YOLOv10 model size (e.g., 'yolov10n.pt', 'yolov10s.pt')
MODEL_NAME = 'yolov10n.pt'

# Training parameters
EPOCHS = 50
IMAGE_SIZE = 640

def main():
    """
    Trains the YOLOv10 model using a dataset that will be split automatically
    by the Ultralytics library.
    """
    # Load a pretrained YOLOv10 model
    model = YOLO(MODEL_NAME)

    # Train the model
    # YOLO will read the 'data.yaml' file, see that 'train' and 'val' point
    # to the same directory, and automatically split the data.
    results = model.train(
        data=DATA_YAML_PATH,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        project='id_card_runs',
        name='layout_model_autosplit_v1' # New name for this run
    )

    print("\n--- Training Complete! ---")
    print(f"Model and results saved in the '{results.save_dir}' directory.")
    
    # The path to your best model weights
    best_model_path = os.path.join(results.save_dir, 'weights/best.pt')
    print("Your trained model is located at:", best_model_path)
    print("\nUse this path in your 'test_layout_model.py' script.")


if __name__ == '__main__':
    main()