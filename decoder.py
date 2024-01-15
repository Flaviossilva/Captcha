import sys
import cv2
import numpy as np
import pytesseract

ADAPTIVE_THRESH_BLOCK_SIZE = 11
ADAPTIVE_THRESH_C = 2
MORPH_KERNEL_SIZE = 2
MORPH_ITERATIONS = 2
ERODE_ITERATIONS = 1
OCR_CONFIG = r'-l eng --oem 3 --psm 7 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"'
OCR_CONFIG2 = r'--psm 11 --oem 3 -l eng -c --tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"'

def process_image(input_path, ocr_config=OCR_CONFIG):
    try:
        # Read image
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        # Increase image resolution if needed
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Applying adaptive thresholding
        img_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_C)

        # Inverting the image
        img_thresh = cv2.bitwise_not(img_thresh)

        # Morphological operations for noise reduction
        kernel = np.ones((MORPH_KERNEL_SIZE, MORPH_KERNEL_SIZE), np.uint8)
        img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel, iterations=MORPH_ITERATIONS)

        # Further denoising with erosion
        img_erode = cv2.erode(img_morph, kernel, iterations=ERODE_ITERATIONS)
        
        # Uncomment to see prewiew of the image processing steps
        #cv2.imshow("Original Image", img)
        #cv2.imshow("Thresholded Image", img_thresh)
        #cv2.imshow("Morphological Operations", img_morph)
        #cv2.imshow("Eroded Image", img_erode)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # OCR
        text = pytesseract.image_to_string(img_erode, config=ocr_config)
        print("Detected captcha text is:", text)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def main(image_path):
    # Replace 'your_image_path.png' with the path to your image file
    #image_path = image_path

    # Extract text from the image
    extracted_text = process_image(image_path, ocr_config=OCR_CONFIG)

    # Print the final result
    print("Extracted Text:", extracted_text)

# To run just execute: python3 teste.py <image_path>
if __name__ == "__main__":
    main(sys.argv[1])
    