import tkinter as tk
from tkinter import ttk, messagebox
from clases.usuarios import Usuarios

class FrmUsuarios:
    def __init__(self, parent, NombreCompleto, email, rol):
        self.tipo_action = "Guardar"
        self.tipo_user = ""
        self.nombre_completo = NombreCompleto
        self.email = email
        self.rol = rol
        self.usuario_seleccionado_id = None  

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        
        tk.Label(self.frame, text=f"Sesión activa: {self.nombre_completo}", font=('Times', 12)).place(x=500, y=30)
        tk.Label(self.frame, text=f"Email: {self.email}", font=('Times', 12)).place(x=500, y=55)
        tk.Label(self.frame, text=f"Rol: {self.rol}", font=('Times', 12)).place(x=500, y=80)

        tk.Label(self.frame, text="Registro de usuarios", font=('Times', 16)).place(x=70, y=30)

        
        tk.Label(self.frame, text="Nombre", font=('Times', 14)).place(x=70, y=130)
        self.cnombre = tk.Entry(self.frame, width=40)
        self.cnombre.place(x=220, y=130)

        
        tk.Label(self.frame, text="Apellido", font=('Times', 14)).place(x=70, y=160)
        self.capellido = tk.Entry(self.frame, width=40)
        self.capellido.place(x=220, y=160)

        
        tk.Label(self.frame, text="Username", font=('Times', 14)).place(x=70, y=190)
        self.cusuario = tk.Entry(self.frame, width=40)
        self.cusuario.place(x=220, y=190)

        
        tk.Label(self.frame, text="Contraseña", font=('Times', 14)).place(x=500, y=100)
        self.ccontrasena = tk.Entry(self.frame, width=40, show="*")
        self.ccontrasena.place(x=600, y=100)

        
        tk.Label(self.frame, text="Correo", font=('Times', 14)).place(x=500, y=130)
        self.ccorreo = tk.Entry(self.frame, width=40)
        self.ccorreo.place(x=600, y=130)

        
        tk.Label(self.frame, text="Rol", font=('Times', 14)).place(x=500, y=160)
        self.ctipo = ttk.Combobox(self.frame, width=40)
        self.ctipo.place(x=600, y=160)
        self.ctipo["values"] = ("Admin", "Vendedor", "Usuario")

        
        tk.Button(self.frame, text="Guardar", font=('Times', 14), command=self.guardar_usuario).place(x=70, y=220)
        tk.Button(self.frame, text="Actualizar", font=('Times', 14), command=self.actualizar_usuarios).place(x=170, y=220)
        tk.Button(self.frame, text="Eliminar", font=('Times', 14), command=self.eliminar_usuarios).place(x=270, y=220)

        self.listar_usuarios()

    def listar_usuarios(self):
        tk.Label(self.frame, text="LISTADO DE USUARIOS", font=('Times', 16)).place(x=70, y=260)

        self.tablausuarios = ttk.Treeview(self.frame, columns=("Nombre", "Apellido", "Username", "Email", "Rol"))
        self.tablausuarios.heading("#0", text="ID")
        self.tablausuarios.heading("Nombre", text="Nombre")
        self.tablausuarios.heading("Apellido", text="Apellido")
        self.tablausuarios.heading("Username", text="Username")
        self.tablausuarios.heading("Email", text="Email")
        self.tablausuarios.heading("Rol", text="Rol")
        self.tablausuarios.place(x=70, y=300)

        
        self.tablausuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.tablausuarios.delete(*self.tablausuarios.get_children())
        usuarios = Usuarios()
        sql = "SELECT id, nombre, apellido, username, email, rol FROM usuarios"
        resultado = usuarios.db.select(sql)
        if resultado:
            for fila in resultado:
                self.tablausuarios.insert("", "end", text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5]))

    def seleccionar_usuario(self, event):
        selected = self.tablausuarios.selection()
        if selected:
            item = self.tablausuarios.item(selected[0])
            self.usuario_seleccionado_id = item["text"]  # El ID
            nombre, apellido, username, email, rol = item["values"]

            self.cnombre.delete(0, tk.END)
            self.cnombre.insert(0, nombre)

            self.capellido.delete(0, tk.END)
            self.capellido.insert(0, apellido)

            self.cusuario.delete(0, tk.END)
            self.cusuario.insert(0, username)

            self.ccorreo.delete(0, tk.END)
            self.ccorreo.insert(0, email)

            self.ctipo.set(rol)
            self.ccontrasena.delete(0, tk.END)

    def guardar_usuario(self):
        nombre = self.cnombre.get()
        apellido = self.capellido.get()
        username = self.cusuario.get()
        clave = self.ccontrasena.get()
        email = self.ccorreo.get()
        rol = self.ctipo.get()

        usuarios = Usuarios()
        exito = usuarios.registrar_usuario(nombre, apellido, email, username, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.limpiar_campos()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo guardar el usuario")

    def actualizar_usuarios(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para actualizar.")
            return

        nombre = self.cnombre.get()
        apellido = self.capellido.get()
        username = self.cusuario.get()
        clave = self.ccontrasena.get()
        email = self.ccorreo.get()
        rol = self.ctipo.get()

        if not all([nombre, apellido, username, email, rol]):
            messagebox.showwarning("Advertencia", "Todos los campos deben estar completos (excepto contraseña).")
            return

        usuarios = Usuarios()
        if clave:
            sql = """UPDATE usuarios SET nombre=%s, apellido=%s, username=%s, email=%s, rol=%s, clave=%s WHERE id=%s"""
            parametros = (nombre, apellido, username, email, rol, clave, self.usuario_seleccionado_id)
        else:
            sql = """UPDATE usuarios SET nombre=%s, apellido=%s, username=%s, email=%s, rol=%s WHERE id=%s"""
            parametros = (nombre, apellido, username, email, rol, self.usuario_seleccionado_id)

        exito = usuarios.db.execute_query(sql, parametros)
        if exito:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            self.limpiar_campos()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.")

    def eliminar_usuarios(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm:
            usuarios = Usuarios()
            sql = "DELETE FROM usuarios WHERE id = %s"
            parametros = (self.usuario_seleccionado_id,)
            exito = usuarios.db.execute_query(sql, parametros)
            if exito:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                self.limpiar_campos()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def limpiar_campos(self):
        campos = [self.cnombre, self.capellido, self.cusuario, self.ccontrasena, self.ccorreo]
        for campo in campos:
            campo.delete(0, tk.END)
        self.ctipo.set('')
        self.usuario_seleccionado_id = None
