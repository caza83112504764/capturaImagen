import tkinter as tk
from PIL import ImageTk, Image
import cv2
import imutils
import os
from imagesToPdfConverter import ImagePDF
from webcamsDisponibles import WebCams
#import webcamsDisponibles


class WebcamCapture:
    def __init__(self, master):
        self.master = master
        self.master.title("Capturador de Documentos desde la Webcam")
        self.master.geometry("652x685")
        
        # Creando un menu para la aplicacion.
        self.menuPrincipal = tk.Menu(self.master)
        self.menuPrincipal.add_command(label='Salir')

        # Creando un menu desplegable para seleccionar la webcam.
        self.desplegableWebcams = tk.Menu(self.menuPrincipal)
        self.desplegableWebcams.add_command(label='1')
        self.desplegableWebcams.add_command(label='2')
        self.desplegableWebcams.add_command(label='3')
        self.menuPrincipal.add_cascade(label='Webcams', menu=self.desplegableWebcams)
        
        # Muestra el menu principal en la ventana principal.
        self.master.config(menu=self.menuPrincipal)

        self.image_dir = "./captures"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        self.crear_frames()
        self.create_widgets()

        ###########################################################################
        ###########################################################################
        ###########################################################################
        self.cap = cv2.VideoCapture(4)
        ###########################################################################
        ###########################################################################
        ###########################################################################
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        self.mostrar_imagen_frontal()
        self.mostrar_imagen_posterior()

        self.update()
        
    def crear_frames(self):
        self.frame_superior = tk.Frame(self.master, width=650, height=480, bg="black")
        self.frame_superior.pack(expand=True,anchor="se")
        
        self.frame_inferior = tk.Frame(self.master,width=650, height=200)
        self.frame_inferior.pack(side="bottom")

    def create_widgets(self):
        
        self.canvas_video = tk.Canvas(self.frame_superior, width=650, height=490)
        self.canvas_video.grid(column=0, row=0)
        #self.canvas.pack()
        
        self.frame_prev_frontal = tk.Frame(self.frame_inferior, width=215, height=190, bg="black")
        self.frame_prev_frontal.grid(column=0, row=1)
        #self.canvas.pack()
        
        self.frame_prev_posterior = tk.Frame(self.frame_inferior, width=215, height=190, bg="blue")
        self.frame_prev_posterior.grid(column=1, row=1)
        #self.canvas.pack()
        
        self.frame_botones = tk.Frame(self.frame_inferior, width=128, height=190, bg="#b4b8b5")
        self.frame_botones.grid(column=2, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
        #self.canvas.pack()
    
    ## Creando  canvas y posicionando dentro de los respectivos frame (frontal y posterior)    
        self.canvas_capture_frontal = tk.Canvas(self.frame_prev_frontal, width=250, height=190)
        # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
        #self.canvas_capture_frontal.create_rectangle(0, 0, self.canvas_capture_frontal.winfo_width(), self.canvas_capture_frontal.winfo_height(), outline="red", width=10)
        # Posicionar el canvas dentro del frame.
        self.canvas_capture_frontal.grid(column=0,row=1, sticky=tk.N)
        #self.canvas_capture_frontal.pack()
        
        self.canvas_capture_posterior = tk.Canvas(self.frame_prev_posterior, width=250, height=190)
        self.canvas_capture_posterior.grid(column=1, row=1, sticky=tk.N)
        #self.canvas_capture_posterior.pack()
        
        
    ## Crear botones y posicionarlos dentro de frame_botones
        self.btn_capture_frontal = tk.Button(self.frame_botones, text="Captura frontal", command=self.capture_frontal)
        self.btn_capture_frontal.grid(column=2, row=1, sticky="nsew")
        #self.btn_capture.pack()
        
        self.btn_capture_posterior = tk.Button(self.frame_botones, text="Capturar posterior", command=self.capture_posterior)
        self.btn_capture_posterior.grid(column=2, row=2, sticky="nsew")
        #self.btn_capture.pack()
        
        self.btn_imgToPdf = tk.Button(self.frame_botones, text="Convertir a PDF", command=self.imgToPdf)
        self.btn_imgToPdf.grid(column=2, row=3, sticky="nsew")
        
        self.tamanio_btn_verPdf = (120, 90)
        self.icono_pdf = tk.PhotoImage(file="./images/ver-pdf.png")
        self.btn_verPdf = tk.Button(self.frame_botones, width=self.tamanio_btn_verPdf[0], height=self.tamanio_btn_verPdf[1], text="Ver PDF", image=self.icono_pdf, command=self.verPdf )
        self.btn_verPdf.grid(column=2, row=4, sticky="nsew")
        self.btn_verPdf.config(state='disabled')   
        
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ancho_canvas_video = self.canvas_video.winfo_width()
            factor_escala = ancho_canvas_video / frame.shape[1]
            nuevo_ancho = int(frame.shape[1] * factor_escala)
            nuevo_alto = int(frame.shape[0] * factor_escala)
            #print(nuevo_alto)
            if nuevo_ancho > 0 and nuevo_alto > 0:
                frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_LINEAR)
                img = Image.fromarray(frame)
                
                photo = ImageTk.PhotoImage(image=img)
                self.canvas_video.create_image(0,0, anchor=tk.NW , image=photo)
                self.canvas_video.photo = photo
                # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
                self.canvas_video.create_rectangle(0, 0, self.canvas_video.winfo_width(), self.canvas_video.winfo_height(), outline="blue", width=10)
        self.master.after(500, self.update)
    
    def agregar_texto_ayuda(self, img, posicion, texto_ayuda):
        # Crear el texto de ayuda
        self.texto_ayuda = texto_ayuda#'Clic izq sostenido + arrastrar = seleccionar el recorte.\n'
        #texto2 = "'ENTER' para capturar el recorte\nPresione 'c' para cancelar y salir."
        #ayuda = texto1 + texto2
        self.posicion = posicion
        self.img = img
        self.x = posicion[0]
        self.y = posicion[1]
        
        # Configurar los parámetros del texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        escala = 0.6
        color = (18, 2, 199)
        grosor = 2
        
        # Obtener el tamaño del texto
        (ancho, alto), _ = cv2.getTextSize(texto_ayuda, font, escala, grosor)
        
        espacio = 2
        y2 = self.y + alto + espacio
        
        # Dibujar el fondo del texto
        cv2.rectangle(self.img, (self.x, self.y), (self.x + ancho, y2), (255, 255, 255), cv2.FILLED)
        
        # Agregar el texto a la imagen
        cv2.putText(self.img, texto_ayuda, (self.x, y2), font, escala, color, grosor)
        
        return self.img
    
    def capture_frontal(self):
        ret, frame = self.cap.read()
        if ret:
            # Seleccionar el ROI con el mouse
            clone = frame.copy()
            cv2.namedWindow("Selecciona el recorte adverso.")
            clone = self.agregar_texto_ayuda(clone, (5, 5),"Clic IZQ sostenido + Arrastrar = Seleccionar el recorte.") # Agregar el texto de ayuda
            clone = self.agregar_texto_ayuda(clone, (5, 25),"'ENTER' = Capturar recorte y Salir.") # Agregar el texto de ayuda
            clone = self.agregar_texto_ayuda(clone, (5, 45),"'C' = Cancelar y Salir.") # Agregar el texto de ayuda
            # Garantiza que la ventana de selecion ROI se muestre arriba
            #cv2.setWindowProperty("Selecciona el recorte adverso.", cv2.WND_PROP_TOPMOST, cv2.WINDOW_FULLSCREEN)
            r = cv2.selectROI("Selecciona el recorte adverso.", clone, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Selecciona el recorte adverso.")
            
            # Recortar la imagen original usando el ROI seleccionado
            (x, y, w, h) = r
            recorte = frame[y:y+h, x:x+w]
            
            # Guardar la imagen recortada en el directorio correspondiente
            if recorte.shape[0] > 0 and recorte.shape[1] > 0:
                filename = "capture_frontal.png"
                filepath = os.path.join(self.image_dir, filename)
                cv2.imwrite(filepath, recorte)
            
    def capture_posterior(self):
        ret, frame = self.cap.read()
        if ret:
            # Seleccionar el ROI con el mouse
            clone = frame.copy()
            cv2.namedWindow("Selecciona el recorte para el reverso.")
            clone = self.agregar_texto_ayuda(clone, (5, 5),"Clic IZQ sostenido + Arrastrar = seleccionar el recorte.") # Agregar el texto de ayuda
            clone = self.agregar_texto_ayuda(clone, (5, 25),"'ENTER' = Capturar recorte y Salir.") # Agregar el texto de ayuda
            clone = self.agregar_texto_ayuda(clone, (5, 45),"'C' para Cancelar y Salir.") # Agregar el texto de ayuda
            # Garantiza que la ventana de selecion ROI se muestre arriba
            #cv2.setWindowProperty("Selecciona el recorte para el reverso.", cv2.WND_PROP_TOPMOST, cv2.WINDOW_FULLSCREEN)
            r = cv2.selectROI("Selecciona el recorte para el reverso.", clone, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Selecciona el recorte para el reverso.")
            
            # Recortar la imagen original usando el ROI seleccionado
            (x, y, w, h) = r
            recorte = frame[y:y+h, x:x+w]
            
            # Guardar la imagen recortada en el directorio correspondiente
            if recorte.shape[0] > 0 and recorte.shape[1] > 0:
                filename = "capture_posterior.png"
                filepath = os.path.join(self.image_dir, filename)
                cv2.imwrite(filepath, recorte)
            
    def mostrar_imagen_frontal(self):
        
        if os.path.isfile("./captures/capture_frontal.png"):
            imagen = Image.open("./captures/capture_frontal.png")
            imagen = imagen.resize((250, 190), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            # Elimina la imagen anterior del canvas
            self.canvas_capture_frontal.delete(tk.ALL)
            # Agragar la nueva imagen al canvas.
            self.canvas_capture_frontal.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            # Actualiza la referencia a la imagen actual en el canvas
            self.canvas_capture_frontal.imagen_tk = imagen_tk
            # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
            self.canvas_capture_frontal.create_rectangle(0, 0, self.canvas_capture_frontal.winfo_width(), self.canvas_capture_frontal.winfo_height(), outline="blue", width=10)
        else:
            # Si el archivo no existe, muestra una imagen de reemplazo o un mensaje de error
            imagen_reemplazo = Image.new("RGB", (250, 190), color="white")
            imagen_tk = ImageTk.PhotoImage(imagen_reemplazo)
            self.canvas_capture_frontal.delete(tk.ALL)
            self.canvas_capture_frontal.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            self.canvas_capture_frontal.imagen_tk = imagen_tk
            # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
            self.canvas_capture_frontal.create_rectangle(0, 0, self.canvas_capture_frontal.winfo_width(), self.canvas_capture_frontal.winfo_height(), outline="blue", width=10)
            #print("Error: El archivo capture_frontal.png no existe.")
               
        # Configura una llamada a la función cada 100 ms para actualizar la imagen en el canvas
        self.master.after(500, self.mostrar_imagen_frontal)
        
    def mostrar_imagen_posterior(self):
        # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
        self.canvas_capture_posterior.create_rectangle(0, 0, self.canvas_capture_posterior.winfo_width(), self.canvas_capture_posterior.winfo_height(), outline="blue", width=10)
        if os.path.isfile("./captures/capture_posterior.png"):
            imagen = Image.open("./captures/capture_posterior.png")
            imagen = imagen.resize((250, 190), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            # Elimina la imagen anterior del canvas
            self.canvas_capture_posterior.delete(tk.ALL)
            # Agragar la nueva imagen al canvas.
            self.canvas_capture_posterior.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            # Actualiza la referencia a la imagen actual en el canvas
            self.canvas_capture_posterior.imagen_tk = imagen_tk
            # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
            self.canvas_capture_posterior.create_rectangle(0, 0, self.canvas_capture_posterior.winfo_width(), self.canvas_capture_posterior.winfo_height(), outline="blue", width=10)
        else:
            # Si el archivo no existe, muestra una imagen de reemplazo o un mensaje de error
            imagen_reemplazo = Image.new("RGB", (250, 190), color="white")
            imagen_tk = ImageTk.PhotoImage(imagen_reemplazo)
            self.canvas_capture_posterior.delete(tk.ALL)
            self.canvas_capture_posterior.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            self.canvas_capture_posterior.imagen_tk = imagen_tk
            #print("Error: El archivo capture_posterior.png no existe.")
            # Crea un borde alrededor del canvas con un ancho de línea de 2 píxeles y color rojo
            self.canvas_capture_posterior.create_rectangle(0, 0, self.canvas_capture_posterior.winfo_width(), self.canvas_capture_posterior.winfo_height(), outline="blue", width=10)
               
        # Configura una llamada a la función cada 100 ms para actualizar la imagen en el canvas
        self.master.after(500, self.mostrar_imagen_posterior) 

    def imgToPdf(self):
        self.convertirToPdf = ImagePDF()
        self.convertirToPdf.create_pdf()
        self.normalizar_btn_verPdf()    
        
    def normalizar_btn_verPdf(self):
        self.path_output = self.convertirToPdf.get_outputPath()
        if not os.path.exists(self.path_output):
            self.btn_verPdf.config(state='disabled')
        else:
            self.btn_verPdf.config(state='normal')

    def verPdf(self):
        self.path_output = self.convertirToPdf.get_outputPath()
        if os.path.exists(self.path_output):
            print("Mostrando PDF.")
            os.system('firefox '+self.path_output)
        else:
            print("Sin documento para mostrar.")
            
class EliminarCapturas:
    def __init__(self, dirCapturas):
        self.dirCapturas = dirCapturas
        for archivo in os.listdir(self.dirCapturas):
            ruta_archivo = os.path.join(self.dirCapturas, archivo)
            os.remove(ruta_archivo)
        
def main():
    root = tk.Tk()
    app = WebcamCapture(root)
    root.mainloop()
    eliminar = EliminarCapturas('./captures')

if __name__ == '__main__':
    main()
