#!/usr/bin/python3
""" Fabric script to distribute an archive to web servers """

from fabric.api import env, run, put, sudo
from os.path import exists

env.hosts = ['52.86.193.42', '52.86.161.66']


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

