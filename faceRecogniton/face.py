from deepface import DeepFace
from from_root import from_root
from loguru import logger
import os


logger.add(sink=os.path.join(from_root(), 'logs.log'),
           format="[{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} ] - {message}",
           level="INFO")


def detect_face(api_image=None, image_folder_path=None):
    """
    :api_image: Image from api
    :image_folder_path: users separate folder path
    """
    try:
        final_result = {}
        number_of_store_images = len(os.listdir(path=image_folder_path))

        for i in os.listdir(path=image_folder_path):

            path2 = os.path.join(from_root(), 'imageStore', i)
            result = DeepFace.verify(img1_path=api_image, img2_path=path2, enforce_detection=False)

            final_result["distance"] = final_result.get("distance", 0) + result['distance']
            final_result["verified"] = final_result.get("verified", 0) + result['verified']

        final_result["distance"] = (final_result["distance"]/number_of_store_images)*100
        final_result["distance"] = (final_result["verified"]/number_of_store_images)*100
        logger.info(final_result)

        return final_result
    except Exception as e:
        logger.error("Error in face detection {0}".format(e.__str__()))


