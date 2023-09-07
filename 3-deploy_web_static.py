#!/usr/bin/python3
""" Fabric script that creates and distributes an archive to web servers """

from fabric.api import local, env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ['52.86.193.42', '52.86.161.66']


def do_pack():
    """ generate a tar.gz file from web_static folder """

    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = ("versions/web_static_{}.tgz".format(timestamp))
    result = local("tar -czvf {} web_static".format(path))

    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """ deploy archive to servers """

    if not exists(archive_path):
        return False

    try:
        # Extract necessary information from the archive path
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.replace(".tgz", "")
        folder_path = "/data/web_static/releases/{}/".format(folder_name)

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create necessary directories and extract the archive
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))

        # Remove temporary archive file
        run("rm -rf /tmp/{}".format(file_name))

        # Move the extracted files to the appropriate location
        run("mv {}/web_static/* {}".format(folder_path, folder_path))

        # Remove the web_static directory within the release folder
        run("rm -rf {}/web_static".format(folder_path))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new version
        run("ln -s {} /data/web_static/current".format(folder_path))

        print('deployment done')
        return True

    except Exception as e:
        print("Error during deployment:", str(e))
        return False


def deploy():
    """ deploy web_static """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
