from flask import Blueprint, request, render_template
from flask_cors import cross_origin
import requests
import os

pinata_bp=Blueprint('pinata',__name__,url_prefix='/pinata')

pinata_api_key = os.getenv("PINATA_API_KEY")
pinata_secret_api_key = os.getenv("PINATA_SECRET_API_KEY")
pinata_gateway = os.getenv("PINATA_GATEWAY")
pinata_jwt = os.getenv("PINATA_JWT")

# PINATA_URL = f"https://api.pinata.cloud/v3/files/public"

     
@pinata_bp.route('/ipfs-download/<string:cid>', methods=['GET'])
@cross_origin(origin='*')
def ipfs_download(cid):
    request.mimetype 
    url = f'https://{pinata_gateway}/ipfs/{cid}'
    response = requests.request("GET", url)
    response.raise_for_status()
    print(response.text)
    return response.text

@pinata_bp.route('/ipfs-upload', methods=['GET'])
@cross_origin(origin='*')
def ipfs_upload():
    file_path = request.args.get('file_path')
    file_name = file_path.split('/')[-1]

    headers = {
        "Authorization": f"Bearer {pinata_jwt}",
        # "Content-Type": "multipart/form-data"
    }
    url = f'https://uploads.pinata.cloud/v3/files'
    public = "pubilc" 
    data = { 
        "network": "public",
        "name": file_name,          # Replace with desired name
    }
    files = {
        "file": (file_name,open(file_path, "rb").read())
   }
    response = requests.request("POST", url, data=data, headers=headers,files=files)
    response.raise_for_status()
    print(response.text)
    return response.json()

@pinata_bp.route('/heartbeat', methods=['GET'])
@cross_origin(origin='*')
def heartbeat():
    return 'good from ipfs' 