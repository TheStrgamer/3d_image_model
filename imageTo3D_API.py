import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import meshio
from tkinter import filedialog
from tqdm import tqdm


class ImageTo3D:
    def __init__(self, image_path=None, reduction_factor=None, extrudeScale=5,inverse=False):

        self.image_path = image_path


        self.mesh=None
        self.inverse=inverse
        self.bottomWidth=10*extrudeScale/25
    def new_image(self, image_path=None, reduction_factor=None, extrudeScale=None,inverse=False):

        self.image_path = image_path
        print(self.image_path)
        if image_path is None:
            self.upload_file()
        if reduction_factor is not None and reduction_factor >= 1:
            self.reduction_factor = reduction_factor
        self.extrudeScale=extrudeScale
        if extrudeScale is not None:
            self.extrudeScale = extrudeScale/25
        print(self.extrudeScale)

        # Open the image and convert to black and white
        try:
            self.image = Image.open(self.image_path)
        except:
            print("Invalid file path")
            return
        self.image.convert("RGB")
        if reduction_factor is None:
            self.reduction_factor = self.reccomendedReduction()
        self.image_bw = self.image.convert('L')
        self.mesh=None
        self.inverse=inverse
        

    def generate_mesh(self):
        image = self.image
        image_bw = self.image_bw.transpose(Image.FLIP_LEFT_RIGHT)
        if image.width//self.reduction_factor < 3 or image.height//self.reduction_factor < 3:
            print("Image too small, decrease reduction_factor")
            return
        # Reduce the size of the image by reduction factor to speed up processing
        image_bw = image_bw.resize((image.width // self.reduction_factor, image.height // self.reduction_factor))

        # Generate 3D coordinates based on color values
        x, y = np.meshgrid(range(image_bw.width), range(image_bw.height))
        z = np.array(image_bw)
        if self.inverse:
            z=255-z
        x, y, z = x.flatten(), y.flatten(), z.flatten()


        # Makes a list of points based on x, y and z, scaled to look better
        mod=1
        if image_bw.width > 1000 and image_bw.height > 1000:
            mod=1/2
        points = np.column_stack((x*mod, y*mod, z*(self.extrudeScale)+self.bottomWidth+1)) 

        verticiesCount = len(points)
        faces = []

        for i in tqdm(range(image_bw.height - 1)):
            for j in range(image_bw.width - 1):
                # First triangle
                faces.append([i * image_bw.width + j + 1, (i + 1) * image_bw.width + j, i * image_bw.width + j])

                # Second triangle
                faces.append([i * image_bw.width + j + 1, (i + 1) * image_bw.width + j + 1,(i + 1) * image_bw.width + j])
        
        bottom_points = np.column_stack((x*mod, y*mod, np.zeros_like(z)))
        # Combine top and bottom plane vertices
        points = np.concatenate((points, bottom_points))

        # Add bottom plane faces
        bottom_faces = []
        bottom_offset = len(points) - len(bottom_points)
        for i in tqdm(range(image_bw.height - 1)):
            for j in range(image_bw.width - 1):
                # Bottom plane
                bottom_faces.append([i * image_bw.width + j + bottom_offset, 
                                     (i + 1) * image_bw.width + j + bottom_offset, 
                                     i * image_bw.width + j + 1 + bottom_offset])

                bottom_faces.append([(i + 1) * image_bw.width + j + bottom_offset, 
                                     (i + 1) * image_bw.width + j + 1 + bottom_offset, 
                                     i * image_bw.width + j + 1 + bottom_offset])


        for i in tqdm(range(image_bw.height - 1)):
            #left faces
            faces.append([i * image_bw.width, i * image_bw.width + verticiesCount, (i + 1) * image_bw.width])
            faces.append([(i + 1) * image_bw.width, i * image_bw.width + verticiesCount, (i + 1) * image_bw.width + verticiesCount])
            #right faces
            faces.append([i * image_bw.width + image_bw.width - 1, i * image_bw.width + image_bw.width - 1 + verticiesCount, (i + 1) * image_bw.width + image_bw.width - 1])
            faces.append([(i + 1) * image_bw.width + image_bw.width - 1, i * image_bw.width + image_bw.width - 1 + verticiesCount, (i + 1) * image_bw.width + image_bw.width - 1 + verticiesCount])
        for i in tqdm(range(image_bw.width - 1)):
            #top faces
            faces.append([i, i + 1, i + verticiesCount])
            faces.append([i + 1, i + 1 + verticiesCount, i + verticiesCount])
            #bottom faces
            faces.append([i + image_bw.width * (image_bw.height - 1), i + image_bw.width * (image_bw.height - 1) + verticiesCount, i + 1 + image_bw.width * (image_bw.height - 1)])
            faces.append([i + 1 + image_bw.width * (image_bw.height - 1), i + image_bw.width * (image_bw.height - 1) + verticiesCount, i + 1 + verticiesCount + image_bw.width * (image_bw.height - 1)])
        # Combine top and bottom plane faces
        faces = np.concatenate((faces, bottom_faces))
        
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
        print("Reccomended reduction factor: ",round((width*height)/200000))
        return round((width*height)/200000)

    def update_reduction_factor(self, reduction_factor):
        self.reduction_factor = reduction_factor
    def update_extrude_scale(self, extrudeScale):
        self.extrudeScale = extrudeScale/25
    def update_inverse(self,inverse):
        self.inverse=inverse

    def upload_file(self):
        #lets the user upload an image, and returns the path to the image
        f_types = [('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('JPEG Files', '*.jpeg')]
        self.image_path = filedialog.askopenfilename(filetypes=f_types)

    def preview(self):
        #shows a preview of the image
        plt.imshow(self.image)
        plt.show()

if __name__ == "__main__":
    inv=True
    print("Enter the path to the image you want to convert to 3D")
    imageTo3D = ImageTo3D(reduction_factor=1,extrudeScale=1,inverse=False)
    imageTo3D.new_image(reduction_factor=1,extrudeScale=1,inverse=False)
    mesh_data = imageTo3D.generate_mesh()

    imageTo3D.export_mesh(mesh_data)





