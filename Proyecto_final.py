import sqlite3
import colorama
colorama.init()

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
   )
''')
conexion.commit()
conexion.close()

def isfloat(precio):
    try:
        float(precio)
        return True
    except ValueError:
        return False
        

def muy_bajo_stock(cantidad):
    cantidad = int(cantidad)
    if cantidad < 20:
        print(colorama.Fore.YELLOW  + "La cantidad del producto es muy baja. Por favor recargue la cantidad con mas de 20."  + colorama.Style.RESET_ALL)
        return True
    else:
        return False
    
def aviso_stock_bajo(cantidad):
    cantidad = int(cantidad)
    if cantidad < 50:
        print(colorama.Fore.YELLOW + "Esta cantidad de productos es baja." + colorama.Style.RESET_ALL)
        return True
    else:
        return False
        

def registrar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    try:
        while True:
                    print(colorama.Fore.CYAN + "~~Registrar producto nuevo~~")
                    nombre = input( "Ingresa el nombre del producto: ").strip().capitalize()
                    descripcion = input( "Ingresa la descripción del producto: ").strip().capitalize()
                    precio = input( "Ingresa el precio del producto (Por favor use punto, no coma): ").strip()
                    cantidad = input( "Ingresa la cantidad de unidades del producto: ").strip()
                    categoria = input( "Ingresa la categoria del producto: "+ colorama.Style.RESET_ALL).strip().capitalize()

                    if not nombre:
                        print(colorama.Fore.RED + "[ERROR] El nombre no puede estar vacío." + colorama.Style.RESET_ALL)
                        continue
                    
                    if not isfloat(precio) or not cantidad.isdigit():
                        print(colorama.Fore.RED + "[ERROR] El precio y la cantidad deben ser digitos"+ colorama.Style.RESET_ALL)
                        continue
                    
                    if aviso_stock_bajo(cantidad):
                        continue
                    if muy_bajo_stock(cantidad):
                        continue
                    
                    else:
                        break
        

        conexion.execute("BEGIN TRANSACTION")
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria)
            VALUES (?,?,?,?,?)
        ''', (nombre, descripcion, float(precio), int(cantidad), categoria))
        
        conexion.commit()
        print(colorama.Fore.GREEN +  f"Producto {nombre} registrado correctamente" + colorama.Style.RESET_ALL)

    except sqlite3.IntegrityError:
        conexion.rollback()
        print(colorama.Fore.RED + "[ERROR] El producto ya está registrado" + colorama.Style.RESET_ALL)
    
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED +  f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
        

    finally:
        conexion.close()


def ver_lista_productos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("\nLista de productos: ")
    for producto in productos:
        print(colorama.Fore.MAGENTA +  f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)

def busqueda_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    try:
            while True:    
                    print(colorama.Fore.CYAN + "---Búsqueda de producto---")
                    print("1 ~ Buscar por ID.")
                    print("2 ~ Buscar por nombre.")
                    print("3 ~ Buscar por  categoria." + colorama.Style.RESET_ALL)
                        
                    try:
                        opcion = int(input(colorama.Fore.CYAN + "Ingresa la opcion deseada: " + colorama.Style.RESET_ALL))
            
                    except ValueError:
                        print(colorama.Fore.RED + "Por favor, ingresá un número válido." + colorama.Style.RESET_ALL)
                        continue

                    match opcion:
                        case 1:
                            try:
                                id_producto = input(colorama.Fore.MAGENTA + "Ingresá el ID del producto a buscar: " + colorama.Style.RESET_ALL).strip()
                                if not id_producto.isdigit():
                                    print(colorama.Fore.RED + "El ID debe ser numérico." + colorama.Style.RESET_ALL)
                                    return
                                
                                cursor.execute("SELECT * FROM productos WHERE id = ?",(id_producto,))
                                resultado = cursor.fetchone()
                                if resultado is None:
                                    print(colorama.Fore.RED + "El producto buscado no existe." + colorama.Style.RESET_ALL)
                                
                                else:
                                    producto = resultado 
                                    print(colorama.Fore.MAGENTA + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)
                    
                            except ValueError:
                                print(colorama.Fore.RED + "La casilla de cantidad no puede quedar vacía o con caracteres no numéricos." + colorama.Style.RESET_ALL)

                            except sqlite3.Error as e:
                                print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
                                    
                            finally:
                                conexion.close()
                                break

                        case 2:
                            try:
                                nombre_producto = input(colorama.Fore.MAGENTA + "Ingresá el nombre del producto a buscar: " + colorama.Style.RESET_ALL).strip()
                                cursor.execute("SELECT * FROM productos WHERE nombre = ?",(nombre_producto,))
                                resultado = cursor.fetchall()
                                if resultado is None:
                                    print(colorama.Fore.RED + "El producto buscado no existe." + colorama.Style.RESET_ALL)
                                else:
                                    for producto in resultado:
                                        print(colorama.Fore.MAGENTA + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)
                            

                            except sqlite3.Error as e:
                                print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
                                    
                            finally:
                                conexion.close()
                                break
                                    
                        case 3:
                            try:
                                categoria_producto = input(colorama.Fore.MAGENTA + "Ingresá el categoría del producto a buscar: " + colorama.Style.RESET_ALL).strip()
                                cursor.execute("SELECT * FROM productos WHERE categoria = ?",(categoria_producto,))
                                resultado = cursor.fetchall()
                                if resultado is None:
                                    print(colorama.Fore.RED + "El producto buscado no existe." + colorama.Style.RESET_ALL)
                                else:
                                    producto = resultado 
                                    print(colorama.Fore.MAGENTA + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)
                    

                            except sqlite3.Error as e:
                                print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
                                    
                            finally:
                                conexion.close()
                                break

    except sqlite3.Error as e:
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    finally:
            conexion.close()



