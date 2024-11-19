import tkinter as tk
from tkinter import messagebox, Toplevel
from datetime import datetime
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

# Función para obtener productos usando un procedimiento almacenado
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

# Función para obtener tipos de pago usando un procedimiento almacenado
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

# Función para agregar comanda
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
    productos_scroll = tk.Scrollbar(productos_frame)
    productos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    lista_productos = tk.Listbox(productos_frame, width=50, height=5, yscrollcommand=productos_scroll.set)
    lista_productos.pack(side=tk.LEFT, fill=tk.BOTH)
    productos_scroll.config(command=lista_productos.yview)

    # Frame para la lista de pagos con scrollbar
    pagos_frame = tk.Frame(ventana)
    pagos_frame.pack(pady=10)
    pagos_scroll = tk.Scrollbar(pagos_frame)
    pagos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    lista_pagos = tk.Listbox(pagos_frame, width=50, height=5, yscrollcommand=pagos_scroll.set)
    lista_pagos.pack(side=tk.LEFT, fill=tk.BOTH)
    pagos_scroll.config(command=lista_pagos.yview)

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

# Función para cierre de caja
def cierre_caja():
    ventana = Toplevel()
    ventana.title("Cierre de Caja")
    ventana.geometry("400x300")

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    tk.Label(ventana, text=f"Fecha: {fecha_actual}", font=("Arial", 12)).pack(pady=5)

    tk.Label(ventana, text="Total Efectivo Verificado:").pack()
    efectivo_veri_entry = tk.Entry(ventana)
    efectivo_veri_entry.pack()

    tk.Label(ventana, text="Total Tarjeta Verificado:").pack()
    tarjeta_veri_entry = tk.Entry(ventana)
    tarjeta_veri_entry.pack()

    tk.Label(ventana, text="Total Yape Verificado:").pack()
    yape_veri_entry = tk.Entry(ventana)
    yape_veri_entry.pack()

    def guardar_cierre():
        efectivo_veri = float(efectivo_veri_entry.get())
        tarjeta_veri = float(tarjeta_veri_entry.get())
        yape_veri = float(yape_veri_entry.get())
        total_veri = efectivo_veri + tarjeta_veri + yape_veri

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc("CerrarCaja", (fecha_actual, yape_veri, efectivo_veri, tarjeta_veri, total_veri))
                conn.commit()
                messagebox.showinfo("Éxito", "Cierre de caja realizado exitosamente.")
                ventana.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al realizar cierre de caja: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Guardar Cierre de Caja", command=guardar_cierre).pack(pady=10)

# Función para consultar totales por tipo de pago en un rango de fechas
def consulta_totales():
    ventana = Toplevel()
    ventana.title("Consulta de Totales por Tipo de Pago")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Fecha Inicio (YYYY-MM-DD):").pack()
    fecha_inicio_entry = tk.Entry(ventana)
    fecha_inicio_entry.pack()

    tk.Label(ventana, text="Fecha Fin (YYYY-MM-DD):").pack()
    fecha_fin_entry = tk.Entry(ventana)
    fecha_fin_entry.pack()

    resultado_frame = tk.Frame(ventana)
    resultado_frame.pack(pady=10)

    def calcular_totales():
        fecha_inicio = fecha_inicio_entry.get()
        fecha_fin = fecha_fin_entry.get()

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT codigo_tipo_de_pago, SUM(total_tipo_de_pago)
                    FROM pago_comanda
                    JOIN comanda ON pago_comanda.id_comanda = comanda.id_comanda
                    WHERE comanda.fecha_cierre_de_caja BETWEEN %s AND %s
                    GROUP BY codigo_tipo_de_pago
                """, (fecha_inicio, fecha_fin))
                totales_rango = cursor.fetchall()

                for widget in resultado_frame.winfo_children():
                    widget.destroy()

                tk.Label(resultado_frame, text="Totales por Tipo de Pago:").pack()
                for tipo_pago, total in totales_rango:
                    tipo_texto = "Efectivo" if tipo_pago == 'EFE001' else "Tarjeta" if tipo_pago == 'TAR001' else "Yape"
                    tk.Label(resultado_frame, text=f"{tipo_texto}: {total:.2f}").pack()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al consultar totales: {e}")
            finally:
                cursor.close()
                conn.close()

    tk.Button(ventana, text="Calcular Totales", command=calcular_totales).pack(pady=10)

# Configuración de la interfaz principal
root = tk.Tk()
root.title("Gestión de Comandas y Cierre de Caja")
root.geometry("300x250")

tk.Button(root, text="Agregar Comanda", command=agregar_comanda).pack(pady=10)
tk.Button(root, text="Cierre de Caja", command=cierre_caja).pack(pady=10)
tk.Button(root, text="Consulta Totales por Rango", command=consulta_totales).pack(pady=10)

root.mainloop()
