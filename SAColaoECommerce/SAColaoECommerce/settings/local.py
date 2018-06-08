from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='4#u9-nwtlgcgntuvx1&&yr9nz(d*u6$thqzjm!wt$3h-kw#yed')

DEBUG = env.bool('DJANGO_DEBUG', default=True)