def actualizar_nombre(id_producto, nuevo_nombre,):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    conexion.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nuevo_nombre, id_producto,))
        conexion.commit() 
        print(colorama.Fore.GREEN + "Nombre actualizado correctamente." + colorama.Style.RESET_ALL) 
    except ValueError:
        conexion.rollback()
        print(colorama.Fore.RED + "La casilla de nombre no puede quedar vacía" + colorama.Style.RESET_ALL)
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    
    finally:
        conexion.close()

def actualizar_descripción(id_producto, nueva_descripcion,):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    conexion.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?", (nueva_descripcion, id_producto,))
        conexion.commit() 
        print(colorama.Fore.GREEN + "Descripción actualizada correctamente." + colorama.Style.RESET_ALL) 
    except ValueError:
        conexion.rollback()
        print(colorama.Fore.RED + "La casilla de descripción no puede quedar vacía" + colorama.Style.RESET_ALL)
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    
    finally:
        conexion.close()

def actualizar_cantidad(id_producto, nueva_cantidad,):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    conexion.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto,))
        conexion.commit() 
        print(colorama.Fore.GREEN + "Cantidad actualizada correctamente." + colorama.Style.RESET_ALL) 
    except ValueError:
        conexion.rollback()
        print(colorama.Fore.RED + "La casilla de cantidad no puede quedar vacía o con caracteres no numéricos" + colorama.Style.RESET_ALL)
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    
    finally:
        conexion.close()

def actualizar_precio(id_producto, nuevo_precio,):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    conexion.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto,))
        conexion.commit() 
        print(colorama.Fore.GREEN + "Precio actualizado correctamente." + colorama.Style.RESET_ALL) 
    except ValueError:
        conexion.rollback()
        print(colorama.Fore.RED + "La casilla de precio no puede estar vacia o con caracteres no numéricos" + colorama.Style.RESET_ALL)
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    
    finally:
        conexion.close()

def actualizar_categoria(id_producto, nueva_categoria,):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    conexion.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (nueva_categoria, id_producto,))
        conexion.commit() 
        print(colorama.Fore.GREEN + "Categoría actualizada correctamente." + colorama.Style.RESET_ALL) 
    except ValueError:
        conexion.rollback()
        print(colorama.Fore.RED + "La casilla de categoría no puede quedar vacía" + colorama.Style.RESET_ALL)
    except sqlite3.Error as e:
        conexion.rollback()
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
    
    finally:
        conexion.close()

def actualizar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    id_producto = input(colorama.Fore.CYAN + "Ingresá el ID del producto a actualizar: " + colorama.Style.RESET_ALL).strip()
    if not id_producto.isdigit():
        print(colorama.Fore.RED + "El ID debe ser numérico." + colorama.Style.RESET_ALL)
        return
   
    try:    
        cursor.execute("SELECT * FROM productos WHERE id = ?",(id_producto,))
        resultado = cursor.fetchone()
        if resultado is None:
            print(colorama.Fore.RED + "El producto buscado no existe." + colorama.Style.RESET_ALL)
        else:
            print(resultado)
            while True:    
                print(colorama.Fore.CYAN + "---Actualización de datos---")
                print("1 ~ Actualizar nombre.")
                print("2 ~ Actualizar descripción.")
                print("3 ~ Actualizar cantidad.")
                print("4 ~ Actualizar precio.")
                print("5 ~ Actualizar categoria." + colorama.Style.RESET_ALL)
                
                try:
                    opcion = int(input(colorama.Fore.CYAN + "Ingresa la opcion deseada: " + colorama.Style.RESET_ALL))
    
                except ValueError:
                    print(colorama.Fore.RED + "Por favor, ingresá un número válido." + colorama.Style.RESET_ALL)
                    continue

                match opcion:
                    case 1:
                        
                        nuevo_nombre = input(colorama.Fore.CYAN + "Ingrese el nuevo nombre del producto: " + colorama.Style.RESET_ALL).strip().capitalize()
                        actualizar_nombre(id_producto, nuevo_nombre,)
                        
                        break 

                    case 2:
                        
                        nueva_descripcion = input(colorama.Fore.CYAN + "Ingrese la nueva descripción del producto: " + colorama.Style.RESET_ALL).strip().capitalize()
                        actualizar_descripción(id_producto, nueva_descripcion,)
                        break

                    case 3:
                        
                        nueva_cantidad = int(input(colorama.Fore.CYAN + "Ingrese la nueva cantidad del producto: " + colorama.Style.RESET_ALL))
                        if aviso_stock_bajo(nueva_cantidad):
                            continue
                        if muy_bajo_stock(nueva_cantidad):
                            return
                        
                        actualizar_cantidad(id_producto, nueva_cantidad,)
                        break
                
                    case 4:
                        
                        nuevo_precio = (input(colorama.Fore.CYAN + "Ingrese el nuevo precio del producto (Por favor use punto, no coma): " + colorama.Style.RESET_ALL))
                        if not isfloat(nuevo_precio):
                            print(colorama.Fore.RED + "[ERROR] El precio y la cantidad deben ser digitos" + colorama.Style.RESET_ALL)
                            return
                        
                        nuevo_precio = float(nuevo_precio)
                        actualizar_precio(id_producto, nuevo_precio,)
                        break
                
                    case 5:
                        
                        nueva_categoria = input(colorama.Fore.CYAN + "Ingrese la nueva categoría del prodcucto: " + colorama.Style.RESET_ALL).strip().capitalize()
                        actualizar_categoria(id_producto, nueva_categoria,)
                        break
                            
    except ValueError:
                    print(colorama.Fore.RED + "Por favor, ingresá un número válido." + colorama.Style.RESET_ALL)
            
    except sqlite3.Error as e:
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
        conexion.rollback()
    
    finally:
        conexion.close()
            

