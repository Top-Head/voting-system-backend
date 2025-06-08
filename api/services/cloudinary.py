import os
import cloudinary
from dotenv import load_dotenv
from cloudinary import uploader

load_dotenv()

cloudinary.config(
    cloud_name="do4yyqaxj",
    api_key="369969542636612",
    api_secret="xpae38WkXnOxVlmybg1WLrxJw1M"
)

def upload_to_cloudinary_members(image_file):
    response = uploader.upload(image_file, folder="members")
    return response.get("secure_url")

def upload_to_cloudinary_projects(image_file):
    response = uploader.upload(image_file, folder="projects")
    return response.get("secure_url")