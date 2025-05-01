import os
import cloudinary
from dotenv import load_dotenv
from cloudinary.uploader import upload

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_API_SECRET')
)

def upload_to_cloudinary_members(image_file):
    response = upload(image_file, folder="members")
    return response.get("secure_url")

def upload_to_cloudinary_projects(image_file):
    response = upload(image_file, folder="projects")
    return response.get("secure_url")