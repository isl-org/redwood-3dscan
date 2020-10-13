import redwood_3dscan as rws
import open3d as o3d

rws.download_mesh("00033")
mesh = o3d.io.read_triangle_mesh("data/mesh/00033.ply")
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
