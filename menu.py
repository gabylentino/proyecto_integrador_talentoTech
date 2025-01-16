from colorama import Fore, Style, init
import sqlite3

init(autoreset=True)  # Inicializar colorama

# Función para crear la base de datos y la tabla
def crear_base_datos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        categoria TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Función para agregar un producto
def agregar_producto(nombre, descripcion, categoria, cantidad, precio):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO productos (nombre, descripcion, categoria, cantidad, precio)
    VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, categoria, cantidad, precio))
    conn.commit()
    conn.close()
    print(Fore.GREEN +"\n*****************************************************************")
    print(Fore.GREEN + f"          Producto '{nombre}' agregado exitosamente.")
    print(Fore.GREEN +"\n*****************************************************************\n")

# Función para consultar inventario
def consultar_inventario():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    if productos:
        print(Fore.CYAN +"************************************************************")
        print(Fore.CYAN +"             Inventario actual:")
        print(Fore.CYAN +"************************************************************\n")
        for producto in productos:
            print(Fore.CYAN + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                  f"Categoría: {producto[3]}, Cantidad: {producto[4]}, Precio: ${producto[5]:.2f}")
            
    else:
        print(Fore.YELLOW +"**************************************************************")
        print(Fore.YELLOW +"              El inventario está vacío.")
        print(Fore.YELLOW +"************************************************************\n")

# Función para buscar producto por ID
def buscar_producto_por_id(id_producto):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
    producto = cursor.fetchone()
    conn.close()
    if producto:
        print(Fore.GREEN +"\n************************************************************************************************************************")
        print(Fore.GREEN + "            Producto encontrado:")
        print(Fore.GREEN + f"   ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
              f"Categoría: {producto[3]}, Cantidad: {producto[4]}, Precio: ${producto[5]:.2f}")
        print(Fore.GREEN +"************************************************************************************************************************\n")     
        return producto
    else:
        print(Fore.YELLOW +"\n********************************************************************")
        print( Fore.YELLOW + f"     No se encontró ningún producto con ID '{id_producto}'.")
        print(Fore.YELLOW +"********************************************************************\n")
        return None

# Función para actualizar producto
def actualizar_producto(id_producto, nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE productos
    SET nombre = ?, descripcion = ?, categoria = ?, cantidad = ?, precio = ?
    WHERE id = ?
    ''', (nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio, id_producto))
    conn.commit()
    conn.close()
    print(Fore.GREEN +"\n****************************************************************")
    print(Fore.GREEN + f"   Producto con ID {id_producto} actualizado exitosamente.")
    print(Fore.GREEN +"*****************************************************************\n")

# Función para eliminar producto
def eliminar_producto(id_producto):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Verificar si el producto existe
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
    producto = cursor.fetchone()

    if producto:
        # Si existe, eliminar el producto
        cursor.execute('DELETE FROM productos WHERE id = ?', (id_producto,))
        conn.commit()
        print(Fore.GREEN + "\n************************************************************")
        print(Fore.GREEN + f"     Producto con ID {id_producto} eliminado exitosamente.")
        print(Fore.GREEN + "*************************************************************\n")
    else:
        # Si no existe, mostrar mensaje de error
        print(Fore.YELLOW + "\n************************************************************")
        print(Fore.YELLOW + f"   Error: No existe ningún producto con ID {id_producto}.")
        print(Fore.YELLOW + "*************************************************************\n")

    conn.close()


# Función para generar reporte de productos con bajo stock
def generar_reporte_bajo_stock(limite):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad < ?', (limite,))
    productos = cursor.fetchall()
    conn.close()
    if productos:
        print(Fore.RED +"\n************************************************************")
        print(Fore.RED +"\n              Productos con bajo stock:")
        print(Fore.RED +"*************************************************************\n")

        for producto in productos:
            print( Fore.RED + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                  f"Categoría: {producto[3]}, Cantidad: {producto[4]}, Precio: ${producto[5]:.2f}")
    else:
        print(Fore.GREEN +"************************************************************")
        print(Fore.GREEN +"     No hay productos con stock crítico.") 
        print(Fore.GREEN +"************************************************************\n")

# Crear base de datos al iniciar
crear_base_datos()

# Menú del programa
print(Fore.GREEN +"************************************************************")
print("            ¡Bienvenidos!, elige la opción de gestión:")
print(Fore.GREEN +"************************************************************")
# Bucle principal del menú
while True:
    print("\n1-Alta de productos")
    print("2-Consultar inventario")
    print("3-Actualizar inventario")
    print("4-Eliminar producto")
    print("5-Buscar producto")
    print("6-Generar reporte de productos con stock critico")
    print("7. Salir\n")

    opcion = input(Fore.GREEN +"Seleccione una opción:\n ")
    if opcion == "1":
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        categoria = input("Categoría: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        agregar_producto(nombre, descripcion, categoria, cantidad, precio)

    elif opcion == "2":
        consultar_inventario()

    elif opcion == "3":
        consultar_inventario()
        try:
            id_producto = int(input("\nID del producto a actualizar: "))
            producto = buscar_producto_por_id(id_producto)
            if producto:
                nuevo_nombre = input(f"Nuevo nombre (actual: {producto[1]} o presione enter para continuar): ") or producto[1]
                nueva_descripcion = input(f"Nueva descripción (actual: {producto[2]} o presione enter para continuar): ") or producto[2]
                nueva_categoria = input(f"Nueva categoría (actual: {producto[3]} o presione enter para continuar): ") or producto[3]
                nueva_cantidad = int(input(f"Nueva cantidad (actual: {producto[4]} o presione enter para continuar): ") or producto[4])
                nuevo_precio = float(input(f"Nuevo precio (actual: {producto[5]} o presione enter para continuar): ") or producto[5])
                actualizar_producto(id_producto, nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio)
        except ValueError:
            print(Fore.YELLOW +"************************************************************")
            print(Fore.YELLOW +"    Error: Ingrese un número válido.")
            print(Fore.YELLOW +"************************************************************")

    elif opcion == "4":
        consultar_inventario()
        try:
            id_producto = int(input("\nID del producto a eliminar: "))
            eliminar_producto(id_producto)
        except ValueError:
            print(Fore.YELLOW +"************************************************************")
            print(Fore.YELLOW +"    Error: Ingrese un número válido.")
            print(Fore.YELLOW +"************************************************************")

    elif opcion == "5":
        try:
            id_producto = int(input("\nID del producto a buscar: "))
            buscar_producto_por_id(id_producto)
        except ValueError:
            print(Fore.YELLOW +"************************************************************")
            print(Fore.YELLOW +"     Error: Ingrese un número válido.")
            print(Fore.YELLOW +"************************************************************")

    elif opcion == "6":
        try:
            limite = int(input("\nIngrese el límite de stock crítico: "))
            generar_reporte_bajo_stock(limite)
        except ValueError:
            print(Fore.YELLOW +"************************************************************")
            print(Fore.YELLOW +"     Error: Ingrese un número válido.")
            print(Fore.YELLOW +"************************************************************")

    elif opcion == "7":
        print(Fore.CYAN +"************************************************************")
        print(Fore.CYAN +"     Saliendo del programa. ¡Hasta luego!")
        print(Fore.CYAN +"************************************************************")
        break

    else:
        print(Fore.YELLOW +"************************************************************")
        print(Fore.YELLOW +"     Opción no válida. Intente de nuevo.")
        print(Fore.YELLOW +"************************************************************")
