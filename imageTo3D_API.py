import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay
import numpy as np
from stl import mesh
from PIL import Image
import meshio


class ImageTo3D:
    def __init__(self, image_path, reduction_factor=10, extrudeScale=5):
        self.image_path = image_path
        self.reduction_factor = reduction_factor
        self.extrudeScale = extrudeScale/25

    def generate_mesh(self):
        # Open the image and convert to black and white
        image = Image.open(self.image_path)
        image.convert("RGB")
        image_bw = image.convert('L')
        if image.width//self.reduction_factor < 3 or image.height//self.reduction_factor < 3:
            print("Image too small, decrease reduction_factor")
            return
        # Reduce the size of the image by reduction factor to speed up processing
        image_bw = image_bw.resize((image.width // self.reduction_factor, image.height // self.reduction_factor))

        # Generate 3D coordinates based on color values
        x, y = np.meshgrid(range(image_bw.width), range(image_bw.height))
        z = np.array(image_bw)
        x, y, z = x.flatten(), y.flatten(), z.flatten()


        # Makes a list of points based on x, y and z, scaled to look better
        points = np.column_stack((x*5, y*5, z*(self.extrudeScale))) 

        with open("points.txt", "w") as f:
            for point in points:
                f.write(f"{point[0]} {point[1]} {point[2]}\n")

        #preview the points
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim([0, image_bw.width*5])
        ax.set_ylim([0, image_bw.height*5])
        ax.set_zlim([0, 255])
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b', marker='.')

        # Set axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Show the plot
        plt.show()

        face_count = (image_bw.width-1) * (image_bw.height-1) * 2
        
        faces = np.zeros((face_count, 3), dtype=int)
        
        #TODO make an algorithm that makes the faces based on the points
        #husk, for å finne trekanten er det punkt i, i+1, i+width

        for i in range(image_bw.height-1):
            for j in range(image_bw.width-1):
                faces[i*2+j] = [i*image_bw.width+j, i*image_bw.width+j+1, (i+1)*image_bw.width+j]
                faces[i*2+j+1] = [(i+1)*image_bw.width+j, i*image_bw.width+j+1, (i+1)*image_bw.width+j+1]
        faces = np.array(faces)
        print(faces)
        print(image_bw.width, image_bw.height)
        mesh = meshio.Mesh(points=points, cells=[("triangle", faces)])
        meshio.write("output.stl", mesh)

        # # Create a mesh using meshio
        # mesh = meshio.Mesh(points=vertices, cells=[("triangle", np.array(faces))])

        # # Save the mesh as an STL file
        # meshio.write("cube.stl", mesh)







    def export_mesh(self, mesh_data, filename):
        # Save the mesh as an STL file
        mesh_data.save(filename)

        print(f"3D model exported to {filename}")
image = Image.open("C:\Bilder\Cursed\Screenshot_20221215-015400_Instagram.jpg")

if __name__ == "__main__":
    path="ikon.png"
    path="C:\Bilder\Cursed\sample_a033837ed4d8eee931e9a725dbd07c34.jpg"
    path="C:\Bilder\Cursed\RDT_20210820_0810126969680436670274982.jpg"
    imageTo3D = ImageTo3D(path, reduction_factor=10,extrudeScale=10)
    mesh_data = imageTo3D.generate_mesh()


    #imageTo3D.export_mesh(mesh_data, "output.stl")



# import meshio
# import numpy as np

# # Define the vertices of a cube
# vertices = np.array([
#     [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Bottom face
#     [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # Top face
# ])

# # Define the six faces of the cube using vertex indices
# faces = [
#     [0, 1, 5], [0, 5, 4],
#     [1, 2, 6], [1, 6, 5],
#     [2, 3, 7], [2, 7, 6],
#     [3, 0, 4], [3, 4, 7],
#     [0, 3, 2], [0, 2, 1],
#     [4, 5, 6], [4, 6, 7]
# ]

# # Create a mesh using meshio
# mesh = meshio.Mesh(points=vertices, cells=[("triangle", np.array(faces))])

# # Save the mesh as an STL file
# meshio.write("cube.stl", mesh)