def eliminar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    try:
        id_producto = input(colorama.Fore.CYAN + "Ingresá el ID del producto a eliminar: " + colorama.Style.RESET_ALL).strip()
        if not id_producto.isdigit():
            print(colorama.Fore.RED + "El ID debe ser numérico." + colorama.Style.RESET_ALL)
            return 
        cursor.execute("SELECT * FROM productos WHERE id = ?",(id_producto,))
        resultado = cursor.fetchone()
        if resultado is None:
            print(colorama.Fore.RED + "El producto buscado no existe." + colorama.Style.RESET_ALL)
        else:
            producto = resultado 
            print(colorama.Fore.MAGENTA + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)
                    
            
            orden = int(input(colorama.Fore.CYAN + "Ingrese confirmación: Presione 0 para borrar.\n Presione 1 para volver al menu principal " + colorama.Style.RESET_ALL))
            if orden == 0:
                conexion.execute("BEGIN TRANSACTION")
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conexion.commit()
                print(colorama.Fore.GREEN + "El producto ha sido eliminado" + colorama.Style.RESET_ALL)

            elif orden == 1:
                print(colorama.Fore.CYAN + "Volviendo al menú principal sin modificaciones..." + colorama.Style.RESET_ALL)
                conexion.commit()

    except sqlite3.Error as e:
        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
        conexion.rollback()
        
    finally:
        conexion.close()

def reporte_stock_limite():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    try:
        limite = input(colorama.Fore.MAGENTA + "Ingresá el límite de stock: " + colorama.Style.RESET_ALL).strip()
        limite = int(limite)
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?",(limite,))
        resultado = cursor.fetchall()
        if not resultado:
            print(colorama.Fore.RED + "No hay productos con cantidad igual o inferior al límite." + colorama.Style.RESET_ALL)
            return
        else:
            for producto in resultado:
                print(colorama.Fore.RED + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: {producto[4]} | Categoría: {producto[5]} " + colorama.Style.RESET_ALL)
                    

    except sqlite3.Error as e:
                        print(colorama.Fore.RED + f"[ERROR] Error en la base de datos: {e}" + colorama.Style.RESET_ALL)
                            
    finally:
        conexion.close()
        

def menu():
     while True:   
                print(colorama.Fore.BLUE + "*~~*INVENTARIO*~~*") 
                print("*~~Menú Principal~~*")
                print("1 ~ Registrar un nuevo producto.")
                print("2 ~ Visualizar lista del inventario.")
                print("3 ~ Buscar un producto.")
                print("4 ~ Actualizar un producto.")
                print("5 ~ Eliminar un producto.")
                print("6 ~ Reporte de productos con bajo stock.")
                print("7 ~ Salir." + colorama.Style.RESET_ALL)
                
                
                try:
                    opcion = int(input(colorama.Fore.BLUE + "Ingresa la opcion deseada: " + colorama.Style.RESET_ALL))
    
                except ValueError:
                    print(colorama.Fore.RED + "Por favor, ingresá un número válido." + colorama.Style.RESET_ALL)
                    continue

                match opcion:
                    case 1:
                        registrar_producto()

                    case 2:
                        ver_lista_productos()
                                        
                    case 3:
                        busqueda_producto()
                        
                    case 4:
                        actualizar_producto()
                        
                    case 5:
                        eliminar_producto()

                    case 6:
                        reporte_stock_limite()

                    case 7:
                        break

menu()