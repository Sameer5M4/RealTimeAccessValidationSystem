import cv2
import os

def draw_box_on_image(image_path, coordinates, label, output_path="verification_output.jpg"):
    """
    Draws a single bounding box on an image to verify coordinates.

    Args:
        image_path (str): The path to the original image.
        coordinates (list): A list of four numbers [x1, y1, x2, y2].
        label (str): A text label to draw above the box (e.g., "student_photo").
        output_path (str): The filename for the output image.
    """
    # 1. Read the image from the file
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"--- ERROR ---")
        print(f"Could not read the image from the path: {image_path}")
        print("Please make sure the file exists and is a valid image.")
        return

    # 2. Convert coordinates to integers, as required by OpenCV
    try:
        x1, y1, x2, y2 = [int(c) for c in coordinates]
    except (ValueError, TypeError):
        print(f"--- ERROR ---")
        print(f"The coordinates provided are not valid: {coordinates}")
        print("Please provide a list of four numbers, like [100, 150, 200, 250].")
        return

    # 3. Draw the rectangle on the image
    # Color is in (B, G, R) format. (36, 255, 12) is a bright green.
    # Thickness is the line width in pixels.
    cv2.rectangle(image, (x1, y1), (x2, y2), color=(36, 255, 12), thickness=2)

    # 4. Draw the text label above the box
    # We'll place the text 10 pixels above the top-left corner of the box.
    cv2.putText(
        image,
        label,
        (x1, y1 - 10),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=(36, 255, 12),
        thickness=2
    )

    # 5. Save the modified image to a new file
    cv2.imwrite(output_path, image)
    
    print("--- SUCCESS ---")
    print(f"Verification image has been saved as: {output_path}")


if __name__ == '__main__':
    # ==================================================================
    # STEP 1: UPDATE THESE FOUR VALUES
    # ==================================================================
    
    # Provide the path to the image you want to draw on.
    IMAGE_TO_CHECK = 'testData/50kb.jpg'

    # Paste the coordinates your model gave you. Format is [x1, y1, x2, y2].
    # Example: [123.45, 234.56, 345.67, 456.78]
    COORDINATES_TO_VERIFY = [353.78387451171875, 312.2796936035156, 793.531494140625, 365.7069091796875]

    # Give the box a name so you know what you're looking at.
    LABEL_FOR_BOX = "student_photo"
    
    # Choose a name for the output file.
    OUTPUT_FILENAME = "verified_photo_box.jpg"

    # ==================================================================
    # STEP 2: RUN THE SCRIPT
    # ==================================================================
    
    # Check if the input file exists before running
    if not os.path.exists(IMAGE_TO_CHECK):
        print(f"--- ERROR ---")
        print(f"The input file was not found: {IMAGE_TO_CHECK}")
        print("Please update the 'IMAGE_TO_CHECK' variable with the correct path.")
    else:
        # Call the function to perform the drawing and saving
        draw_box_on_image(IMAGE_TO_CHECK, COORDINATES_TO_VERIFY, LABEL_FOR_BOX, OUTPUT_FILENAME)