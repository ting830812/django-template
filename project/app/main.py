import time
from django.core.cache import cache

from . import utils

def processor(file_id, file_name, f):
    """main processor with input file
    """

    # Put your own code here
    # Following code is an example for how to deal with uploaded file

    # Handle input file
    lines = []
    try:
        for chunk in f.chunks():
            lines.extend(chunk.decode('ascii').split('\n'))

    except Exception:
        raise InvalidFileException

    # Processing and produce result file
    results = []
    for line in lines:
        results.append(line + ' test')
    time.sleep(5)
    
    # Save the result to cache
    cache.set(file_id, (file_name, 'finish_processing', results), utils.FILE_RESULTS_CACHE_TIME)