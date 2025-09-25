from ultralytics import YOLO
import cv2

# --- CONFIGURATION ---
# Path to your newly trained model file.
MODEL_PATH = './best.pt'

# Path to the image you want to test. Change this to test different images.
TEST_IMAGE_PATH = 'testData/50kb.jpg' 

# Confidence threshold: Detections below this score will be ignored.
CONFIDENCE_THRESHOLD = 0.5

def validate_id_card(image_path, model):
    """
    Validates an ID card using the final, correct logic:
    - Fails if 'wrong_layout' is detected.
    - Succeeds if 'collegeName_with_logo' is detected (and 'wrong_layout' is not).
    """
    try:
        # Run inference on the image
        results = model(image_path, verbose=False)
        result = results[0]
        class_names = model.names
    except Exception as e:
        print(f"Error during model inference: {e}")
        return

    detected_classes = {}
    detected_objects = {}

    # Step 1: Gather all high-confidence detections from the model
    for box in result.boxes:
        confidence = box.conf[0].item()
        if confidence > CONFIDENCE_THRESHOLD:
            class_id = int(box.cls[0].item())
            class_name = class_names[class_id]
            
            # Store the detection's confidence and coordinates
            detected_classes[class_name] = confidence
            detected_objects[class_name] = box.xyxy[0].tolist()

    # --- Print what the model found ---
    print("\n--- High-Confidence Detections ---")
    if not detected_classes:
        print("No objects detected with confidence >", CONFIDENCE_THRESHOLD)
    else:
        for name, conf in detected_classes.items():
            print(f"- Found '{name}' with confidence: {conf:.2f}")

    # --- Final, Correct Decision Logic ---
    print("\n--- Validation Result ---")

    # Priority 1 (Security): If 'wrong_layout' is detected, it's an immediate failure.
    if 'wrong_layout' in detected_classes:
        print("Status: FAILED")
        print("Reason: A 'wrong_layout' was detected.")
        return

    # Priority 2 (Success): If 'collegeName_with_logo' is detected and 'wrong_layout' was not, it's a success.
    if 'collegeName_with_logo' in detected_classes:
        print("Status: SUCCESS")
        print("Reason: 'collegeName_with_logo' detected, layout is considered valid.")
        print("\n--- Extracted Coordinates [x1, y1, x2, y2] ---")
        
        # Loop through the names of the fields we want to extract
        for name in ['student_photo', 'student_name', 'student_roll_number']:
            if name in detected_objects:
                print(f"- {name}: {detected_objects[name]}")
            else:
                print(f"- {name}: Not Found")
        return
        
    # Priority 3 (Default Failure): If neither of the key layout indicators was found.
    print("Status: FAILED")
    print("Reason: Could not verify the card layout (key components like 'collegeName_with_logo' not found).")


if __name__ == '__main__':
    # Load the trained model with error handling
    try:
        yolo_model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        print(f"Please make sure the file '{MODEL_PATH}' exists and is a valid model file.")
        exit()

    # Validate the test image
    validate_id_card(TEST_IMAGE_PATH, yolo_model)