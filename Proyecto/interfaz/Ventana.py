import tkinter as tk
from tkinter import messagebox
import threading
from app.controlador import detectar_pendrive










class VentanaPrincipal:
   def __init__(self, root):
       self.root = root
       self.root.title("Detector de Pendrive")
       self.root.geometry("300x150")


       self.label = tk.Label(root, text="Esperando conexión...", font=("Arial", 12))
       self.label.pack(pady=20)


       self.boton = tk.Button(root, text="Iniciar detección", command=self.iniciar_deteccion)
       self.boton.pack()


   def mostrar_mensaje(self):
       self.label.config(text="Pendrive detectado.")
       messagebox.showinfo("Éxito", "Pendrive detectado.")


   def iniciar_deteccion(self):
       self.label.config(text="Esperando que se conecte un pendrive...")
       self.boton.config(state=tk.DISABLED)


       # Inicia la detección en un hilo aparte para no congelar la interfaz
       threading.Thread(target=detectar_pendrive, kwargs={'callback': self.mostrar_mensaje}, daemon=True).start()


def lanzar_interfaz():
   root = tk.Tk()
   app = VentanaPrincipal(root)
   root.mainloop()
