from tkinter import *
from tkinter import messagebox
from DAO import UsuarioDAO
import os


usuario_dao = UsuarioDAO()

ventana=Tk()
ventana.title("")
ventana.geometry("600x400")


img=PhotoImage(file="fondofinal.png")
imgf=Label(ventana,image=img)
imgf.place(x=0,y=0)

frame = Frame(ventana)
frame.pack(pady=50)


txtUsuario=Label(text="Usuario",bg="goldenrod")
lblUsuario = Entry(ventana)

txtContraseña=Label(text="Contraseña",bg="goldenrod")
lblContraseña = Entry(ventana, show="*")
btnRegistrar = Button(ventana, text="Registrar", command=lambda:registrar(),bg="goldenrod")
btnLogin = Button(ventana, text="Iniciar Sesion", command=lambda:login(),bg="goldenrod")

txtUsuario.pack(pady=1)
lblUsuario.pack(pady=1)
txtContraseña.pack(pady=1)
lblContraseña.pack(pady=1)
btnRegistrar.pack(pady=1)
btnLogin.pack(pady=1)


def registrar():
    usuario = lblUsuario.get()
    contraseña = lblContraseña.get()

    registrado = usuario_dao.registrar_usuario(usuario, contraseña)

    if registrado:
        messagebox.showinfo("Registro", "Registro exitoso")
        exit()

    else:
        messagebox.showerror("Error", "El usuario ya existe")

def login():
    usuario = lblUsuario.get()
    contraseña = lblContraseña.get()

    logueado = usuario_dao.login_usuario(usuario, contraseña)

    if logueado:
        if usuario == "admin" and contraseña=="12345":
            ventana.destroy()
            os.system("main.py")

        else:
            messagebox.showinfo("bienvenido","BIENVENIDO")
            exit()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")



ventana.mainloop()



