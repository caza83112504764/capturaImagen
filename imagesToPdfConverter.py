from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import os
import configparser
from PIL import Image
from tkinter import simpledialog
import tkinter as tk
import datetime

class ImagePDF:
    def __init__(self):
        
        self.outputs_name = ""
        self.fecha_hora_actual = ""
        
        configuracion = configparser.ConfigParser()
        configuracion.read("./config/imagesToPdfConverter.init")
        
        self.solicitarOutputName = configuracion.get('outputPdf', "solicitarNombre")
        if self.solicitarOutputName == 'True' :
            self.outputs_name = self.solicitaNombreForPdf()
            
        self.capturesPath = configuracion.get('outputPdf', 'capturesImgPath')
        self.frontal_image_name = configuracion.get('outputPdf', 'frontalImageName' )
        self.posterior_image_name = configuracion.get('outputPdf', 'posteriorImageName')
        self.frontal_image_path = self.capturesPath+self.frontal_image_name
        self.posterior_image_path = self.capturesPath+self.posterior_image_name
        print(self.posterior_image_path)
        print(self.frontal_image_path)
        self.outputs_path = configuracion.get('outputPdf', 'outputpdfPath')
        # Si en este punto la variable para el nombre no esta disponible, el nombre se trae desde el achivo de configuración
        if self.outputs_name == "":
                self.outputs_name = configuracion.get('outputPdf', 'outputPdfName')
        
        # Si agragar datetime al nombre de output esta activo
        self.agregarDatatime = configuracion.get('outputPdf', 'dateInOutputName')
        if self.agregarDatatime == "True":
            self.now = datetime.datetime.now()
            self.fecha_hora_actual = self.now.strftime("_%Y%m%d%H%M%S")
            #print(self.fecha_hora_actual)
                
        self.outputs_extension = configuracion.get('outputPdf', 'outputExtension')
        self.output_path = self.outputs_path+self.outputs_name+self.fecha_hora_actual+'.'+self.outputs_extension
        self.scale = float(configuracion.get('outputPdf', 'scaleCapture'))
        self.grayScale = configuracion.get('outputPdf', 'grayScale')
        print(self.grayScale)
        print(type(self.grayScale))
        
    def get_outputPath(self):
        return self.output_path
    
    def create_pdf(self):
        # abrir un nuevo archivo PDF
        c = canvas.Canvas(self.output_path, pagesize=letter)
        
        if not os.path.exists(self.frontal_image_path) and not os.path.exists(self.posterior_image_path) :
            img_frontal = ImageReader("./images/Imagen_no_disponible.png")
            img_posterior = ImageReader("./images/Imagen_no_disponible.png")
        else:
                      
            if self.grayScale == "True":
                img_frontal = Image.open(self.frontal_image_path).convert('L')
                img_posterior = Image.open(self.posterior_image_path).convert('L') 
                # crear objetos ImageReader a partir de las imágenes convertidas
                img_frontal = ImageReader(img_frontal)
                img_posterior = ImageReader(img_posterior)
            else:
                img_frontal = Image.open(self.frontal_image_path)
                img_posterior = Image.open(self.posterior_image_path)
                # cargar las imágenes sin conversion a grises
                img_frontal = ImageReader(img_frontal)
                img_posterior = ImageReader(img_posterior)

        # Obtener las dimensiones de las imagenes obtenidas.
        w_frontal, h_frontal = img_frontal.getSize()
        w_posterior, h_posterior = img_posterior.getSize()

        # aplicar el factor de escala a las dimensiones
        w_frontal *= self.scale
        h_frontal *= self.scale
        w_posterior *= self.scale
        h_posterior *= self.scale

        # calcular el tamaño de la página y la posición de las imágenes
        w, h = letter
        x_frontal = 2 * inch
        y_frontal = h - 0.5 * inch - h_frontal
        x_posterior = 2 * inch
        y_posterior = y_frontal - 0.5 * inch - h_posterior

        # dibujar las imágenes en la página
        c.drawImage(img_frontal, x_frontal, y_frontal, width=w_frontal, height=h_frontal)
        c.drawImage(img_posterior, x_posterior, y_posterior, width=w_posterior, height=h_posterior)
        

        # guardar y cerrar el archivo PDF
        c.save()
        # # Elimina las capturas despues de convertir, para evitar que se previsualicen en la reapertura de app.
        # if os.path.isfile(self.frontal_image_path):
        #     os.remove(self.frontal_image_path)
        # if os.path.isfile(self.posterior_image_path):
        #     os.remove(self.posterior_image_path)
            
    def solicitaNombreForPdf(self):
        # Crear una nueva ventana emergente que solicite al usuario el nombre del archivo PDF
        self.winEmergenteNombrePdf = tk.Tk()
        self.winEmergenteNombrePdf.withdraw()
        self.nombre_archivo = simpledialog.askstring(title="Guardar PDF", prompt="# de Documento para usar como nombre de archivo:")
        self.winEmergenteNombrePdf.destroy()
        

        # El nombre del archivo PDF ingresado por el usuario se almacenará en la variable 'nombre_archivo'
        print(self.nombre_archivo)
        return self.nombre_archivo
        
if __name__ == "__main__":
    imagen_pdf = ImagePDF()
    imagen_pdf.create_pdf()


