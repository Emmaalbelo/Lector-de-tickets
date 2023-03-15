import cv2
import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

# Cargar la imagen del ticket de compra
imagen = cv2.imread("C:\\Users\\ACER Nitro 5\\Desktop\\ticket.jpg")

# Utilizar pytesseract para reconocer el texto en la imagen
texto = pytesseract.image_to_string(imagen)

# Buscar la línea del total en el texto reconocido
total = None
for linea in texto.split("\n"):
    if "total" in linea.lower():
        total = linea.split(":")[1]
        break

# total = None
# for linea in texto.split("\n"):
#     if "Total" in linea:
#         total = float(linea.split(":")[1].strip())


# Validar si se encontró el total en la imagen
if total is None:
    print("No se encontró el total en el ticket")
else:
    # Agregar el total a una hoja de cálculo de control de gastos
    df = pd.read_excel("C:\\Users\\ACER Nitro 5\\Desktop\\Gastos.xlsx")
    df = df.append({"fecha": "YYYY-MM-DD", "monto": total}, ignore_index=True)
    df.to_excel("C:\\Users\\ACER Nitro 5\\Desktop\\Gastos.xlsx", index=False)
    print("Total agregado a la hoja de cálculo de gastos")


# # Buscar el total en el texto extraído
# total = None
# for linea in texto.split("\n"):
#     if "total" in linea.lower():
#         total = linea.split(":")[1]
#         break

# # Asegurar que se encontró un total en el texto
# if total is None:
#     print("No se encontró un total en el texto.")
#     exit()

# # Crear o abrir archivo de Excel para almacenar el gasto
# df = pd.read_excel("ruta/a/tu/archivo.xlsx")

# # Agregar nueva fila con el gasto
# df = df.append({"total": total}, ignore_index=True)

# # Guardar cambios en el archivo de Excel
# df.to_excel("ruta/a/tu/archivo.xlsx", index=False)
