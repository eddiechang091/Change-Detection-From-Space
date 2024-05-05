import cv2
import numpy as np
import os

def resize_to_match(img1, img2):
    # Resize the second image to match the dimensions of the first image
    return cv2.resize(img2, (img1.shape[1], img1.shape[0]), interpolation=cv2.INTER_AREA)

def segment_trees(image):
    # Advanced segmentation to identify tree areas
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    return mask

def count_trees(segmented_before, segmented_after):
    difference = cv2.absdiff(segmented_before, segmented_after)
    _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    num_labels, labels_im = cv2.connectedComponents(cleaned)
    return num_labels - 1

input_folder = '../input_queue'
output_folder = '../output_queue'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Identify the before and after images
files = os.listdir(input_folder)
before_image_path = next((os.path.join(input_folder, f) for f in files if '_1' in f), None)
after_image_path = next((os.path.join(input_folder, f) for f in files if '_2' in f), None)

# Ensure both images are found
if before_image_path is None or after_image_path is None:
    raise FileNotFoundError("Before and/or after image files not found in the input folder.")

# Load the images
img1 = cv2.imread(before_image_path)
img2 = cv2.imread(after_image_path)

# Ensure both images are the same size
if img1.shape[:2] != img2.shape[:2]:
    img2 = resize_to_match(img1, img2)

# Calculate segment for both images
ndvi_before = segment_trees(img1)
ndvi_after = segment_trees(img2)



# Count the approximate number of trees cut
trees_cut = count_trees(ndvi_before, ndvi_after)
result_text = f"Approximately {trees_cut} trees have been cut down."

# Output the result to a text file
output_path = os.path.join(output_folder, 'tree_cut_count.txt')
with open(output_path, 'w') as file:
    file.write(result_text)

print(result_text)
