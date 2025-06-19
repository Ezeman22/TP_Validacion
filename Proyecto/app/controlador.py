# controlador.py

from .dispositivos import obtener_dispositivos_usb
def hay_nuevo_dispositivo(dispositivos_anteriores):
   dispositivos_actuales = obtener_dispositivos_usb()
   nuevos = set(dispositivos_actuales) - set(dispositivos_anteriores)
   return len(nuevos) > 0


def detectar_pendrive(callback=None):
   """Espera a que se conecte un nuevo pendrive. Llama a callback() si se detecta uno."""
   import time
   dispositivos_iniciales = obtener_dispositivos_usb()


   while True:
       if hay_nuevo_dispositivo(dispositivos_iniciales):
           if callback:
               callback()
           break
       time.sleep(1)
