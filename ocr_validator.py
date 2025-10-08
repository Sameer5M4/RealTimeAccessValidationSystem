# import cv2
# import pytesseract
# import os
# import re

# # --- CONFIGURATION ---
# # IMPORTANT: Uncomment and update this path if Tesseract is not automatically found on your system.
# # This is common on Windows.
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# def clean_extracted_text(text, keywords_to_remove):
#     """
#     Removes common keywords and extra characters from the OCR output.
#     This function is case-insensitive.
#     """
#     # Create a temporary variable to modify
#     cleaned_text = text

#     # Remove common keywords, ignoring case (e.g., "Roll No" and "roll no")
#     for keyword in keywords_to_remove:
#         # (?i) is a regex flag for case-insensitivity
#         cleaned_text = re.sub(f'(?i){keyword}', '', cleaned_text)

#     # Remove common separators like colons, hyphens, and extra spaces
#     cleaned_text = re.sub(r'[:\- ]', '', cleaned_text)
    
#     # Return the final cleaned and stripped text
#     return cleaned_text.strip()


# def is_roll_number_valid(roll_no):
#     """
#     Validates a given roll number against GPREC's specific B.Tech format criteria.
    
#     Args:
#         roll_no (str): The extracted and cleaned roll number text.

#     Returns:
#         tuple: A tuple containing (bool, str). 
#                (True, "Valid") if it matches the criteria.
#                (False, "Reason for failure") if it does not.
#     """
#     # Rule 0: Check for expected length (10 characters)
#     if len(roll_no) != 10:
#         return False, f"Incorrect length. Expected 10 characters, but got {len(roll_no)}."

#     # --- Deconstruct the Roll Number ---
#     year_str = roll_no[0:2]
#     college_code = roll_no[2]
#     admission_type_indicator = roll_no[4]
    
#     # --- Validation Rules ---
#     # Rule 1: Year of Admission (Digits 1-2) must be between 22 and 29.
#     try:
#         year = int(year_str)
#         if not (22 <= year <= 29):
#             return False, f"Year of admission '{year}' is out of the valid range (22-29)."
#     except ValueError:
#         return False, f"Year of admission '{year_str}' is not a valid number."

#     # Rule 2: College Code (Digit 3) must be '9'.
#     if college_code != '9':
#         return False, f"College code is '{college_code}', but expected '9'."

#     # Rule 3: Check for the two valid formats based on admission type (Digit 5).
#     # Format for Regular B.Tech (e.g., 239X1A0301)
#     if admission_type_indicator == '1':
#         pattern = r"^\d{2}9X1A\w{2}\w{2}$"
#         if not re.match(pattern, roll_no):
#             return False, "Does not match the Regular B.Tech format (e.g., 239X1A0301)."
#     # Format for Lateral Entry (e.g., 179X5A02E0)
#     elif admission_type_indicator == '5':
#         pattern = r"^\d{2}9X5A\w{2}\w{2}$"
#         if not re.match(pattern, roll_no):
#             return False, "Does not match the Lateral Entry format (e.g., 179X5A02E0)."
#     else:
#         return False, f"Admission type indicator is '{admission_type_indicator}', but expected '1' or '5'."

#     # If all checks passed
#     return True, "Valid"


# def validate_text_fields(id_card_path, student_name_coords, roll_number_coords):
#     """
#     Crops, extracts, cleans, and validates text from an ID card image.
#     """
#     print("\n--- Starting OCR Text Field Validation ---")
    
#     try:
#         id_card_img = cv2.imread(id_card_path)
#         if id_card_img is None:
#             print("Status: ERROR\nReason: Could not read the ID card image at the specified path.")
#             return
#     except Exception as e:
#         print(f"Status: ERROR\nReason: Failed to load image. {e}")
#         return

#     # --- 1. Crop, OCR, and Clean Student Name ---
#     try:
#         x1, y1, x2, y2 = [int(round(c)) for c in student_name_coords]
#         name_crop = id_card_img[y1:y2, x1:x2]
        
#         name_config = r'-c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ." --psm 7'
#         raw_name_text = pytesseract.image_to_string(name_crop, config=name_config).strip()
        
