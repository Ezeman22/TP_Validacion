import psutil


def obtener_dispositivos_usb():
   dispositivos = []
   for part in psutil.disk_partitions(all=False):
       if 'removable' in part.opts or part.device.startswith('/dev/sd'):
           dispositivos.append(part.device)
   return dispositivos
