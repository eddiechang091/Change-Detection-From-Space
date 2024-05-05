import cv2
import numpy as np
import os

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (1024, 768))
    # Enhancing contrast using histogram equalization
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    return blurred

def detect_containers(image):
    # Apply adaptive thresholding to enhance container edges
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to separate connected containers
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    separated = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    contours, _ = cv2.findContours(separated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    container_count = 0
    
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 1.2 <= aspect_ratio <= 5.0:  # More specific to container shapes
                container_count += 1
                
    return container_count


def compare_container_counts(img_path1, img_path2):
    img1 = preprocess_image(img_path1)
    img2 = preprocess_image(img_path2)
    count1 = detect_containers(img1)
    count2 = detect_containers(img2)
    difference_in_teu = abs(count1 - count2) // 2
    return difference_in_teu

def process_image_pairs(input_folder, output_folder):
    # Identify the before and after images
    files = os.listdir(input_folder)
    before_image_path = next((os.path.join(input_folder, f) for f in files if '_1' in f), None)
    after_image_path = next((os.path.join(input_folder, f) for f in files if '_2' in f), None)
    # Ensure both images are found
    if before_image_path is None or after_image_path is None:
        raise FileNotFoundError("Before and/or after image files not found in the input folder.")
    difference = compare_container_counts(before_image_path, after_image_path)
    result_line = f"Difference in TEU = {difference}\n"
    with open(os.path.join(output_folder, f"teu_difference.txt"), 'w') as f:
        f.write(result_line)
            

# Define paths to input and output folders
input_folder_path = '../input_queue'
output_folder_path = '../output_queue'
process_image_pairs(input_folder_path, output_folder_path)
