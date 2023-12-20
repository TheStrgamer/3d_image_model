import tkinter as tk
from imageTo3D_API import ImageTo3D
from PIL import Image, ImageTk

class ImageTo3D_UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image To 3D")
        self.window.geometry("900x500")
        self.window.resizable(False, False)
        self.window.configure(bg="#cfcfcf")
        self.ImageTo3D = ImageTo3D(reduction_factor=5, extrudeScale=1/2, inverse=True)
        self.canvas = tk.Canvas(self.window, width=500, height=500, bg="#ffffff")
        self.canvas.place(x=50, y=0)

        self.model_data=None

        # Upload File Button
        self.upload_button = tk.Button(self.window, text="Upload File", command=self.upload_file)
        self.upload_button.place(x=600, y=50)

        # Reduction Factor Input Field
        self.reduction_factor_label = tk.Label(self.window, text="Reduction Factor:")
        self.reduction_factor_label.place(x=600, y=100)
        self.reduction_factor_entry = tk.Entry(self.window)
        self.reduction_factor_entry.place(x=720, y=100)

        # Extrude Scale Input Field
        self.extrude_scale_label = tk.Label(self.window, text="Extrude Scale:")
        self.extrude_scale_label.place(x=600, y=150)
        self.extrude_scale_entry = tk.Entry(self.window)
        self.extrude_scale_entry.place(x=720, y=150)

        # Inverse Checkbox
        self.inverse_var = tk.BooleanVar()
        self.inverse_checkbox = tk.Checkbutton(self.window, text="Inverse", variable=self.inverse_var)
        self.inverse_checkbox.place(x=600, y=200)

        
        # Save Model Button
        self.gen_model_button = tk.Button(self.window, text="Generate Model", command=self.genereate_mesh)
        self.gen_model_button.place(x=600, y=250)

        self.save_model_button = tk.Button(self.window, text="Save Model", command=self.save_model)
        self.save_model_button.place(x=600, y=290)

    def upload_file(self):
        self.ImageTo3D.upload_file()
        self.image_path = self.ImageTo3D.image_path
        self.ImageTo3D.new_image(image_path=self.image_path)
        self.preview_image()
        pass

    def preview_image(self):
        if self.ImageTo3D.image_bw is not None:
            image = self.ImageTo3D.image_bw.transpose(Image.FLIP_LEFT_RIGHT)
            image = image.resize((500, 500))
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def genereate_mesh(self):
        reduction_factor = int(self.reduction_factor_entry.get())
        extrude_scale = float(self.extrude_scale_entry.get())
        inverse = self.inverse_var.get()
        if reduction_factor is None:
            reduction_factor = 10
        if extrude_scale is None:
            extrude_scale = 1/2
        if inverse is None:
            inverse = True
        self.ImageTo3D.update_inverse(inverse)
        self.ImageTo3D.update_reduction_factor(reduction_factor)
        self.ImageTo3D.update_extrude_scale(extrude_scale)
        self.model_data =self.ImageTo3D.generate_mesh()
    def save_model(self):
        # Add your code here to save the model
        if self.model_data is None:
            print("No model to save")
            return
        else:
            self.ImageTo3D.export_mesh(self.model_data)
            print("Model Saved")
            pass
        

if __name__ == "__main__":
    app = ImageTo3D_UI()
    app.window.mainloop()
        
    


