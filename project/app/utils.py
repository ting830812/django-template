from django.core.cache import cache
import threading
import uuid
import time

from . import main

# How long will cache be saved (sec.). 
FILE_RESULTS_CACHE_TIME = 86400

def get_cached_data(file_id):
    """return cached pmids
    """
    cached_data = cache.get(file_id, None)
    if cached_data is None:
        raise FileNotFoundException
    file_name, status, results = cached_data
    return file_name, status, results


def handle_uploaded_file(f, file_name):
    """handle uploaded file
    """
    file_id = str(uuid.uuid4())
    cache.set(file_id, (file_name, 'under_processing', []), FILE_RESULTS_CACHE_TIME)

    t = threading.Thread(target=main.processor, args=(file_id, file_name, f), daemon=True)
    t.start()
    return file_id