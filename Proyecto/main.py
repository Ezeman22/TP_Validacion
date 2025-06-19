import sys
from app.controlador import detectar_pendrive
from interfaz.Ventana import lanzar_interfaz


def mostrar_mensaje():
   print("Pendrive detectado.")


def main():
   if len(sys.argv) > 1 and sys.argv[1] == "gui":
       lanzar_interfaz()
   else:
       print("Conecte un pendrive...")
       detectar_pendrive(callback=mostrar_mensaje)


if __name__ == "__main__":
   main()
