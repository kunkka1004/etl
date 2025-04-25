from pathlib import Path

## const define
BASE_URL = 'https://jsonplaceholder.typicode.com'
POSTS_ENDPOINT = f'{BASE_URL}/posts'
INTERVAL = 30
RAW_DATA_SAVE_PATH = Path(__file__).resolve().parent.parent / 'data/raw'
PROCESS_DATA_SAVE_PATH = Path(__file__).resolve().parent.parent / 'data/processed/'
ATTEMPTS = 3

DATA_LAKE_PATH = Path(__file__).resolve().parent.parent / 'data/data_lake'
