import os
import requests

# 🔧 Configuration
FOLDER_PATH = "./data"  # Replace with the actual path
UPLOAD_URL = "https://localhost:3000/.integration/api/webhook/google-analytics"  # Replace with your target URL

def find_myactivity_files(base_folder):
    files = {}
    for root, dirs, filenames in os.walk(base_folder):
        for filename in filenames:
            if filename == "MyActivity.json":
                parent_folder = os.path.basename(root)
                renamed = f"{parent_folder}.json"
                full_path = os.path.join(root, filename)
                files[renamed] = full_path
    return files

def create_multipart_payload(files_dict):
    multipart_data = {}
    for name, path in files_dict.items():
        multipart_data[name] = (name, open(path, 'rb'), 'application/json')
    return multipart_data

def upload_files(files_dict):
    print(f"Uploading {len(files_dict)} file(s)...")
    response = requests.post(UPLOAD_URL, files=create_multipart_payload(files_dict))
    print(f"Response code: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    files = find_myactivity_files(FOLDER_PATH)
    if not files:
        print("No files found.")
    else:
        upload_files(files)
