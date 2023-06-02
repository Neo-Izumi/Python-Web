import sys
import logging

sys.path.insert(0, 'the absolute path points to the Python-Web directory. ex /var/www/Python-Web')
sys.path.insert(0, 'the absolute path points to the python virtual environment. ex /var/www/Python-Web/venv/python3.10/site-packages/')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from main import app as application