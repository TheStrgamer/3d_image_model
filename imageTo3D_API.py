import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import meshio
from tkinter import filedialog


class ImageTo3D:
    def __init__(self, image_path, reduction_factor=10, extrudeScale=5):
        if reduction_factor is None:
            reduction_factor = self.reccomendedReduction()
        self.image_path = image_path
        self.reduction_factor = reduction_factor
        self.extrudeScale = extrudeScale/25
        # Open the image and convert to black and white
        self.image = Image.open(self.image_path)
        self.image.convert("RGB")
        self.image_bw = self.image.convert('L')

    def generate_mesh(self):
        image = self.image
        image_bw = self.image_bw
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
        if image_bw.width > 1000 and image_bw.height > 1000:
            points = np.column_stack((x, y, z*(self.extrudeScale)))
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

        faces = []
        for i in range(image_bw.height - 1):
            for j in range(image_bw.width - 1):
                # First triangle
                faces.append([i * image_bw.width + j, (i + 1) * image_bw.width + j, i * image_bw.width + j + 1])

                # Second triangle
                faces.append([(i + 1) * image_bw.width + j, (i + 1) * image_bw.width + j + 1, i * image_bw.width + j + 1])

        faces = np.array(faces)
        mesh = meshio.Mesh(points=points, cells=[("triangle", faces)])
        return mesh

        # # Create a mesh using meshio
        # mesh = meshio.Mesh(points=vertices, cells=[("triangle", np.array(faces))])

        # # Save the mesh as an STL file
        # meshio.write("cube.stl", mesh)







    def export_mesh(self, filename, mesh):
        meshio.write("output.stl", mesh)

        print(f"3D model exported to {filename}")
    
    def reccomendedReduction(self):
        width = self.image.width
        height = self.image.height
        return 1000/(width*height)

def upload_file():
    #lets the user upload an image, and returns the path to the image
    f_types = [('PNG Files', '*.png'),('JPG Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    return filename
def savefile():
    #lets the user save the file
    f_types = [('STL Files', '*.stl')]
    filename = filedialog.asksaveasfilename(filetypes=f_types)
    return filename

image = Image.open("C:\Bilder\Cursed\Screenshot_20221215-015400_Instagram.jpg")

if __name__ == "__main__":
    # path="C:\Bilder\Cursed\sample_a033837ed4d8eee931e9a725dbd07c34.jpg"
    # path="ikon.png"
    #path="C:\Bilder\Cursed\RDT_20210820_0810126969680436670274982.jpg"
    path="C:\Bilder\Cursed\Screenshot_20230409-234115_Instagram.jpg"
    path=upload_file()
    imageTo3D = ImageTo3D(path, reduction_factor=10,extrudeScale=10)
    mesh_data = imageTo3D.generate_mesh()
    filename = savefile()
    imageTo3D.export_mesh(filename, mesh_data)





