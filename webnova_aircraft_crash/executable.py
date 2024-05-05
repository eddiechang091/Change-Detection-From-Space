import cv2
import numpy as np
import os

def load_images(folder):
    # If there are no files in the folder, message and exit
    if not os.listdir(folder):
        print("No files to process.")
        exit()
    before_images = []
    after_images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            if "before" in filename:
                before_images.append((filename, img))
            elif "after" in filename:
                after_images.append((filename, img))
    return before_images, after_images

def save_image(image, path):
    cv2.imwrite(path, image)

def process_image_pair(before, after):
    # Resize 'after' image to match 'before' image dimensions
    after_resized = cv2.resize(after, (before.shape[1], before.shape[0]))
    
    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after_resized, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    before_eq = cv2.equalizeHist(before_gray)
    after_eq = cv2.equalizeHist(after_gray)

    # Apply edge detection
    before_edges = cv2.Canny(before_eq, 100, 200)
    after_edges = cv2.Canny(after_eq, 100, 200)

    # Compute the absolute difference between the edge images
    difference = cv2.absdiff(before_edges, after_edges)

    # Use adaptive thresholding
    thresholded = cv2.adaptiveThreshold(difference, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

    # Apply morphological closing to fill gaps
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    return closed

def main():
    input_folder = '../input_queue'
    output_folder = '../output_queue'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    before_images, after_images = load_images(input_folder)

    # Initialize variables to find the most significant change
    max_difference_area = 0
    max_image = None
    max_info = ""

    for before_name, before_img in before_images:
        for after_name, after_img in after_images:
            processed_diff = process_image_pair(before_img, after_img)
            
            # Find contours and select the largest contour
            contours, _ = cv2.findContours(processed_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > max_difference_area:
                    max_difference_area = cv2.contourArea(largest_contour)
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    center = (x + w // 2, y + h // 2)
                    radius = max(w, h) // 2
                    max_image = cv2.resize(after_img, (before_img.shape[1], before_img.shape[0])).copy()
                    cv2.circle(max_image, center, radius, (0, 0, 255), 2)  # Draw red circle
                    max_info = f'Change detected from {before_name} to {after_name}'

    if max_image is not None:
        output_path = os.path.join(output_folder, 'most_significant_change.png')
        save_image(max_image, output_path)
        print(max_info)

if __name__ == '__main__':
    main()
