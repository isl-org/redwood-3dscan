# A Large Dataset of Object Scans (redwood-3dscan)

<p align="center">
<img src="http://redwood-data.org/3dscan/img/teaser.jpg" width="640" />
</p>

## Abstract

We have created a dataset of more than ten thousand 3D scans of real objects.
To create the dataset, we recruited 70 operators, equipped them with
consumer-grade mobile 3D scanning setups, and paid them to scan objects in
their environments. The operators scanned objects of their choosing, outside the
laboratory and without direct supervision by computer vision professionals. The
result is a large and diverse collection of object scans: from shoes, mugs, and
toys to grand pianos, construction vehicles, and large outdoor sculptures. We
worked with an attorney to ensure that data acquisition did not violate privacy
constraints. The acquired data was irrevocably placed in the public domain and
is available freely.

You can preview and explore the dataset at
[http://redwood-data.org/3dscan/](http://redwood-data.org/3dscan/).

## Dataset organization

If you use our download scripts, the downloaded dataset will be stored in `data/`.

```txt
data
├── rgbd (10,933 RGBD scans, each contains multiple RGB and depth images)
│   ├── 00001.zip
│   ├── 00002.zip
│   ├── ...
│   ├── 11097.zip
│   └── 11098.zip
├── mesh (441 reconstructed models)
│   ├── 00004.ply
│   ├── 00033.ply
│   ├── ...
│   ├── 10548.ply
│   └── 10664.ply
└── video (10,933 videos created from images)
    ├── 00001.mp4
    ├── 00002.mp4
    ├── ...
    ├── 11097.mp4
    └── 11098.mp4
```

- Dataset size: The entire dataset is ~4TB in size.
- RGBD scans: There are 10,933 RGBD scans. Each scan contains multiple RGBD images.
- Meshes: There are 441 reconstructed mesh models.
- Videos: There are 10,933 videos, created from RGBD images.
- Categories: 9,131 RGBD scans are categorized into 320 categories. Each scan has at most one category.

## Example usage

```python
import redwood_3dscan as rws

# Print RGBD scans (list)
print(rws.rgbds)

# Print meshes (list)
print(rws.meshes)

# Print categories (dict: string->list)
print(rws.categories)

# Print all scan_id of the "sofa" category
print(rws.categories["sofa"])

# Download by scan_id "00033"
# Download will be skipped if the resource is unavailable
# e.g. some RGBD images may not come with mesh.
rws.download_rgbd("00033")  # Save to data/rgbd/00033.zip, if available
rws.download_mesh("00033")  # Save to data/mesh/00033.ply, if available
rws.download_video("00033") # Save to data/video/00033.mp4, if available
rws.download_all("00033")   # Downloads rgbd, mesh, and video together

# Download by category "sofa"
rws.download_category("sofa")
```

You can use
[Open3D](https://github.com/intel-isl/Open3D) to load and visualize the models.

```shell
# For installation guides, see:
# http://www.open3d.org/docs/release/getting_started.html
pip install open3d
```

```python
import redwood_3dscan as rws
import open3d as o3d

rws.download_mesh("00033")
mesh = o3d.io.read_triangle_mesh("data/mesh/00033.ply")
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
```

![Open3D Visualizer](assets/open3d_vis.png)

## License

The entire dataset, including both RGB-D scans and reconstructed models, is in
the [public domain](https://wiki.creativecommons.org/wiki/Public_domain). Any
part of the dataset can be used for any purpose with proper attribution. If
you use any of the data, please cite
[our technical report](http://arxiv.org/abs/1602.02481).

```bibtex
@article{Choi2016,
          author    = {Sungjoon Choi and Qian-Yi Zhou and Stephen Miller and Vladlen Koltun},
          title     = {A Large Dataset of Object Scans},
          journal   = {arXiv:1602.02481},
          year      = {2016},
        }
```

## File Format

The RGB-D sequences were acquired with PrimeSense Carmine cameras. The
resolution is 640×480, the frame rate is 30Hz. Each scan is packaged in a zip
archive that contains consecutive color images stored as JPG and depth images
stored as 16-bit PNG, where pixel values represent depth in millimeters. The
first part of a file name indicates the frame number and the second part
provides a time stamp in microseconds.

The focal length is 525 for both axes and the principal point is (319.5, 239.5).
The depth images are registered to the color images.

The reconstructed models are all in
[PLY file format](https://en.wikipedia.org/wiki/PLY_(file_format)).
