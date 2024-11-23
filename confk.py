import tkinter as tk
from tkinter import messagebox, Toplevel
from datetime import datetime
from tkinter import ttk
from tkinter import simpledialog
import mysql.connector

# Configuración de la conexión a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="BDregistro_ventas"
        )
        return conexion
    except mysql.connector.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None


# ============================
# Funciones de Productos
# ============================

def obtener_productos():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.callproc("ObtenerProductos")
            for resultado in cursor.stored_results():
                productos = resultado.fetchall()
            return productos
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def agregar_producto():
    ventana = Toplevel()
    ventana.title("Agregar Producto")
    ventana.geometry("300x300")

    tk.Label(ventana, text="ID del Producto:").pack(pady=5)
    id_producto_entry = tk.Entry(ventana)
    id_producto_entry.pack(pady=5)

    tk.Label(ventana, text="Descripción:").pack(pady=5)
    descripcion_entry = tk.Entry(ventana)
    descripcion_entry.pack(pady=5)

    tk.Label(ventana, text="Precio Unitario:").pack(pady=5)
    precio_entry = tk.Entry(ventana)
    precio_entry.pack(pady=5)

    def guardar_producto():
        id_producto = id_producto_entry.get().strip()
        descripcion = descripcion_entry.get().strip()
        try:
            precio = float(precio_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un precio válido.")
            return

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc("AgregarProducto", (id_producto, descripcion, precio))
                conn.commit()
                messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
                ventana.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al agregar producto: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Guardar", command=guardar_producto).pack(pady=10)

   
def eliminar_producto():
    ventana = Toplevel()
    ventana.title("Eliminar Producto")
    ventana.geometry("300x200")

    tk.Label(ventana, text="ID del Producto:").pack(pady=5)
    id_producto_entry = tk.Entry(ventana)
    id_producto_entry.pack(pady=5)

    def confirmar_eliminar():
        id_producto = id_producto_entry.get().strip()
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc("EliminarProducto", (id_producto,))
                conn.commit()
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
                ventana.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Eliminar", command=confirmar_eliminar).pack(pady=10)

def actualizar_producto():
    ventana = Toplevel()
    ventana.title("Actualizar Producto")
    ventana.geometry("300x300")

    tk.Label(ventana, text="ID del Producto:").pack(pady=5)
    id_producto_entry = tk.Entry(ventana)
    id_producto_entry.pack(pady=5)

    tk.Label(ventana, text="Nueva Descripción:").pack(pady=5)
    descripcion_entry = tk.Entry(ventana)
    descripcion_entry.pack(pady=5)

    tk.Label(ventana, text="Nuevo Precio Unitario:").pack(pady=5)
    precio_entry = tk.Entry(ventana)
    precio_entry.pack(pady=5)

    def guardar_actualizacion():
        id_producto = id_producto_entry.get().strip()
        descripcion = descripcion_entry.get().strip()
        try:
            precio = float(precio_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un precio válido.")
            return

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc("ActualizarProducto", (id_producto, descripcion, precio))
                conn.commit()
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
                ventana.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al actualizar producto: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Actualizar", command=guardar_actualizacion).pack(pady=10)

# ============================
# Funciones de Comandas
# ============================

def agregar_comanda():
    ventana = Toplevel()
    ventana.title("Agregar Comanda")
    ventana.geometry("500x700")

    # Fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    tk.Label(ventana, text=f"Fecha: {fecha_actual}", font=("Arial", 12)).pack(pady=5)

    tk.Label(ventana, text="ID de Comanda:").pack()
    id_comanda_entry = tk.Entry(ventana)
    id_comanda_entry.pack()

    productos = []
    pagos = []
    total_label = tk.Label(ventana, text="Total: 0.00")
    total_label.pack()

    # Frame para la lista de productos con scrollbar
    productos_frame = tk.Frame(ventana)
    productos_frame.pack(pady=10)

    # Scrollbars para productos
    productos_scroll_y = tk.Scrollbar(productos_frame, orient=tk.VERTICAL)
    productos_scroll_x = tk.Scrollbar(productos_frame, orient=tk.HORIZONTAL)

    # Lista de productos
    lista_productos = tk.Listbox(
        productos_frame, 
        width=50, 
        height=10, 
        yscrollcommand=productos_scroll_y.set, 
        xscrollcommand=productos_scroll_x.set
    )
    productos_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    productos_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    lista_productos.pack(side=tk.LEFT, fill=tk.BOTH)

    # Configurar scrollbars
    productos_scroll_y.config(command=lista_productos.yview)
    productos_scroll_x.config(command=lista_productos.xview)

    # Frame para la lista de pagos con scrollbar
    pagos_frame = tk.Frame(ventana)
    pagos_frame.pack(pady=10)

    # Scrollbars para pagos
    pagos_scroll_y = tk.Scrollbar(pagos_frame, orient=tk.VERTICAL)
    pagos_scroll_x = tk.Scrollbar(pagos_frame, orient=tk.HORIZONTAL)

    # Lista de pagos
    lista_pagos = tk.Listbox(
        pagos_frame, 
        width=50, 
        height=10, 
        yscrollcommand=pagos_scroll_y.set, 
        xscrollcommand=pagos_scroll_x.set
    )
    pagos_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    pagos_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    lista_pagos.pack(side=tk.LEFT, fill=tk.BOTH)

    # Configurar scrollbars
    pagos_scroll_y.config(command=lista_pagos.yview)
    pagos_scroll_x.config(command=lista_pagos.xview)

    total_pagos_label = tk.Label(ventana, text="Total Pagos: 0.00")
    total_pagos_label.pack()

    
    def agregar_producto():
        producto_ventana = Toplevel()
        producto_ventana.title("Agregar Producto")
        producto_ventana.geometry("300x200")

        productos_disponibles = obtener_productos()

        tk.Label(producto_ventana, text="Selecciona el Producto:").pack()
        producto_seleccionado = tk.StringVar(producto_ventana)
        producto_seleccionado.set("Selecciona un producto")
        producto_menu = tk.OptionMenu(producto_ventana, producto_seleccionado, *[f"{p[0]} - {p[1]} (${p[2]})" for p in productos_disponibles])
        producto_menu.pack()

        tk.Label(producto_ventana, text="Cantidad:").pack()
        cantidad_entry = tk.Entry(producto_ventana)
        cantidad_entry.pack()

        def guardar_producto():
            try:
                producto_info = producto_seleccionado.get().split(" - ")
                id_producto = producto_info[0]
                descripcion = producto_info[1].split(" ($")[0]
                cantidad = int(cantidad_entry.get())
                precio_unitario = next(p[2] for p in productos_disponibles if p[0] == id_producto)
                subtotal = cantidad * precio_unitario
                productos.append((id_producto, descripcion, cantidad, subtotal))
                lista_productos.insert(tk.END, f"{descripcion} - Cantidad: {cantidad}, Subtotal: {subtotal:.2f}")
                total_label.config(text=f"Total: {sum([p[3] for p in productos]):.2f}")
                producto_ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida.")

        tk.Button(producto_ventana, text="Guardar Producto", command=guardar_producto).pack(pady=10)

    def agregar_pago():
        pago_ventana = Toplevel()
        pago_ventana.title("Agregar Pago")
        pago_ventana.geometry("300x200")

        tipos_pago_disponibles = obtener_tipos_de_pago()

        tk.Label(pago_ventana, text="Selecciona el Tipo de Pago:").pack()
        tipo_pago_seleccionado = tk.StringVar(pago_ventana)
        tipo_pago_seleccionado.set("Selecciona un tipo de pago")
        tipo_pago_menu = tk.OptionMenu(pago_ventana, tipo_pago_seleccionado, *[f"{p[0]} - {p[1]}" for p in tipos_pago_disponibles])
        tipo_pago_menu.pack()

        tk.Label(pago_ventana, text="Monto:").pack()
        monto_entry = tk.Entry(pago_ventana)
        monto_entry.pack()

        def guardar_pago():
            try:
                tipo_pago_info = tipo_pago_seleccionado.get().split(" - ")
                codigo_tipo_pago = tipo_pago_info[0]
                nombre_pago = tipo_pago_info[1]
                monto = float(monto_entry.get())
                pagos.append((codigo_tipo_pago, nombre_pago, monto))
                lista_pagos.insert(tk.END, f"{nombre_pago}: {monto:.2f}")
                total_pagos_label.config(text=f"Total Pagos: {sum([p[2] for p in pagos]):.2f}")
                pago_ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")

        tk.Button(pago_ventana, text="Guardar Pago", command=guardar_pago).pack(pady=10)
        
    def guardar_comanda():
        id_comanda = id_comanda_entry.get()
        total_comanda = sum([p[3] for p in productos])
        if total_comanda != sum([p[2] for p in pagos]):
            messagebox.showerror("Error", "El total de pagos no coincide con el total de la comanda.")
            return

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc("VerificarOCrearFechaCierreCaja", (fecha_actual,))
                cursor.callproc("CrearComanda", (id_comanda, total_comanda, fecha_actual))
                for producto in productos:
                    id_producto, _, cantidad, subtotal = producto
                    cursor.callproc("AgregarDetalleComanda", (id_comanda, id_producto, cantidad, subtotal))
                for pago in pagos:
                    codigo_tipo_pago, _, monto = pago
                    cursor.callproc("RegistrarPagoComanda", (id_comanda, codigo_tipo_pago, monto))
                conn.commit()
                messagebox.showinfo("Éxito", "Comanda guardada exitosamente.")
                ventana.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al guardar comanda: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Agregar Producto", command=agregar_producto).pack(pady=10)
    tk.Button(ventana, text="Agregar Pago", command=agregar_pago).pack(pady=10)
    tk.Button(ventana, text="Guardar Comanda", command=guardar_comanda).pack(pady=10)

# ============================
# Funciones de Cierre de Caja
# ============================

def cierre_caja():
    ventana = Toplevel()
    ventana.title("Cierre de Caja")
    ventana.geometry("400x300")
    
    tk.Button(ventana, text="Eliminar Cierre de Caja", command=eliminar_cierre_caja).pack(pady=10)

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    tk.Label(ventana, text=f"Fecha: {fecha_actual}", font=("Arial", 12)).pack(pady=5)

    tk.Label(ventana, text="Total Efectivo Verificado:").pack()
    efectivo_veri_entry = tk.Entry(ventana)
    efectivo_veri_entry.pack()

    # Eliminar la entrada de "Total Tarjeta Verificado"
    # Si deseas ocultarlo por completo, no lo declares aquí

    tk.Label(ventana, text="Total Yape Verificado:").pack()
    yape_veri_entry = tk.Entry(ventana)
    yape_veri_entry.pack()

    def guardar_cierre():
        try:
            # Validar y obtener los valores ingresados por el usuario
            efectivo_veri = float(efectivo_veri_entry.get().strip())
            yape_veri = float(yape_veri_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos en los campos correspondientes.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                try:
                    # Llamar al procedimiento almacenado para registrar el cierre de caja
                    cursor.callproc("CerrarCaja", (fecha_actual, yape_veri, efectivo_veri, 0))  # 0 en lugar de Tarjeta Verificada manual
                    conn.commit()

                    # Llamar al procedimiento almacenado para consultar los valores del cierre de caja
                    cursor.callproc("ConsultarCierreCaja", (fecha_actual,))

                    # Recuperar los resultados del procedimiento
                    for resultado in cursor.stored_results():
                        resultados = resultado.fetchone()

                    if not resultados:
                        messagebox.showerror("Error", "No se encontraron datos para el cierre de caja en la fecha indicada.")
                        return

                    # Asignar los resultados a variables
                    yape_veri_val, efectivo_veri_val, tarjeta_veri_val, total_veri_val, \
                    yape_comanda_val, efectivo_comanda_val, tarjeta_comanda_val, total_comanda_val = resultados

                    # Actualizar los totales calculados para incluir "Tarjeta Verificada" y "Tarjeta Comanda"
                    total_veri_val = yape_veri_val + efectivo_veri_val + tarjeta_veri_val
                    total_comanda_val = yape_comanda_val + efectivo_comanda_val + tarjeta_comanda_val

                    # Crear una nueva ventana para mostrar resultados
                    resultado_ventana = Toplevel()
                    resultado_ventana.title("Resultados del Cierre de Caja")
                    resultado_ventana.geometry("450x400")

                    # Crear un marco para mostrar los resultados
                    frame = tk.Frame(resultado_ventana)
                    frame.pack(pady=10)

                    # Función para determinar el color según si los valores coinciden o no
                    def obtener_color(veri, comanda):
                        return "green" if veri == comanda else "red"

                    # Mostrar los valores en la ventana con colores
                    tk.Label(frame, text="Valores Verificados y Calculados", font=("Arial", 14, "bold")).pack(pady=5)

                    # Mostrar Yape
                    tk.Label(frame, text=f"Yape Verificado: {yape_veri_val:.2f}",
                            fg=obtener_color(yape_veri_val, yape_comanda_val)).pack(anchor="w")
                    tk.Label(frame, text=f"Yape Comanda: {yape_comanda_val:.2f}",
                            fg=obtener_color(yape_veri_val, yape_comanda_val)).pack(anchor="w")

                    # Mostrar Efectivo
                    tk.Label(frame, text=f"Efectivo Verificado: {efectivo_veri_val:.2f}",
                            fg=obtener_color(efectivo_veri_val, efectivo_comanda_val)).pack(anchor="w")
                    tk.Label(frame, text=f"Efectivo Comanda: {efectivo_comanda_val:.2f}",
                            fg=obtener_color(efectivo_veri_val, efectivo_comanda_val)).pack(anchor="w")

                    # Mostrar Tarjeta
                    tk.Label(frame, text=f"Tarjeta Verificada: {tarjeta_veri_val:.2f}",
                            fg=obtener_color(tarjeta_veri_val, tarjeta_comanda_val)).pack(anchor="w")
                    tk.Label(frame, text=f"Tarjeta Comanda: {tarjeta_comanda_val:.2f}",
                            fg=obtener_color(tarjeta_veri_val, tarjeta_comanda_val)).pack(anchor="w")

                    # Mostrar Total
                    tk.Label(frame, text=f"Total Verificado: {total_veri_val:.2f}",
                            fg=obtener_color(total_veri_val, total_comanda_val)).pack(anchor="w")
                    tk.Label(frame, text=f"Total Comanda: {total_comanda_val:.2f}",
                            fg=obtener_color(total_veri_val, total_comanda_val)).pack(anchor="w")

                except mysql.connector.Error as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"Error al realizar el cierre de caja: {e}")
            finally:
                cursor.close()
        conn.close()


    tk.Button(ventana, text="Guardar Cierre de Caja", command=guardar_cierre).pack(pady=10)



# ============================
# Gestión de Reportes de Tarjetas
# ============================

def gestionar_reporte_tarjetas():
    """
    Registra un reporte de tarjetas junto con las ventas asociadas.
    """
    ventana = Toplevel()
    ventana.title("Registrar Reporte Tarjetas")
    ventana.geometry("600x600")

    # Información automática
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    id_local = "8513875"  # ID único del local

    # Mostrar los datos automáticos
    tk.Label(ventana, text=f"Fecha: {fecha_actual}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana, text=f"ID Local: {id_local}", font=("Arial", 12)).pack(pady=5)

    # Entrada de datos del reporte
    tk.Label(ventana, text="Hora del Reporte (HH:MM:SS):").pack(pady=5)
    hora_entry = tk.Entry(ventana)
    hora_entry.pack(pady=5)

    tk.Label(ventana, text="Total Crédito (S/):").pack(pady=5)
    total_credito_entry = tk.Entry(ventana)
    total_credito_entry.pack(pady=5)

    tk.Label(ventana, text="Total Débito (S/):").pack(pady=5)
    total_debito_entry = tk.Entry(ventana)
    total_debito_entry.pack(pady=5)

    tk.Label(ventana, text="Total Soles (S/):").pack(pady=5)
    total_soles_entry = tk.Entry(ventana, state="disabled")  # Este campo es solo de lectura
    total_soles_entry.pack(pady=5)

    # Calcula automáticamente el total soles
    def actualizar_total_soles(*args):
        try:
            total_credito = float(total_credito_entry.get().strip() or 0)
            total_debito = float(total_debito_entry.get().strip() or 0)
            total_soles = total_credito + total_debito

            # Actualizar el campo de solo lectura
            total_soles_entry.config(state="normal")
            total_soles_entry.delete(0, tk.END)
            total_soles_entry.insert(0, f"{total_soles:.2f}")
            total_soles_entry.config(state="disabled")
        except ValueError:
            total_soles_entry.config(state="normal")
            total_soles_entry.delete(0, tk.END)
            total_soles_entry.config(state="disabled")

    # Eventos para actualizar automáticamente el total soles
    total_credito_entry.bind("<KeyRelease>", actualizar_total_soles)
    total_debito_entry.bind("<KeyRelease>", actualizar_total_soles)

    # Lista de ventas asociadas
    tk.Label(ventana, text="Ventas Asociadas:").pack(pady=5)
    ventas_frame = tk.Frame(ventana)
    ventas_frame.pack(fill="both", expand=True, pady=10)

    columnas = ("Ref Pago", "N° Tarjeta", "Tipo", "Monto")
    tabla_ventas = ttk.Treeview(ventas_frame, columns=columnas, show="headings", height=5)
    tabla_ventas.pack(fill="both", expand=True)
    for col in columnas:
        tabla_ventas.heading(col, text=col)
        tabla_ventas.column(col, anchor="center", width=100)

    # Botón para agregar una venta
    def agregar_venta():
        venta_ventana = Toplevel()
        venta_ventana.title("Agregar Venta Tarjeta")
        venta_ventana.geometry("400x300")

        tk.Label(venta_ventana, text="Referencia de Pago:").pack(pady=5)
        ref_pago_entry = tk.Entry(venta_ventana)
        ref_pago_entry.pack(pady=5)

        tk.Label(venta_ventana, text="N° Tarjeta (Últimos 4 dígitos):").pack(pady=5)
        num_tarjeta_entry = tk.Entry(venta_ventana)
        num_tarjeta_entry.pack(pady=5)

        tk.Label(venta_ventana, text="Tipo de Tarjeta:").pack(pady=5)
        tipo_tarjeta_seleccionado = tk.StringVar(venta_ventana)
        tipo_tarjeta_seleccionado.set("Visa")
        tipo_tarjeta_menu = tk.OptionMenu(venta_ventana, tipo_tarjeta_seleccionado, "Visa", "Mastercard", "American Express")
        tipo_tarjeta_menu.pack(pady=5)

        tk.Label(venta_ventana, text="Monto Cobrado (S/):").pack(pady=5)
        monto_entry = tk.Entry(venta_ventana)
        monto_entry.pack(pady=5)

        def guardar_venta():
            try:
                ref_pago = ref_pago_entry.get().strip()
                ultimos_digitos = num_tarjeta_entry.get().strip()
                tipo_tarjeta = tipo_tarjeta_seleccionado.get()
                monto = float(monto_entry.get().strip())

                if not ref_pago or len(ultimos_digitos) != 4 or not ultimos_digitos.isdigit() or monto <= 0:
                    raise ValueError("Datos incompletos o inválidos.")

                num_tarjeta_formateado = f"***{ultimos_digitos}"
                tabla_ventas.insert("", "end", values=(ref_pago, num_tarjeta_formateado, tipo_tarjeta, f"{monto:.2f}"))
                venta_ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa datos válidos para la venta.")

        tk.Button(venta_ventana, text="Guardar Venta", command=guardar_venta).pack(pady=10)

    tk.Button(ventana, text="Agregar Venta", command=agregar_venta).pack(pady=10)

    # Botón para guardar el reporte completo
    def guardar_reporte():
        """
        Registra un reporte de tarjetas llamando al procedimiento almacenado.
        """
        try:
            # Obtener los datos de la interfaz
            hora = hora_entry.get().strip()
            total_credito = float(total_credito_entry.get().strip())
            total_debito = float(total_debito_entry.get().strip())
            total_soles = total_credito + total_debito

            # Validar formato de hora
            datetime.strptime(hora, '%H:%M:%S')

            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                try:
                    # Llamar al procedimiento almacenado con parámetros
                    cursor.callproc("RegistrarReporteTarjetas", (
                        fecha_actual, hora, total_credito, total_debito, total_soles, fecha_actual, id_local
                    ))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Reporte registrado exitosamente.")
                    ventana.destroy()
                except mysql.connector.Error as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"Error al registrar el reporte: {e}")
                finally:
                    cursor.close()
                    conn.close()
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")




    tk.Button(ventana, text="Registrar Reporte", command=guardar_reporte).pack(pady=10)


# ============================
# Gestión de Tipos de Pago
# ============================

def obtener_tipos_de_pago():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.callproc("ObtenerTiposDePago")
            for resultado in cursor.stored_results():
                tipos_pago = resultado.fetchall()
            return tipos_pago
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al obtener tipos de pago: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


    
def eliminar_cierre_caja():
    respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el cierre de caja?")
    if not respuesta:
        return

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.callproc("EliminarCierreCaja", (fecha_actual,))
                conn.commit()
                messagebox.showinfo("Éxito", "Cierre de caja eliminado exitosamente.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al eliminar el cierre de caja: {e}")

def eliminar_comanda():
    id_comanda = simpledialog.askstring("Eliminar Comanda", "Ingresa el ID de la comanda a eliminar:")
    if not id_comanda:
        return

    with conectar_bd() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.callproc("EliminarComanda", (id_comanda,))
                conn.commit()
                messagebox.showinfo("Éxito", f"La comanda con ID {id_comanda} fue eliminada exitosamente.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al eliminar la comanda: {e}")

# Función para consultar totales por tipo de pago en un rango de fechas
def consulta_totales():
    ventana = Toplevel()
    ventana.title("Consulta de Totales por Tipo de Pago")
    ventana.geometry("400x400")

    # Entradas para rango de fechas
    tk.Label(ventana, text="Fecha Inicio (YYYY-MM-DD):").pack()
    fecha_inicio_entry = tk.Entry(ventana)
    fecha_inicio_entry.pack()

    tk.Label(ventana, text="Fecha Fin (YYYY-MM-DD):").pack()
    fecha_fin_entry = tk.Entry(ventana)
    fecha_fin_entry.pack()

    # Frame para mostrar resultados
    resultado_frame = tk.Frame(ventana)
    resultado_frame.pack(pady=10)

    # Crear Treeview para mostrar los datos
    columnas = ("Tipo de Pago", "Total")
    tabla = ttk.Treeview(resultado_frame, columns=columnas, show="headings")
    tabla.heading("Tipo de Pago", text="Tipo de Pago")
    tabla.heading("Total", text="Total")
    tabla.pack(fill="both", expand=True)

    # Ajustar columnas
    tabla.column("Tipo de Pago", anchor="center", width=150)
    tabla.column("Total", anchor="center", width=100)

    # Función para calcular y mostrar los totales
    def calcular_totales():
        # Limpiar la tabla antes de insertar nuevos datos
        for item in tabla.get_children():
            tabla.delete(item)

        fecha_inicio = fecha_inicio_entry.get().strip()
        fecha_fin = fecha_fin_entry.get().strip()

        # Validar las fechas ingresadas
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa fechas válidas en el formato YYYY-MM-DD.")
            return

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                # Llamar al procedimiento almacenado
                cursor.callproc("ConsultarTotalesPorTipoPago", (fecha_inicio, fecha_fin, None))

                # Recuperar el resultado de la consulta
                for resultado in cursor.stored_results():
                    datos = resultado.fetchall()  # Obtener todos los datos como una lista

                # Insertar los datos en la tabla
                for tipo_pago, total in datos:
                    tabla.insert("", "end", values=(tipo_pago, f"{total:.2f}"))

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al consultar totales: {e}")
            finally:
                cursor.close()
                conn.close()

    # Botón para ejecutar la consulta
    tk.Button(ventana, text="Consultar", command=calcular_totales).pack(pady=10)

           
def ver_comandas_del_dia():
    ventana = Toplevel()
    ventana.title("Comandas del Día")
    ventana.geometry("600x400")

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    tk.Label(ventana, text=f"Comandas Registradas el Día: {fecha_actual}", font=("Arial", 12)).pack(pady=10)

    # Crear Treeview para mostrar comandas
    columnas = ("ID Comanda", "Fecha", "Total")
    tabla_comandas = ttk.Treeview(ventana, columns=columnas, show="headings")
    tabla_comandas.heading("ID Comanda", text="ID Comanda")
    tabla_comandas.heading("Fecha", text="Fecha")
    tabla_comandas.heading("Total", text="Total")
    tabla_comandas.pack(fill="both", expand=True, pady=10)

    # Ajustar las columnas
    tabla_comandas.column("ID Comanda", anchor="center", width=150)
    tabla_comandas.column("Fecha", anchor="center", width=150)
    tabla_comandas.column("Total", anchor="center", width=100)

    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Llamar al procedimiento almacenado
            cursor.callproc("ConsultarComandasDelDia", (fecha_actual,))

            # Limpiar la tabla
            for item in tabla_comandas.get_children():
                tabla_comandas.delete(item)

            # Recuperar los resultados
            for resultado in cursor.stored_results():
                comandas = resultado.fetchall()

            if not comandas:
                messagebox.showinfo("Sin resultados", "No se encontraron comandas para hoy.")
            else:
                for comanda in comandas:
                    tabla_comandas.insert("", "end", values=comanda)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al consultar comandas: {e}")
        finally:
            cursor.close()
            conn.close()

          
# Configuración de la interfaz principal
root = tk.Tk()
root.title("Gestión de Comandas y Cierre de Caja")
root.geometry("300x250")

tk.Button(root, text="Agregar Comanda", command=agregar_comanda).pack(pady=10)
tk.Button(root, text="Cierre de Caja", command=cierre_caja).pack(pady=10)
tk.Button(root, text="Consulta Totales por Rango", command=consulta_totales).pack(pady=10)
tk.Button(root, text="Ver Comandas del Día", command=ver_comandas_del_dia).pack(pady=10)
tk.Button(root, text="Eliminar Comanda", command=eliminar_comanda).pack(pady=10)
tk.Button(root, text="Agregar Producto", command=agregar_producto).pack(pady=5)
tk.Button(root, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)
tk.Button(root, text="Actualizar Producto", command=actualizar_producto).pack(pady=5)
tk.Button(root, text="Gestionar Reporte Tarjetas", command=gestionar_reporte_tarjetas).pack(pady=10)



root.mainloop()