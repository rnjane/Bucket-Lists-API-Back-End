import os
import urllib
import psycopg2


urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

SECRET_KEY = "mysecretalone"
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/bucketlists'
CSRF_ENABLED = True
USER_ENABLE_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
