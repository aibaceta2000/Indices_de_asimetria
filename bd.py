import pymongo
import streamlit as st
import bcrypt
from utilidades import add_sesion_state


def guardar(data_entrada):
    client = pymongo.MongoClient(
        "mongodb+srv://sebasheviarivas:izipass@cluster0.opihyei.mongodb.net/ChromIndex?retryWrites=true&w=majority"
    )
    db = client.Chromindex  # Reemplaza 'ChromIndex' con el nombre de tu base de datos
    collection = (
        db.tu_coleccion
    )  # Reemplaza 'tu_coleccion' con el nombre de tu colección

    # borrar todo lo de la bd
    collection.delete_many({})

    username = st.session_state["logeado"]
    for data in data_entrada:
        data["username"] = username
        inserted_data = collection.insert_one(data)

        if inserted_data.acknowledged:
            st.write(
                f"Datos insertados para {username} con el ID:",
                inserted_data.inserted_id,
            )
        else:
            st.write("Error al insertar datos.")

    # imprimir toda la data de la bd
    data_from_collection = list(collection.find({"username": username}))

    if data_from_collection:
        st.header("Data from MongoDB Collection")
        for data in data_from_collection:
            st.write(data)

    client.close()


# auth muy basico, busca si esta el user y password en la coleccion users
def auth(username, password):
    client = pymongo.MongoClient(
        "mongodb+srv://sebasheviarivas:izipass@cluster0.opihyei.mongodb.net/ChromIndex?retryWrites=true&w=majority"
    )
    db = client["Chromindex"]
    collection = db["users"]

    user_data = collection.find_one({"username": username})

    if user_data:
        hashed_password = user_data.get("password")
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return True
    else:
        return False


# login que utiliza el auth basico
def login():
    st.header("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if auth(username, password):
            st.success("Inicio de sesión exitoso")
            add_sesion_state("logeado", username)  # esto mantiene la sesion del usuario
        else:
            st.error("Credenciales incorrectas. Inténtalo de nuevo.")


# crear user basico, cifrar con bcrypt
def create_user():
    st.header("Create account")
    client = pymongo.MongoClient(
        "mongodb+srv://sebasheviarivas:izipass@cluster0.opihyei.mongodb.net/ChromIndex?retryWrites=true&w=majority"
    )
    db = client["Chromindex"]
    collection = db["users"]

    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña deseada", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")

    if st.button("Registrar"):
        if password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            st.success("Registro exitoso. Puedes iniciar sesión ahora.")
        else:
            st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
