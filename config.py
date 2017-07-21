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
SQLALCHEMY_DATABASE_URI = 'postgresql://rysxbcmtfrizgg:f83aa7c7c22300b62cd5cf475948efd146a33136c06b8029d44645a688e7d57c@ec2-184-73-236-170.compute-1.amazonaws.com/db7ai5ug00k7do'
CSRF_ENABLED = True
USER_ENABLE_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
