import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import meshio
from tkinter import filedialog


class ImageTo3D:
    def __init__(self, image_path=None, reduction_factor=10, extrudeScale=5):
        if reduction_factor is None:
            reduction_factor = self.reccomendedReduction()
        self.image_path = image_path
        if image_path is None:
            self.upload_file()
        self.reduction_factor = reduction_factor
        self.extrudeScale = extrudeScale/25
        # Open the image and convert to black and white
        self.image = Image.open(self.image_path)
        self.image.convert("RGB")
        self.image_bw = self.image.convert('L')

        self.mesh=None

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

        faces = []
        for i in range(image_bw.height - 1):
            for j in range(image_bw.width - 1):
                # First triangle
                faces.append([i * image_bw.width + j, (i + 1) * image_bw.width + j, i * image_bw.width + j + 1])

                # Second triangle
                faces.append([(i + 1) * image_bw.width + j, (i + 1) * image_bw.width + j + 1, i * image_bw.width + j + 1])

        faces = np.array(faces)
        mesh = meshio.Mesh(points=points, cells=[("triangle", faces)])
        self.mesh=mesh
        return mesh


    def export_mesh(self, mesh):
        f_types = [('STL Files', '*.stl')]
        filename = filedialog.asksaveasfilename(filetypes=f_types)
        if not filename.endswith(".stl"):
            filename+=".stl"
        meshio.write(filename, mesh)

        print(f"3D model exported to {filename}")
    
    def reccomendedReduction(self):
        width = self.image.width
        height = self.image.height
        return 1000/(width*height)

    def upload_file(self):
        #lets the user upload an image, and returns the path to the image
        f_types = [('JPG Files', '*.jpg')]
        self.image_path = filedialog.askopenfilename(filetypes=f_types)

    def preview(self):
        #shows a preview of the image
        plt.imshow(self.image)
        plt.show()

if __name__ == "__main__":
    imageTo3D = ImageTo3D(reduction_factor=10,extrudeScale=10)
    mesh_data = imageTo3D.generate_mesh()
    imageTo3D.export_mesh(mesh_data)





