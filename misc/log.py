from logging.config import fileConfig
import os

paths = [
    'logging.conf',
    'etc/logging.conf'
]

for i in paths:
    if os.path.exists(i):
        fileConfig(i)
        break
