from ultralytics import YOLO
import cv2
import os

# --- CONFIGURATION ---
MODEL_PATH = './best.pt'
TEST_IMAGE_PATH = 'testData/4.jpg' 

# Confidence threshold for the initial detection pass.
CONFIDENCE_THRESHOLD = 0.20

# Intersection over Union (IoU) threshold for Non-Max Suppression.
# A lower value means it will be stricter and merge more boxes. 0.5 is a good default.
IOU_THRESHOLD = 0.5

def validate_id_card(image_path, model):
    """
    Validates an ID card using built-in Non-Max Suppression for cleaner results
    and enforces that all key fields are found.
    """
    try:
        # Load the image for drawing later
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Could not read the image.")
            return
            
        # Run inference. The library handles NMS automatically when you access the results.
        results = model(image_path, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD, verbose=False)
        result = results[0]
        class_names = model.names
    except Exception as e:
        print(f"Error during model inference: {e}")
        return

    # --- Step 1: Gather the final, clean detections after NMS ---
    detected_objects = {}
    print(f"\n--- Final Detections (Conf > {CONFIDENCE_THRESHOLD*100:.0f}%, IoU < {IOU_THRESHOLD}) ---")
    
    for box in result.boxes:
        # The boxes here are the clean results after NMS has been applied.
        class_id = int(box.cls[0].item())
        class_name = class_names[class_id]
        confidence = box.conf[0].item()
        coords = box.xyxy[0].tolist()
        
        # In case NMS still lets a duplicate through (rare), we keep the most confident one.
        if class_name not in detected_objects or confidence > detected_objects[class_name]['confidence']:
             detected_objects[class_name] = {
                 "coordinates": coords,
                 "confidence": confidence
             }

    if not detected_objects:
        print("No objects detected.")
    else:
        for name, data in detected_objects.items():
            print(f"- Found '{name}' with confidence: {data['confidence']:.2f}")
            # Draw the final box on the image
            x1, y1, x2, y2 = [int(c) for c in data['coordinates']]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{name} {data['confidence']:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Save the visual output
    output_filename = "debug_final_output.jpg"
    cv2.imwrite(output_filename, image)
    print(f"\nVisual output with final bounding boxes saved to: {output_filename}")


    # --- Final, STRICT Decision Logic ---
    print("\n--- Validation Result ---")
    if 'wrong_layout' in detected_objects:
        print("Status: FAILED\nReason: A 'wrong_layout' was detected.")
        return

    mandatory_fields = ['collegeName_with_logo', 'student_photo', 'student_name', 'student_roll_number']
    missing_fields = [field for field in mandatory_fields if field not in detected_objects]

    if not missing_fields:
        print("Status: SUCCESS\nReason: Layout is valid and all mandatory fields were found.")
        print("\n--- Extracted Coordinates [x1, y1, x2, y2] ---")
        for name in ['student_photo', 'student_name', 'student_roll_number']:
            print(f"- {name}: {detected_objects[name]['coordinates']}")
    else:
        print("Status: FAILED\nReason: The ID card layout is valid, but mandatory fields are missing.")
        print(f"Missing Field(s): {', '.join(missing_fields)}")


if __name__ == '__main__':
    try:
        yolo_model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        exit()
    validate_id_card(TEST_IMAGE_PATH, yolo_model)