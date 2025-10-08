import os
import cloudinary
from dotenv import load_dotenv
from cloudinary import uploader


load_dotenv()

cloudinary.config(
    cloud_name="dktkxxfxj",
    api_key="312515664979372",
    api_secret="G7licg9At4DjbzNt4YQ0WJ_LC9o"
)

def upload_to_cloudinary_members(image_file):
    response = uploader.upload(image_file, folder="members")
    return response.get("secure_url")

def upload_to_cloudinary_projects(image_file):
    response = uploader.upload(image_file, folder="projects")
    return response.get("secure_url")

def upload_to_cloudinary_stand(image_file):
    response = uploader.upload(image_file, folder="stands")
    return response.get("secure_url")