import yaml
import uuid
import os
from from_root import from_root
from cryptography.fernet import Fernet


def read_config(config):
    with open(config) as config:
        content = yaml.safe_load(config)

    return content


# PId Generator
def unique_id_generator():
    try:
        random = uuid.uuid4()
        unique_id = "PID" + str(random)

        return unique_id
    except Exception as e:
        return f"Error in unique_id_generator {e.__str__()}"


# Create User Space
def make_user_folder(unique_id=None, where=None):
    try:
        if where == "api":
            path = os.path.join(from_root(), "apiImage", unique_id)
            if os.path.isdir(path):
                return "Folder already Exists"
            else:
                os.mkdir(path=path)
                return "Folder Created"
        elif where == "imageStore":
            path = os.path.join(from_root(), "imageStore", unique_id)
            if os.path.isdir(path):
                return "Folder already Exists"
            else:
                os.mkdir(path=path)
                return "Folder Created"
        else:
            return "Wrong path in where"
    except Exception as e:
        return f"Error in make_user_folder {e.__str__()}"


# Check of user folder is empty or not
def check_folder(unique_id=None, where=None):
    try:
        if where == "api":
            path = os.path.join(from_root(), "apiImage", unique_id)
            if len(os.listdir(path)) == 0:
                return "Api Folder Empty"
            else:
                return "Image already Exists in api"

        elif where == "imageStore":
            path = os.path.join(from_root(), "imageStore", unique_id)
            if len(os.listdir(path)) == 0:
                return "Image store Folder Empty"
            else:
                return "Image already Exists in store"
        else:
            return "Wrong path in where"
    except Exception as e:
        return f"Error in make_user_folder {e.__str__()}"


def encrypt(message=None):
    try:
        key = b'TrN6MYpiY53IMPVeZj7qm7vDAbRlwcMX85VBbwM5wIM='
        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())
        return encMessage
    except Exception as e:
        return f"Error in encrypt {e.__str__()}"


def decrypt(encMessage=None):
    try:
        key = b'TrN6MYpiY53IMPVeZj7qm7vDAbRlwcMX85VBbwM5wIM='
        fernet = Fernet(key)
        decMessage = fernet.decrypt(encMessage)
        return decMessage.decode("utf-8")
    except Exception as e:
        return f"Error in decrypt {e.__str__()}"

