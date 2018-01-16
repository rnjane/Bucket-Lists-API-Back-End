# import os
# import urllib
# import psycopg2


# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )

SECRET_KEY = "mysecretalone"
SQLALCHEMY_DATABASE_URI = 'postgres://uycbaccjqarraa:80a7f82339090c38f6c23e37232e55e49de51befc2014eddf4d7c4dfb0f6d4df@ec2-54-235-219-113.compute-1.amazonaws.com:5432/d4a1q3rqevudhl'
CSRF_ENABLED = True
USER_ENABLE_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
