from tkinter import *
from tkinter import ttk
from DAO import * 
from connection import DataBase
from log import *

db = DataBase()
personaje_dao = PersonajeDAO()

ventana = Tk()
ventana.title("Ingreso de datos")
ventana.geometry("600x500")

ftos = Canvas(ventana, width=600, height=500)
ftos.pack()

img = PhotoImage(file="barco.png")
img2 = PhotoImage(file="awa.png")
img3 = PhotoImage(file="personaje.png")
img4 = PhotoImage(file="cielo.png")
img5 = PhotoImage(file="INFINITY.png")

ftos.create_image(-10, -100, anchor=NW, image=img4)
ftos.create_image(490, -5, anchor=NW, image=img5)
ftos.create_image(-100, -400, anchor=NW, image=img2)
ftos.create_image(-100, -500, anchor=NW, image=img)
ftos.create_image(510, 160, anchor=NW, image=img3)

modificar = False
personaje = StringVar()
raza = StringVar()
habilidad = StringVar()
equipamiento = StringVar()


def select(event):
    selection = tvDatos.selection()
    if selection:
        id = tvDatos.item(selection[0], "values")[0]
        if int(id) > 0:
            data = tvDatos.item(selection[0], "values")
            personaje.set(data[1])
            raza.set(data[2])
            habilidad.set(data[3])
            equipamiento.set(data[4])


marco = LabelFrame(ventana, text="Datos juego de rol")
marco.place(x=50, y=50, width=500, height=400)
marco.config(bg="beige")

lblPersonaje = Label(marco, text="Personaje", bg="saddlebrown", fg="#FFFDD0").grid(column=0, row=0, padx=5, pady=5)
txtPersonaje = Entry(marco, textvariable=personaje)
txtPersonaje.grid(column=1, row=0)

lblRaza = Label(marco, text="Raza", bg="saddlebrown", fg="#FFFDD0").grid(column=0, row=1, padx=5, pady=5)
txtRaza = ttk.Combobox(marco, values=["Orco","Demonio","Angel","No-Muerto","Humano"], textvariable=raza)
txtRaza.grid(column=1, row=1)
txtRaza.current(0)

lblHabilidad = Label(marco, text="Habilidad", bg="saddlebrown", fg="#FFFDD0").grid(column=2, row=0, padx=5, pady=5)
txtHabilidad = Entry(marco, textvariable=habilidad)
txtHabilidad.grid(column=3, row=0)

lblEquipamiento = Label(marco, text="Equipamiento", bg="saddlebrown", fg="#FFFDD0").grid(column=2, row=1, padx=5, pady=5)
txtEquipamiento = ttk.Combobox(marco, values=["C","B","A","A+","S","S+","SS"],textvariable=equipamiento)
txtEquipamiento.grid(column=3, row=1)
txtEquipamiento.current(0)

lblMensaje = Label(marco, text="Datos Ingresados", bg="saddlebrown", fg="#FFFDD0")
lblMensaje.grid(column=0, row=2, columnspan=4)

tvDatos = ttk.Treeview(marco, selectmode=NONE)
tvDatos.grid(column=0, row=3, columnspan=4, padx=5)
tvDatos["columns"] = ("ID", "PERSONAJE", "RAZA", "HABILIDAD", "EQUIPAMIENTO",)
tvDatos.column("#0", width=0, stretch=NO)
tvDatos.column("ID", width=50, anchor=CENTER)
tvDatos.column("PERSONAJE", width=100, anchor=CENTER)
tvDatos.column("RAZA", width=80, anchor=CENTER)
tvDatos.column("HABILIDAD", width=100, anchor=CENTER)
tvDatos.column("EQUIPAMIENTO", width=150, anchor=CENTER)

tvDatos.heading("#0", text="")
tvDatos.heading("ID", text="ID", anchor=CENTER)
tvDatos.heading("PERSONAJE", text="PERSONAJE", anchor=CENTER)
tvDatos.heading("RAZA", text="RAZA", anchor=CENTER)
tvDatos.heading("HABILIDAD", text="HABILIDAD", anchor=CENTER)
tvDatos.heading("EQUIPAMIENTO", text="EQUIPAMIENTO", anchor=CENTER)
tvDatos.bind("<<TreeviewSelect>>", select)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", background="saddlebrown")
style.configure("Treeview.Heading", foreground="#FFFDD0")

