import os
import cloudinary
from dotenv import load_dotenv
from cloudinary import uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)


def upload_to_cloudinary_members(image_file):
    response = uploader.upload(image_file, folder="members")
    full_url = response.get("secure_url").strip()
    
    return full_url.split("/upload/")[1]

def upload_to_cloudinary_projects(image_file):
    response = uploader.upload(image_file, folder="projects")
    full_url = response.get("secure_url").strip()
    
    return full_url.split("/upload/")[1]


def upload_to_cloudinary_stand(image_file):
    response = uploader.upload(image_file, folder="stands")
    full_url = response.get("secure_url").strip()
    
    return full_url.split("/upload/")[1]
