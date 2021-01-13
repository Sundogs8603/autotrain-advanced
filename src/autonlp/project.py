import requests
import os

from . import config
from loguru import logger


class Project:
    def __init__(self, name, org, user):
        self.name = name
        self.org = org
        self.user = user

    def upload(self, files, split, col_mapping):
        jdata = {"project": self.name, "org": self.org, "user": self.user}
        for file_path in files:
            base_name = os.path.basename(file_path)
            binary_file = open(file_path, "rb")
            files = [("files", (base_name, binary_file, "text/csv"))]
            response = requests.post(
                url=config.HF_AUTONLP_BACKEND_API + "/uploader/upload_files",
                data=jdata,
                files=files,
            )
            logger.info(response.text)

            payload = {
                "split": split,
                "col_mapping": col_mapping,
                "data_files": [{"fname": base_name, "username": self.user, "org": self.org}],
            }
            logger.info(payload)
            response = requests.post(url=config.HF_AUTONLP_BACKEND_API + "/projects/1/data/add", json=payload)
            logger.info(response.text)

    def train(self):
        response = requests.get(url=config.HF_AUTONLP_BACKEND_API + "/projects/1/data/start_process")
        logger.info(response.text)
