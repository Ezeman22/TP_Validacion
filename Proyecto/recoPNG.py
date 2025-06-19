import os
import time
import psutil
import string
import re

def obtener_dispositivos_usb():
    """Obtiene dispositivos USB en Windows usando psutil"""
    dispositivos = []
    for part in psutil.disk_partitions(all=True):
        # En Windows, las unidades USB aparecen como discos removibles
        if 'removable' in part.opts.lower() and part.device:
            # Normalizar la ruta del dispositivo (ej: 'D:\\' -> 'D:')
            device_path = part.device.rstrip('\\')
            dispositivos.append((device_path, part.mountpoint))
    return dispositivos

def esperar_pendrive():
    print("="*60)
    print("Esperando la conexión de un pendrive...".center(60))
    print("="*60)

    dispositivos_detectados = set()

    while True:
        dispositivos_actuales = set(obtener_dispositivos_usb())
        nuevos_dispositivos = dispositivos_actuales - dispositivos_detectados

        if nuevos_dispositivos:
            dispositivo, ruta_montaje = list(nuevos_dispositivos)[0]
            print(f"\nDetectado nuevo dispositivo: {dispositivo} montado en {ruta_montaje}")
            return dispositivo  # Devuelve la letra de unidad (ej: 'D:')

        dispositivos_detectados = dispositivos_actuales
        time.sleep(2)

def buscar_y_recuperar_jpg_binario(unidad, carpeta_destino):
    """Busca archivos JPG en la unidad USB"""
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    contador = 0
    BLOCK_SIZE = 512*2  # Tamaño de bloque para escaneo

    print("\nEscaneando el dispositivo en busca de imágenes JPG...")

    try:
        # En Windows, accedemos a la unidad directamente (ej: 'D:')
        with open(f'\\\\.\\{unidad}', 'rb') as f:
            jpg_actual = bytearray()
            guardando = False

            while True:
                bloque = f.read(BLOCK_SIZE)
                if not bloque:
                    break

                if b'\xff\xd8' in bloque:  # Cabecera JPG
                    guardando = True
                    jpg_actual = bytearray()
                    inicio = bloque.find(b'\xff\xd8')
                    jpg_actual += bloque[inicio:]

                elif guardando:
                    jpg_actual += bloque

                if b'\xff\xd9' in bloque and guardando:  # Fin JPG
                    fin = bloque.find(b'\xff\xd9') + 2
                    jpg_actual = jpg_actual[:len(jpg_actual) - len(bloque) + fin]

                    nombre_archivo = os.path.join(carpeta_destino, f"recuperado_{contador}.jpg")
                    with open(nombre_archivo, 'wb') as jpg_file:
                        jpg_file.write(jpg_actual)

                    print(f"[✔] Imagen recuperada: {nombre_archivo}")
                    contador += 1
                    guardando = False

    except PermissionError:
        print("[✖] Error: Permiso denegado. Ejecuta el script como Administrador.")
    except Exception as e:
        print(f"[✖] Error: {e}")

    print(f"\nRecuperación finalizada. Total de imágenes recuperadas: {contador}")

def main():
    try:
        print("Detector de Pendrives y Recuperador de JPG - Versión Windows")
        unidad_pendrive = esperar_pendrive()  # Ejemplo: 'D:'
        carpeta_destino = os.path.expanduser("~/Recovered_JPG")
        buscar_y_recuperar_jpg_binario(unidad_pendrive, carpeta_destino)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

if __name__ == "__main__":
    main()