#         # Define keywords to remove from the name field
#         name_keywords_to_remove = ["Name", "Student Name", "Student"]
#         student_name_text = clean_extracted_text(raw_name_text, name_keywords_to_remove)

#     except Exception as e:
#         print(f"Status: FAILED\nReason: Could not process student name coordinates. Error: {e}")
#         return

#     # --- 2. Crop, OCR, and Clean Roll Number ---
#     try:
#         x1, y1, x2, y2 = [int(round(c)) for c in roll_number_coords]
#         roll_no_crop = id_card_img[y1:y2, x1:x2]
        
#         roll_no_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 7'
#         raw_roll_no_text = pytesseract.image_to_string(roll_no_crop, config=roll_no_config).strip()
        
#         # Define keywords to remove from the roll number field
#         roll_no_keywords_to_remove = ["Roll No", "Roll Number", "RN", "ROll", "R0ll"] # Added common OCR mistakes
#         roll_number_text = clean_extracted_text(raw_roll_no_text, roll_no_keywords_to_remove)

#     except Exception as e:
#         print(f"Status: FAILED\nReason: Could not process roll number coordinates. Error: {e}")
#         return
        
#     print(f"\nRaw Extracted Name: '{raw_name_text}' -> Cleaned: '{student_name_text}'")
#     print(f"Raw Extracted Roll No: '{raw_roll_no_text}' -> Cleaned: '{roll_number_text}'")

#     # --- 3. Perform Final Validations on Cleaned Text ---
#     validation_errors = []
    
#     # Validation A: Check if student name is present
#     if len(student_name_text) < 3:
#         validation_errors.append("Student Name not found or is too short.")
    
#     # Validation B: Check if the cleaned roll number is valid
#     is_valid, reason = is_roll_number_valid(roll_number_text)
#     if not is_valid:
#         validation_errors.append(f"Roll Number is invalid: {reason}")
        
#     # --- 4. Display Final Result ---
#     print("\n--- OCR Validation Result ---")
#     if not validation_errors:
#         print("Status: SUCCESS")
#         print("Reason: Successfully validated all text fields.")
#     else:
#         print("Status: FAILED")
#         print("Reason(s):")
#         for error in validation_errors:
#             print(f"- {error}")


# if __name__ == '__main__':
#     # ==================================================================
#     # STEP 1: UPDATE THESE PLACEHOLDER VALUES FOR YOUR TEST
#     # ==================================================================
    
#     # Provide the path to the ID card you want to validate.
#     ID_CARD_IMAGE_PATH = 'testData/50kb.jpg'

#     # Provide the coordinates for the Student Name from your YOLO model.
#     STUDENT_NAME_COORDS = [341, 209, 829, 276] # Example: [x1, y1, x2, y2]

#     # Provide the coordinates for the Roll Number from your YOLO model.
#     ROLL_NUMBER_COORDS = [341, 280, 829, 350] # Example: [x1, y1, x2, y2]
    
#     # ==================================================================
#     # STEP 2: RUN THE SCRIPT
#     # ==================================================================
    
#     if not os.path.exists(ID_CARD_IMAGE_PATH):
#         print("SETUP REQUIRED: The file specified in 'ID_CARD_IMAGE_PATH' was not found.")
#     else:
#         validate_text_fields(ID_CARD_IMAGE_PATH, STUDENT_NAME_COORDS, ROLL_NUMBER_COORDS)

import cv2
import pytesseract
import os
import re

# --- CONFIGURATION ---
# IMPORTANT: Uncomment and update this path if Tesseract is not automatically found.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import cv2
import pytesseract
import os
import re

# --- CONFIGURATION ---
# IMPORTANT: Uncomment and update this path if Tesseract is not automatically found.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import cv2
import pytesseract
import os
import re

# --- CONFIGURATION ---
# IMPORTANT: Uncomment and update this path if Tesseract is not automatically found.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def advanced_clean_extracted_text(text):
    """
    An advanced function to clean OCR'd text from an ID card.
    """
    keywords = ["Name", "Student Name", "Student", "Roll No", "Roll Number", "RN", "ROll", "R0ll"]
    separators = [':', ';', '-']
    cleaned_text = text
    found_separator = False
    for sep in separators:
        if sep in cleaned_text:
            try:
                cleaned_text = cleaned_text.split(sep, 1)[1]
                found_separator = True
                break
            except IndexError:
                cleaned_text = ""
                found_separator = True
                break
    if not found_separator:
        for keyword in keywords:
            cleaned_text = re.sub(f'(?i){keyword}', '', cleaned_text)
    cleaned_text = re.sub(r'[^A-Za-z0-9 ]+', '', cleaned_text).strip()
    return cleaned_text


