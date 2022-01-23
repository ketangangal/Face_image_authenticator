import os
from from_root import from_root


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


#response = make_user_folder(unique_id="pid12234", where='api')
check = check_folder(unique_id="pid12234", where='imageStore')
#print(response)
print(check)
