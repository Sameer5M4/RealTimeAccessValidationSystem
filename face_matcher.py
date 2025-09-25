import cv2
from deepface import DeepFace
import os

# --- CONFIGURATION ---
# The backend model to use for face recognition. VGG-Face is a good balance of speed and accuracy.
# Other options: "Facenet", "Facenet512", "ArcFace", "SFace"
FACE_RECOGNITION_MODEL = "VGG-Face"

def match_faces(selfie_path, id_card_path, id_photo_coords):
    """
    Matches a face from a selfie against a face cropped from an ID card.

    Args:
        selfie_path (str): The file path to the user's selfie image.
        id_card_path (str): The file path to the original ID card image.
        id_photo_coords (list): A list of four numbers [x1, y1, x2, y2] for the photo on the ID card.

    Returns:
        None. Prints the result directly to the console.
    """
    print("\n--- Starting Face Verification ---")

    # 1. --- Load and Crop the Photo from the ID Card ---
    try:
        id_card_img = cv2.imread(id_card_path)
        if id_card_img is None:
            print("Status: ERROR")
            print(f"Reason: Could not read the ID card image at path: {id_card_path}")
            return

        # Ensure coordinates are integers for cropping
        x1, y1, x2, y2 = [int(c) for c in id_photo_coords]
        
        # Crop the image using NumPy slicing
        id_photo_crop = id_card_img[y1:y2, x1:x2]

        # Optional: Save the crop to see if it's correct
        # cv2.imwrite("debug_id_crop.jpg", id_photo_crop)

    except Exception as e:
        print("Status: ERROR")
        print(f"Reason: Failed to crop the photo from the ID card. Error: {e}")
        return

    # 2. --- Verify the Faces using DeepFace ---
    try:
        # The core of the logic. DeepFace.verify() does all the work.
        # It detects faces, aligns them, and compares them.
        # 'enforce_detection=True' will raise an error if a face isn't found.
        result = DeepFace.verify(
            img1_path=selfie_path,
            img2_path=id_photo_crop,
            model_name=FACE_RECOGNITION_MODEL,
            enforce_detection=True
        )

        # 3. --- Interpret the Result ---
        print("\n--- Face Verification Result ---")
        if result['verified']:
            print("Status: MATCH")
            print("Reason: The face in the selfie is a confident match to the face on the ID card.")
        else:
            print("Status: NO MATCH")
            print("Reason: The two faces are determined to be from different people.")
        
        print(f"(Distance Score: {result['distance']:.2f} - lower is a better match)")

    except ValueError as e:
        # This error is typically raised by DeepFace when a face cannot be detected.
        print("\n--- Face Verification Result ---")
        print("Status: ERROR")
        error_message = str(e).lower()
        if "face could not be detected" in error_message:
            if "first" in error_message:
                print("Reason: Could not detect a clear face in the selfie image. Please provide a clearer picture.")
            elif "second" in error_message:
                print("Reason: Could not detect a clear face in the ID card photo. The ID card may be blurry or damaged.")
        else:
            print(f"Reason: An unexpected error occurred during face detection. Details: {e}")

    except Exception as e:
        # Catch any other unexpected errors.
        print("\n--- Face Verification Result ---")
        print("Status: ERROR")
        print(f"Reason: An unexpected error occurred. Details: {e}")


if __name__ == '__main__':
    # --- This is where you will integrate the code ---
    # In a real application, these values will come from your UI and the YOLO model.

    # 1. Provide the path to the user's uploaded selfie.
    SELFIE_IMAGE_PATH = 'testData/sai.jpg'

    # 2. Provide the path to the user's uploaded ID card.
    ID_CARD_IMAGE_PATH = 'testData/50kb.jpg'

    # 3. Provide the coordinates for the student photo, which you get from your YOLO model.
    #    Format is [x1, y1, x2, y2].
    ID_PHOTO_COORDINATES = [80.03714752197266, 225.78961181640625, 301.0567321777344, 463.36761474609375] # Example coordinates, replace with real ones.

    # Check if the example files exist before running
    if not os.path.exists(SELFIE_IMAGE_PATH) or not os.path.exists(ID_CARD_IMAGE_PATH):
        print("="*50)
        print("SETUP REQUIRED:")
        print("Please update the placeholder paths in the 'if __name__ == '__main__':' block.")
        print(f" - Set SELFIE_IMAGE_PATH to a valid selfie image.")
        print(f" - Set ID_CARD_IMAGE_PATH to a valid ID card image.")
        print(f" - Set ID_PHOTO_COORDINATES to the actual coordinates from your YOLO model.")
        print("="*50)
    else:
        # Run the face matching function
        match_faces(SELFIE_IMAGE_PATH, ID_CARD_IMAGE_PATH, ID_PHOTO_COORDINATES)