btnEliminar = Button(marco, text="Eliminar", command=lambda: eliminar(), bg="saddlebrown", fg="#FFFDD0")
btnEliminar.grid(column=1, row=4)
btnIngresar = Button(marco, text="Ingresar", command=lambda: validar_raza(), bg="saddlebrown", fg="#FFFDD0")
btnIngresar.grid(column=2, row=4)
btnModificar = Button(marco, text="Seleccionar", command=lambda: actualizar(), bg="saddlebrown", fg="#FFFDD0")
btnModificar.grid(column=3, row=4)

    #--------------------------FUNCIONES------------------------------
        
def validar_personaje(n_personaje):
    buscar= personaje_dao.buscar_personaje(n_personaje)
    if buscar:
        return False
    else:
        return True 

def validar_raza():
    raza=txtRaza.get()
    opc=["Orco","Demonio","Angel","No-Muerto","Humano"]
    if raza in opc:
        validar_equipamiento()
    else:
        lblMensaje.config(text="Raza invalida", bg="white",fg="red")


def validar_equipamiento():
    equipamiento = txtEquipamiento.get()
    opc= ["C","B","A","A+","S","S+","SS"]
    if equipamiento in opc:
        ingresar()  
    else:
        lblMensaje.config(text="Equipamiento invalido", bg="white",fg="red")

def vaciartabla():
    tvDatos.delete(*tvDatos.get_children())


def llenartabla():
    vaciartabla()
    personajes = personaje_dao.llenado()
    for personaje in personajes:
        tvDatos.insert("", END, values=personaje)


def eliminar():
    selection = tvDatos.selection()
    if selection:
        id = tvDatos.item(selection[0], "values")[0]
        if int(id) > 0:
            personaje_dao.borrar_personaje(id)
            tvDatos.delete(selection[0])
            lblMensaje.config(text="Datos borrados correctamente",bg="white",fg="green")
            limpiar()
    else:
        lblMensaje.config(text="Seleccione un registro para eliminar",bg="white",fg="red")


def modificarFalse():
    global modificar
    modificar = False
    tvDatos.config(selectmode=NONE)
    btnIngresar.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)


def modificarTrue():
    global modificar
    modificar = True
    tvDatos.config(selectmode=BROWSE)
    btnIngresar.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)


def ingresar():
    if modificar == False:
        if validar():
                if validar_personaje(personaje.get()):
                    personaje_obj = Datos(personaje.get(), raza.get(), habilidad.get(), equipamiento.get())
                    personaje_dao.ingreso(personaje_obj)
                    lblMensaje.config(text="Datos ingresados correctamente", fg="green")
                    llenartabla()
                    limpiar()
                else:
                    lblMensaje.config(text="El nombre del personaje ya está en la base de datos", fg="red")
        else:
            lblMensaje.config(text="-----> Hay campos vacíos <-----", fg="#FFFDD0")
    else:
        modificarFalse()


def validar():
    return len(personaje.get()) and len(habilidad.get())


def limpiar():
    personaje.set("")
    habilidad.set("")


def actualizar():
    if modificar == True:
        if validar():
            selection = tvDatos.selection()
            if selection:
                id = tvDatos.item(selection[0], "values")[0]
                personaje_obj = Datos(personaje.get(), raza.get(), habilidad.get(), equipamiento.get(), id)
                personaje_dao.actualizar_personaje(id, personaje_obj.personaje, personaje_obj.raza, personaje_obj.habilidad, personaje_obj.equipamiento)
                lblMensaje.config(text="Se ha actualizado el registro correctamente")
                llenartabla()
                limpiar()
            else:
                lblMensaje.config(text="Seleccione un registro para modificar")
        else:
            lblMensaje.config(text="-----> Hay campos vacíos <-----", fg="#FFFDD0")
    else:
        modificarTrue()


llenartabla()
ventana.mainloop()
