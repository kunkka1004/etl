import json

from core.const import *
import os
from datetime import datetime
from pathlib import Path
from core.base import BaseWorker
from core.log import LoggerConfig

logger_config = LoggerConfig()
logger = logger_config.get_logger(__name__)


class DataLake(BaseWorker):

    def __init__(self, timestamp, **kwargs):
        self.timestamp = timestamp

    def process(self, ):
        logger.info(f"start to write date to datalake both rawdata and processed data")
        try:
            dt = datetime.fromtimestamp(self.timestamp)
            formatted_date = dt.strftime('%Y-%m-%d')

            raw_data_file = f'{RAW_DATA_SAVE_PATH}/raw_data_{self.timestamp}.json'
            raw_data_lake_file = f'{DATA_LAKE_PATH}/raw/data_{formatted_date}.json'

            processed_data_file = f'{PROCESS_DATA_SAVE_PATH}/processed_data_{self.timestamp}.txt'
            processed_data_lake_file = f'{DATA_LAKE_PATH}/processed/data_{formatted_date}.txt'

            os.makedirs(os.path.dirname(raw_data_lake_file), exist_ok=True)
            os.makedirs(os.path.dirname(processed_data_lake_file), exist_ok=True)

            logger.info(f"read from raw data file {raw_data_file}")
            ## rawdata to lakehouse
            merge_content = []
            with open(raw_data_file, 'r', encoding='utf-8') as rf:
                pre_content = rf.read()
                if len(pre_content) > 0:
                    pre_json = json.loads(pre_content)
                    merge_content.extend(pre_json)
            if Path(raw_data_lake_file).exists():
                with open(raw_data_lake_file, 'r', encoding='utf-8') as lf:
                    current = lf.read()
                    ## merge to a whole json
                    if len(current) > 0:
                        current = json.loads(current)
                        merge_content.extend(current)

            data = json.dumps(merge_content, ensure_ascii=False)
            with open(raw_data_lake_file, 'w', encoding='utf-8') as f:
                f.write(data)

            logger.info(f"read from processed data file {processed_data_file}")

            ## processed data to lakehouse
            with open(processed_data_file, 'r', encoding='utf-8') as rf:
                with open(processed_data_lake_file, 'a', encoding='utf-8') as wf:
                    data = rf.read()
                    wf.write(data)

            logger.info(f"raw data written to datalake,file path {raw_data_lake_file}")
            logger.info(f"processed data written to datalake,file path:{processed_data_lake_file}")



        except Exception as e:
            logger.error(f"fail to write date to datalake  case: {e}")


if __name__ == '__main__':
    s = ''
    json.loads(s)
