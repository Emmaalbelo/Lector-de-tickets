import cv2
import pytesseract
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

class CenterWidgetMixin:
    def center (self):
        """
        Centra la ventana en la pantalla
        "WIDTHxHEIGTH+OFFSET_X+OFFSET_Y"
        de modo automatico
        w: ancho de la ventana de la aplicacion
        h: alto de la ventana de la aplicacion
        ws: ancho del monitor
        hs: altura del monitor
        """       
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry (f"{w}x{h}+{x}+{y}")


class VentanaPrincipal(tk.Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Lector de tickets")
        self.cargar_widget()
        self.total = None
        self.center()
        
    def cargar_widget(self):
        # Crear un botón para cargar la imagen
        boton_cargar = ttk.Button(self, text="Cargar ticket", command=self.cargar_imagen)
        boton_cargar.pack(padx=10, pady=10)

        # Crear una tabla para mostrar los valores obtenidos de la imagen
        self.tabla = ttk.Treeview(self, columns=("fecha", "monto"), show="headings")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("monto", text="Monto")
        self.tabla.pack(padx=10, pady=10)

        # Crear un botón para descargar los datos extraídos al Excel asociado
        boton_descargar = ttk.Button(self, text="Descargar a Excel", command=self.descargar_excel)
        boton_descargar.pack(padx=10, pady=10)

        # Crear un botón para salir de la aplicación
        boton_salir = ttk.Button(self, text="Salir", command=self.quit)
        boton_salir.pack(padx=10, pady=10)
        
    def cargar_imagen(self):
        # Abrir un diálogo de archivo para seleccionar una imagen
        filename = filedialog.askopenfilename(initialdir=".", title="Seleccionar archivo de imagen", filetypes=(("Archivos de imagen", "*.jpg;*.png;*.bmp"), ("Todos los archivos", "*.*")))
        if filename:
            # Cargar la imagen seleccionada
            imagen = cv2.imread(filename)
            # Utilizamos pytesseract para extraer el texto de la imagen
            texto = pytesseract.image_to_string(imagen)
            # Separar la información en líneas
            lineas = texto.split('\n')
            # Inicializar la variable a retornar
            self.total = None
            # Recorrer cada línea
            for linea in lineas:
                # Si la línea contiene la palabra 'total', extraer el valor del total
                if "total" in linea.lower():
                    # Si se encontró algún número, convertirlo a flotante y salir del ciclo
                    self.total = linea.split()[-1].strip()
                    break
                    
            # Validar si se encontró el total en la imagen
            if self.total is None:
                print("No se encontró el total en el ticket")
            else:
                # Agregar el total a la tabla
                fecha = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                self.tabla.insert("", tk.END, values=(fecha, self.total))
                print("Total agregado a la tabla")

    def descargar_excel(self):
        # Validar si se encontró el total en la imagen
        if self.total is None:
            print("No se encontró el total en el ticket")
        else:
            # Agregar el total a una hoja de cálculo de control de gastos
            df = pd.read_excel("C:\\Users\\ACER Nitro 5\\Desktop\\Gastos.xlsx")
            fecha = pd.Timestamp.now().strftime("%Y-%m-%d")
            df = df.append({"fecha": fecha, "monto": self.total}, ignore_index=True)
            df.to_excel("C:\\Users\\ACER Nitro 5\\Desktop\\Gastos.xlsx", index=False)
            print


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()