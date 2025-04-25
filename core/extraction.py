import json
import requests
from core import utils
from core.const import *
import os
from core.base import BaseWorker
from core.log import LoggerConfig

logger_config = LoggerConfig()
logger = logger_config.get_logger(__name__)





class APIBaseExtraction(BaseWorker):
    def __init__(self, timestamp: int, **kwargs):
        self.timestamp = timestamp

    def process(self):
        logger.info('Start api extraction process ')
        raw_data = self.fetch_raw_data()
        self.save_data(raw_data)
        logger.info('Finish api extraction process ')

    def fetch_raw_data(self):
        return self._fetch_api_data(POSTS_ENDPOINT, ATTEMPTS)

    def save_data(self, data):
        self._save_rawdata_to_local(f'{RAW_DATA_SAVE_PATH}/raw_data_{self.timestamp}.json', data)

    def _fetch_api_data(self, api_url: str, attempts: int) -> str:
        for attempt in range(1, attempts + 1):
            try:
                response = requests.get(api_url)
                if response.status_code != 200:
                    logger.warning(
                        f'Attempt {attempt}/{attempts} - Failed to fetch data: url: {POSTS_ENDPOINT}, status_code: {response.status_code}')
                else:
                    content = response.text
                    logger.info(f'Fetched data from API: url: {POSTS_ENDPOINT}')
                    return content
            except Exception as e:
                logger.warning(f'Attempt {attempt}/{attempts} - Error fetching data from API: {e}')
        logger.error(f'All {attempts} attempts failed to fetch data from API: url: {POSTS_ENDPOINT}')
        exit(1)

    def _save_rawdata_to_local(self, file_path: str, data: str):
        logger.info(f'Start saving raw data into local file: {file_path}')
        if not utils.is_json(data):
            try:
                json_data = json.dumps(data)
            except Exception as e:
                logger.error(f'Decode data to json failed with exception: {e}')
        else:
            json_data = data
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
                logger.info(f'Finish saved data from API to local file: {file_path}')
        except Exception as e:
            logger.error(f'Error saving data from API: path {file_path} ,cause:  {e}')




