from typing import Union
from urllib.request import urlretrieve

from conf.base import IMAGE_FOLDER
from utils.log import get_log

logger = get_log(__file__)


def donwload_img(url: str, comic_id: int) -> Union[str, bool]:
    IMAGE_FOLDER.mkdir(exist_ok=True, parents=True)
    img_path = IMAGE_FOLDER.joinpath(f"{comic_id}.jpg")

    try:
        urlretrieve(url, img_path)
        return str(img_path)
    except Exception as e:
        logger.error(f"Can't download img {url} , caused by: {e}")
        return False
