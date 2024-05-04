import shutil
import os

# Define the input and output directories
input_dir = '../input_queue'
output_dir = '../output_queue'

# List all files in the input directory
files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
# If no files in inupt directory, exit
if len(files) == 0:
    print("No files to process.")
    exit()
# Move each file to the output directory
for file in files:
    shutil.move(os.path.join(input_dir, file), os.path.join(output_dir, file))

print("Files moved successfully.")