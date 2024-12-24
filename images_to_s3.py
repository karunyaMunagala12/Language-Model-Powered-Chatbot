import boto3
from dotenv import load_dotenv
import os
import csv
from urllib.parse import quote_plus

load_dotenv()

AWS_S3_ACCESS_KEY = os.environ.get('AWS_S3_ACCESS_KEY')
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')

# Constants
LOCAL_ROOT_DIR = 'Lecture_Notes'
BUCKET_NAME = 'ddm-eta'
CSV_FILE_PATH = 'image_s3_locations.csv'

# Initialize the S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)


# Helper function to clean file names
def clean_filename(filename):
    filename = filename.replace(" ", "_")
    return filename.replace('-', '_')

# Helper function to upload a file to S3, ensuring no redundant folder names
def upload_file_to_s3(local_path, s3_path):
    cleaned_filename = clean_filename(os.path.basename(s3_path))
    # Adjusting the path to avoid redundancy and ensure the "Lecture_Notes/" prefix
    path_parts = s3_path.split(os.sep)
    if len(path_parts) > 1:  # This checks if there are subdirectories in the path
        s3_upload_path = os.path.join("Lecture_Notes", path_parts[0], cleaned_filename)
    else:
        s3_upload_path = os.path.join("Lecture_Notes", cleaned_filename)
    s3_client.upload_file(local_path, BUCKET_NAME, s3_upload_path)
    # Creating a cleaner URL
    s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_upload_path.replace(os.path.sep, '/')}"
    return s3_url

# Main function to process directories and upload files
def process_and_upload_files():
    with open(CSV_FILE_PATH, 'w', newline='') as csv_file:
        fieldnames = ['Image Name', 'S3 Location']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for root, dirs, files in os.walk(LOCAL_ROOT_DIR):
            for file in files:
                if file.lower().endswith('.png'):
                    local_file_path = os.path.join(root, file)
                    # Adjusted to ensure the path does not double the lecture folder name
                    s3_file_path = os.path.relpath(local_file_path, start=LOCAL_ROOT_DIR)
                    s3_url = upload_file_to_s3(local_file_path, s3_file_path)
                    writer.writerow({'Image Name': file, 'S3 Location': s3_url})
                    print(f"Uploaded {file} to S3 with URL: {s3_url}")

if __name__ == "__main__":
    process_and_upload_files()