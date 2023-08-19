import numpy as np
import trimesh
import pyrender
import plotly.graph_objects as go
from pywavefront import Wavefront

if __name__ == '__main__':

    # Load the OBJ file
    file_path = r"C:\Users\ChrisUnice\Downloads\F-22 Raptor.obj"  # Replace with the actual path to your OBJ file
    obj = Wavefront(file_path, collect_faces=True, parse=True)

    # Get the vertices from the OBJ file
    vertices = np.array(obj.vertices)
    faces = np.array(obj.mesh_list[0].faces)

    # Create a dictionary to map material names to their corresponding faces
    material_faces = {}

    # Populate the dictionary with the material names and corresponding faces
    for name, material in obj.materials.items():
        material_faces[name] = []

    # Map the material names to faces of the mesh
    for i, face in enumerate(faces):
        material_name = obj.mesh_list[0].materials[i].name
        material_faces[material_name].append(face)

    # Create a pyrender.Scene object
    scene = pyrender.Scene()

    # Load and assign materials from the MTL file to each mesh
    for name, faces in material_faces.items():
        # Create a Trimesh object with the vertices and faces for this material
        mesh = trimesh.Trimesh(vertices=vertices, faces=np.vstack(faces), process=False)

        # Extract material properties from the MTL file
        material = obj.materials[name]
        color = material.ambient  # Replace with the material property you want to use (e.g., ambient, diffuse, specular)

        # Create a pyrender.Material object with the extracted material properties
        render_material = pyrender.MetallicRoughnessMaterial(baseColorFactor=color[:3] + [1.0])

        # Create a pyrender.Mesh object from the Trimesh with the current material
        render_mesh = pyrender.Mesh.from_trimesh(mesh, material=render_material)

        # Create a pyrender.Node with the mesh attached to it
        mesh_node = pyrender.Node(mesh=render_mesh)

        # Add the node to the scene
        scene.add_node(mesh_node)

    # Define the camera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)

    # Define the light
    light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=1.0)

    # Add the camera and light to the scene
    scene.add(camera, pose=np.eye(4))
    scene.add(light, pose=np.eye(4))

    # Create a pyrender.Viewer to display the scene
    viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

    # Render the scene and capture the image as a NumPy array
    image = viewer.render(render_flags=pyrender.RenderFlags.RGBA)

    # Convert the image to a Plotly figure
    plotly_fig = go.Figure(data=[go.Image(z=image)])

    # Set the axis labels
    plotly_fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

    # Show the plot
    plotly_fig.show()
