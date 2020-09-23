# Django template for processing uploaded file
A simple Django template allows developer to deploy a website with his own code to process the input file uploaded by users, and then provide a download link for the result.   

## Develop

### Environment
```sh
# Download anaconda
apt-get install wget
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh

# Install Django
pip install django==3.0.4

```
### Clone this project
```sh
git clone git@github.com:ting830812/django-template.git
```

### Put your own code in `main.py`

`project/app/main.py`
```python
import time
from django.core.cache import cache

from . import utils

def processor(file_id, file_name, f):
    """main processor with input file
    """

    # Put your own code here
    # Following code is an example for how to deal with uploaded file
    # Here, we try to add 'test' at the end of each line in uploaded file

    # Handle input file
    lines = []
    try:
        for chunk in f.chunks():
            lines.extend(chunk.decode('ascii').split('\n'))

    except Exception:
        raise InvalidFileException

    # Process and produce the result file
    results = []
    for line in lines:
        results.append(line + ' test')
    time.sleep(5)
    
    # Save the result to cache
    cache.set(file_id, (file_name, 'finish_processing', results), utils.FILE_RESULTS_CACHE_TIME)

```
### Start running 
```sh
python manage.py runserver
```
Then you can see your website on http://localhost:8000/app/

