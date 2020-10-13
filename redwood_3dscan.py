########################################################
# Python script for downloading "A Large Dataset of Object Scans" dataset.
#
# Requirements:
# - Python 2.7 or 3.x
# - This script requires 'requests' module
#
# For more details, visit:
# - https://github.com/intel-isl/redwood-3dscan
# - http://redwood-data.org/3dscan
########################################################

import json
import requests
import time
import os
import sys


def _load_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def _download(url, dst_file, skip_if_exists=True):
    print("Downloading {} to {}.".format(url, dst_file))

    if skip_if_exists and os.path.isfile(dst_file):
        print("{} already exists. Skipped.".format(dst_file))
        return True

    dst_dir = os.path.dirname(dst_file)
    if not os.path.exists(dst_dir):
        print("Creating directory {}".format(dst_dir))
        os.makedirs(dst_dir)

    start_time = time.time()
    try:
        r = requests.get(url, stream=True)
        if r.ok:
            num_bytes = 0
            with open(dst_file, 'wb') as f:
                for chunk in r.iter_content(32768):
                    num_bytes += len(chunk)
                    f.write(chunk)
            mbytes = num_bytes / float(1000000)
            elapsed_time = time.time() - start_time
            speed = mbytes / elapsed_time
            print("Downloaded {:.2f}MB, speed {:.2f}MB/s.".format(
                mbytes, speed))
            return True
        else:
            print("Download request failed.")
            return False
    except:
        e = sys.exc_info()[0]
        print("Download request failed with exception {}.".format(e))
        return False


# List of RGBD image ids.
rgbds = _load_json("rgbds.json")

# List of mesh ids.
meshes = _load_json("meshes.json")

# Dictionary with {"category_0": [id_0, id_1, ...]}.
categories = _load_json("categories.json")

_base_url = "https://s3.us-west-1.wasabisys.com/redwood-3dscan"
_pwd = os.path.dirname(os.path.abspath(__file__))


def download_rgbd(scan_id, skip_if_exists=True):
    """Download RGBD scan by scan_id.

    Downloaded file will be saved to "data/rgbd/{scan_id}.zip".

    Args:
        scan_id: String of 5 digits, e.g. "00072".
        skip_if_exists: Skip downloading if the file already exists.
    """
    if scan_id in rgbds:
        url = "{}/rgbd/{}.zip".format(_base_url, scan_id)
        dst_file = os.path.join(_pwd, "data", "rgbd", "{}.zip".format(scan_id))
        _download(url, dst_file, skip_if_exists=skip_if_exists)
    else:
        print("RGBD scan_id {} is not available. Skipped.".format(scan_id))


def download_mesh(scan_id, skip_if_exists=True):
    """Download reconstructed mesh by scan_id.

    Downloaded file will be saved to "data/mesh/{scan_id}.zip".

    Args:
        scan_id: String of 5 digits, e.g. "00072".
        skip_if_exists: Skip downloading if the file already exists.
    """
    if scan_id in meshes:
        url = "{}/mesh/{}.ply".format(_base_url, scan_id)
        dst_file = os.path.join(_pwd, "data", "mesh", "{}.ply".format(scan_id))
        _download(url, dst_file, skip_if_exists=skip_if_exists)
    else:
        print("Mesh scan_id {} is not available. Skipped.".format(scan_id))


def download_video(scan_id, skip_if_exists=True):
    """Download RGB video by scan_id.

    Downloaded file will be saved to "data/video/{scan_id}.zip".

    Args:
        scan_id: String of 5 digits, e.g. "00072".
        skip_if_exists: Skip downloading if the file already exists.
    """
    if scan_id in rgbds:
        url = "{}/video/{}.mp4".format(_base_url, scan_id)
        dst_file = os.path.join(_pwd, "data", "video",
                                "{}.mp4".format(scan_id))
        _download(url, dst_file, skip_if_exists=skip_if_exists)
    else:
        print("Video scan_id {} is not available. Skipped.".format(scan_id))


def download_all(scan_id, skip_if_exists=True):
    """Download RGBD images, mesh and video by scan_id, if available.

    Downloaded file will be saved to "data/".

    Args:
        scan_id: String of 5 digits, e.g. "00072".
        skip_if_exists: Skip downloading if the file already exists.
    """
    download_rgbd(scan_id, skip_if_exists=skip_if_exists)
    download_mesh(scan_id, skip_if_exists=skip_if_exists)
    download_video(scan_id, skip_if_exists=skip_if_exists)


def download_category(category_name, skip_if_exists=True):
    """Download RGBD images, mesh and video by category_name, if available.

    Downloaded file will be saved to "data/".

    Args:
        category_name: String of the category name, e.g. "sofa".
        skip_if_exists: Skip downloading if the file already exists.
    """
    print("Downloading category {}.".format(category_name))
    if category_name not in categories:
        print("Category {} not found. Skipped.".format(category_name))
    else:
        for scan_id in categories[category_name]:
            download_all(scan_id, skip_if_exists=skip_if_exists)


if __name__ == "__main__":
    # Test cases
    download_all("00001")
    download_category("atm")
