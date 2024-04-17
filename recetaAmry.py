import sqlite3
from datetime import datetime

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('receta.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def crear_tabla(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS receta (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ingredientes (
                            id INTEGER PRIMARY KEY,
                            receta_id INTEGER NOT NULL,
                            ingrediente TEXT NOT NULL,
                            cantidad TEXT,
                            FOREIGN KEY(receta_id) REFERENCES receta(id)
                        );''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def añadir_receta(conn, nombre):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO receta (nombre) VALUES (?)", (nombre,))
    conn.commit()
    return cursor.lastrowid

def actualizar_receta(conn, receta_id, nombre):
    cursor = conn.cursor()
    cursor.execute("UPDATE receta SET nombre = ? WHERE id = ?", (nombre, receta_id))
    conn.commit()

def borrar_receta(conn, receta_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receta WHERE id = ?", (receta_id,))
    cursor.execute("DELETE FROM ingredientes WHERE receta_id = ?", (receta_id,))
    conn.commit()

def ver_receta(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receta")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def buscar_ingredientes(conn, receta_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingredientes WHERE receta_id = ?", (receta_id,))
    ingredientes = cursor.fetchall()
    print("Ingredientes:")
    for ingredientes in ingredientes:
        print(ingredientes)

def main():
    conn = create_connection()
    crear_tabla(conn)

    while True:
        print("\nOpcciones disponibles:")
        print("a) Añada una nueva receta")
        print("b) Actualice una receta")
        print("c) Borre una receta")
        print("d) Ver la lista de recetas")
        print("e) buscar por ingredientes")
        print("f) Salir")

        choice = input("Introduzca una opcion: ").lower()

        if choice == 'a':
            nombre = input("Nombre de la receta: ")
            receta_id = añadir_receta(conn, nombre)
            print(f"Receta añadida con el id: {receta_id}")

        elif choice == 'b':
            receta_id = int(input("Ingrese el id de la receta: "))
            nombre = input("ingrese nombre actualizado: ")
            actualizar_receta(conn, receta_id, nombre)

        elif choice == 'c':
            receta_id = int(input("Introduce el id de la receta: "))
            borrar_receta(conn, receta_id)
            print("Receta borrada")

        elif choice == 'd':
            ver_receta(conn)

        elif choice == 'e':
            receta_id = int(input("Introduce el id de la receta: "))
            buscar_ingredientes(conn, receta_id)

        elif choice == 'f':
            break

        else:
            print("Opcion invalida, intente nuevamente")

if __name__ == "__main__":
    main()