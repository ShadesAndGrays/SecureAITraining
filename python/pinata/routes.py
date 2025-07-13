from flask import Blueprint, request, render_template
from flask_cors import cross_origin
import requests
import os
import joblib
#import ipfshttpclient no latest version we doing this raw

pinata_bp=Blueprint('pinata',__name__,url_prefix='/pinata')

pinata_api_key = os.getenv("PINATA_API_KEY")
pinata_secret_api_key = os.getenv("PINATA_SECRET_API_KEY")
pinata_gateway = os.getenv("PINATA_GATEWAY")
pinata_jwt = os.getenv("PINATA_JWT")

PINATA_URL = f"https://api.pinata.cloud/v3/files/public"

IPFS_HOST_IP = os.getenv("IPFS_HOST_IP")
IPFS_API_PORT = os.getenv("IPFS_API_PORT")
IPFS_API_BASE_URL = f"http://{IPFS_HOST_IP}:{IPFS_API_PORT}/api/v0"
IPFS_API_URL_ADD = f"{IPFS_API_BASE_URL}/add"
IPFS_API_URL_CAT = f"{IPFS_API_BASE_URL}/cat"
# res = requests.post(f'{IPFS_API_BASE_URL}/pin/ls')
# print(res.json())

     
@pinata_bp.route('/ipfs-download/<string:cid>/<string:path>', methods=['GET'])
@cross_origin(origin='*')
def download(cid,path):
    return pinata_download(cid,path)


@pinata_bp.route('/ipfs-upload', methods=['GET'])
@cross_origin(origin='*')
def upload():
    file_path = request.args.get('file_path')
    pinata_upload(file_path)
    pass

@pinata_bp.route('/heartbeat', methods=['GET'])
@cross_origin(origin='*')
def heartbeat():
    return 'good from ipfs' 

def pinata_download(cid,path):
    return ipfs_download(cid,path)
    # url = f'https://{pinata_gateway}/ipfs/{cid}'
    # print("dowload",url)
    # response = requests.request("GET", url)
    # response.raise_for_status()
    # with open(path,'wb') as f:
    #     f.write(response.content)
    # return path


def pinata_upload(file_path):
    return ipfs_upload(file_path)
    # url = f'https://uploads.pinata.cloud/v3/files'
    # file_name = file_path.split('/')[-1]
    # headers = {
    #     "Authorization": f"Bearer {pinata_jwt}",
    #     # "Content-Type": "multipart/form-data"
    # }
    # data = { 
    #     "network": "public",
    #     "name": file_name,          # Replace with desired name
    # }
    # files = {
    #     "file": (file_name,open(file_path, "rb").read())
    # }
    # response = requests.request("POST", url, data=data, headers=headers,files=files)
    # response.raise_for_status()
    # print(response.text)
    # return response.json()['data']['cid']

def upload_object_to_ipfs(python_object, filename='model_params.joblib'):
    """
    (INPUT) Python object <any> 
    (OUTPUT) cid <string>
    """
    try:
        # 1. Serialize the Python object to bytes
        serialized_data = joblib.dumps(python_object)

        # 2. Prepare the data for upload as multipart/form-data
        # The 'files' parameter in requests expects a dictionary:
        # {'field_name': ('filename', file_content_as_bytes, 'content_type')}
        # IPFS API typically expects the field name to be 'file'
        files = {
            'file': (filename, serialized_data, 'application/octet-stream')
        }

        # 3. Make the POST request to the IPFS add endpoint
        print(f"Uploading data to IPFS: {IPFS_API_URL_ADD}")
        response = requests.post(IPFS_API_URL_ADD, files=files)
        response.raise_for_status()

        # 4. Parse the JSON response
        data = response.json()
        cid = data['Hash']
        print(f"Successfully uploaded. CID: {cid}")
        return cid

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to IPFS daemon {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during upload: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return None

def upload_file_to_ipfs(file_path):
    """
    Uploads a local file to IPFS.
    Returns the CID (Content ID) if successful, None otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None


    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/octet-stream')
            }
            print(f"Uploading file '{os.path.basename(file_path)}' to IPFS: {IPFS_API_URL_ADD}")
            response = requests.post(IPFS_API_URL_ADD, files=files)
            response.raise_for_status()

            data = response.json()
            cid = data['Hash']
            print(f"Successfully uploaded. CID: {cid}")
            return cid

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to IPFS daemon. {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during upload: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return None

def download_object_from_ipfs(cid,path):
    """
    Downloads content from IPFS by CID and attempts to unpickle it.
    Returns the unpickled Python object if successful, None otherwise.
    """
    try:
        # 1. Prepare query parameters
        params = {'arg': cid}

        # 2. Make the POST request to the IPFS cat endpoint
        print(f"Downloading content for CID: {cid} from {IPFS_API_URL_CAT}")
        response = requests.post(IPFS_API_URL_CAT, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses

        # 3. Get the raw bytes content
        with open(path,'wb') as f:
            f.write(response.content)

        # 4. return path 
        return path

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to IPFS daemon. {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during download: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 404:
            print("Error: Content not found on IPFS daemon (CID might be incorrect or not pinned).")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        return None

def ipfs_download(cid,path):
    return download_object_from_ipfs(cid,path)


def ipfs_upload(file_path):
    return upload_file_to_ipfs(file_path)