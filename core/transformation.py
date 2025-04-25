from core.const import *
import json
from core.base import BaseWorker
from core.log import LoggerConfig
import os

logger_config = LoggerConfig()
logger = logger_config.get_logger(__name__)


class Transformation(BaseWorker):
    def __init__(self, timestamp: int, delimiter="\u0001"):
        self.timestamp = timestamp
        self.delimiter = delimiter

    def process(self):
        raw_data_file_path = f'{RAW_DATA_SAVE_PATH}/raw_data_{self.timestamp}.json'
        processed_data_file_path = f'{PROCESS_DATA_SAVE_PATH}/processed_data_{self.timestamp}.txt'
        logger.info(f"data transformation started , transform data file {raw_data_file_path}")
        raw_data = self._get_raw_data(file_path=raw_data_file_path)
        processed_data = self.transform(raw_data)
        self.save_processed_data(processed_data,
                                 file_path=processed_data_file_path)
        logger.info(f"data transformation completed save to file {processed_data_file_path}")

    def _get_raw_data(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = f.read()
            return raw_data

    def transform(self, data):
        logger.info("data transformation started")
        try:
            json_data = json.loads(data)
            processed_data = ''
            for post in json_data:
                user_id = post['userId']
                id = post['id']
                title = post['title']
                content = post['body'].replace('\n', '\\n').strip()
                processed_data += f"{user_id}{self.delimiter}{id}{self.delimiter}{title}{self.delimiter}{content}\n"
            logger.info(f"data transformation completed")
            return processed_data
        except Exception as e:
            logger.error(f'Error while processing data {data}, case: {e}')

    def save_processed_data(self, data: str, file_path: str):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            logger.error(f'Error saving processed  data : path {file_path} ,cause:  {e}')
