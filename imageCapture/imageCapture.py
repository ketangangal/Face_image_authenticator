import cv2
import os
from loguru import logger
from from_root import from_root

logger.add(sink=os.path.join(from_root(), 'logs.log'),
           format="[{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {module} ] - {message}",
           level="INFO")


def capture_image(path, number_of_images):
    """
    :Created by: Ketan Gangal
    :param path: "path to store images"
    :param number_of_images: "number of images you want to capture"
    :return: "Status of execution of function"
    """
    try:
        vid = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = vid.read()
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('x') and count < number_of_images:
                print('Captured Image ', count + 1)
                cv2.imwrite(os.path.join(path, str(count) + '.jpg'), frame)
                count += 1
                if count == number_of_images:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        vid.release()
        cv2.destroyAllWindows()

        if count == number_of_images:
            logger.info('Successfully captured Images')
            return True, 'Successfully captured Images'
        else:
            logger.info('Program stopped')
            return False, 'Program stopped'
    except Exception as e:
        logger.error(f'Error while capturing Images {e.__str__()}')
        return False, "Error"


