#!/usr/bin/python3
""" generate a .tgz archive from contents of web_static """

from fabric.api import local
from datetime import datetime


def do_pack():
    """ generate a tar.gz file from web_static folder """

    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = ("versions/web_static_{}.tgz".format(timestamp))
    result = local("tar -czvf {} web_static".format(path))

    if result.failed:
        return None
    return path
