from django.core.cache import cache
import itertools
import threading
import multiprocessing
import uuid
import time

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
    lines = []
    try:
        for chunk in f.chunks():
            lines.extend(chunk.decode('ascii').split('\n'))

    except Exception:
        raise InvalidFileException

    file_id = str(uuid.uuid4())
    cache.set(file_id, (file_name, 'under_processing', []), FILE_RESULTS_CACHE_TIME)

    t = threading.Thread(target=service, args=(file_id, file_name, lines), daemon=True)
    t.start()
    return file_id

def service(file_id, file_name, lines):
    """main service with input file
    """
    results = []
    for line in lines:
        results.append(line + 'Test test test')
    time.sleep(5)
    
    cache.set(file_id, (file_name, 'finish_processing', results), FILE_RESULTS_CACHE_TIME)