def preprocess_for_ocr(image):
    """
    Applies preprocessing steps to an image to improve OCR accuracy.
    """
    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Apply a binary threshold to get a black and white image
    #    This helps to remove noise and shadows.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 3. Slightly enlarge the image (interpolation helps smoothing)
    #    Tesseract often performs better on slightly larger text.
    scale_factor = 2
    width = int(thresh.shape[1] * scale_factor)
    height = int(thresh.shape[0] * scale_factor)
    dim = (width, height)
    resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_CUBIC)
    
    # Optional: Save the preprocessed image for debugging
    # cv2.imwrite("debug_preprocessed_roll_crop.jpg", resized)

    return resized


def extract_text_fields(id_card_path, student_name_coords, roll_number_coords):
    """
    Crops, preprocesses, extracts, and cleans text from an ID card image.
    """
    print("\n--- Starting OCR Text Extraction ---")
    
    try:
        id_card_img = cv2.imread(id_card_path)
        if id_card_img is None:
            print("Status: ERROR\nReason: Could not read the ID card image at the specified path.")
            return
    except Exception as e:
        print(f"Status: ERROR\nReason: Failed to load image. {e}")
        return

    # --- 1. Process Student Name (usually doesn't need preprocessing) ---
    try:
        x1, y1, x2, y2 = [int(round(c)) for c in student_name_coords]
        name_crop = id_card_img[y1:y2, x1:x2]
        raw_name_text = pytesseract.image_to_string(name_crop, config=r'--psm 7').strip()
        student_name_text = advanced_clean_extracted_text(raw_name_text)
    except Exception as e:
        print(f"Status: ERROR\nReason: Could not process student name coordinates. Error: {e}")
        return

    # --- 2. Process Roll Number (with PREPROCESSING) ---
    try:
        x1, y1, x2, y2 = [int(round(c)) for c in roll_number_coords]
        roll_no_crop = id_card_img[y1:y2, x1:x2]
        
        # --- NEW PREPROCESSING STEP ---
        preprocessed_roll_crop = preprocess_for_ocr(roll_no_crop)
        
        # Run OCR on the new, cleaner image
        raw_roll_no_text = pytesseract.image_to_string(preprocessed_roll_crop, config=r'--psm 7').strip()
        roll_number_text = advanced_clean_extracted_text(raw_roll_no_text)

    except Exception as e:
        print(f"Status: ERROR\nReason: Could not process roll number coordinates. Error: {e}")
        return
        
    # --- 3. Display Final Extracted Data ---
    print("\n--- OCR EXTRACTION RESULT ---")
    print(f"Raw Extracted Name:    '{raw_name_text}'")
    print(f"Cleaned Name:          '{student_name_text}'")
    print("-" * 30)
    print(f"Raw Extracted Roll No: '{raw_roll_no_text}'")
    print(f"Cleaned Roll No:       '{roll_number_text}'")


if __name__ == '__main__':
    # ==================================================================
    # STEP 1: UPDATE THESE PLACEHOLDER VALUES FOR YOUR TEST
    # ==================================================================
    
    ID_CARD_IMAGE_PATH = 'testData/3.jpg'
    STUDENT_NAME_COORDS = [540.642822265625, 417.192138671875, 1306.5504150390625, 559.5859985351562]
    ROLL_NUMBER_COORDS = [537.5161743164062, 504.6066589355469, 1146.6292724609375, 642.0905151367188]
    
    # ==================================================================
    # STEP 2: RUN THE SCRIPT
    # ==================================================================
    
    if not os.path.exists(ID_CARD_IMAGE_PATH):
        print("SETUP REQUIRED: The file specified in 'ID_CARD_IMAGE_PATH' was not found.")
    else:
        extract_text_fields(ID_CARD_IMAGE_PATH, STUDENT_NAME_COORDS, ROLL_NUMBER_COORDS)