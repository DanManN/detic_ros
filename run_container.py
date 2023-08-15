#!/usr/bin/env python3

# NOTE: please use only standard libraries
import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

_DETIC_ROS_ROOT_INSIDE_CONTAINER = "/home/user/detic_ws/src/detic_ros"


def add_prefix(file_path: Path, prefix: str) -> Path:
    parent = file_path.parent
    return parent / (prefix + file_path.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mount", type=str, help="mount source launch file or directory"
    )
    parser.add_argument(
        "-models", type=str, help="mount directory for Detic pretrained models"
    )
    parser.add_argument("-name", type=str, help="launch file name")
    parser.add_argument(
        "-host", type=str, default="pr1040", help="host name or ip-address"
    )
    parser.add_argument(
        "launch_args",
        nargs=argparse.REMAINDER,
        help="launch args in ros style e.g. foo:=var",
    )
    args = parser.parse_args()

    mount_path_str: Optional[str] = args.mount
    assert mount_path_str is not None
    mount_path = Path(mount_path_str)

    models_path: Optional[str] = args.models
    if models_path is not None:
        models_path = Path(models_path)

    launch_file_name: Optional[str] = args.name
    assert launch_file_name is not None

    for launch_arg in args.launch_args:
        assert bool(re.match(r".*:=.*", launch_arg))
    launch_args = " ".join(args.launch_args)

    with TemporaryDirectory() as td:
        tmp_launch_path = Path(td) / "launch"

        if mount_path.is_dir():
            shutil.copytree(mount_path, tmp_launch_path)
        else:
            shutil.copyfile(mount_path, tmp_launch_path)

        if models_path is not None:
            mount_models_str="-v {}:{}/models".format(models_path,_DETIC_ROS_ROOT_INSIDE_CONTAINER)
        else:
            mount_models_str=""

        docker_run_command = """
            docker run \
                -v {tmp_launch_path}:{detic_ros_root}/launch \
                {maybe_mount_models_path} \
                --rm --net=host -it \
                --gpus 1 detic_ros:latest \
                /bin/bash -i -c \
                "source ~/.bashrc; \
                roscd detic_ros; \
                rossetip $ROS_IP; rossetmaster {host}; \
                roslaunch detic_ros {launch_file_name} {launch_args}"
                """.format(
            tmp_launch_path=tmp_launch_path,
            detic_ros_root=_DETIC_ROS_ROOT_INSIDE_CONTAINER,
            maybe_mount_models_path=mount_models_str,
            host=args.host,
            launch_file_name=launch_file_name,
            launch_args=launch_args,
        )
        print(docker_run_command)
        subprocess.call(docker_run_command, shell=True)
