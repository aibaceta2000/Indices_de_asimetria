import pymongo
import streamlit as st
import bcrypt
import pandas as pd
from utilidades import add_sesion_state
from dotenv import load_dotenv
import os

load_dotenv()


def conectar():
    client = pymongo.MongoClient(os.getenv("mongo_client"))
    db = client.Chromindex  # nombre de la bd
    return client, db


# guardar resultados de los indices
def guardar(data_entrada):
    idioma = st.session_state.idioma
    
    client, db = conectar()
    collection = db.indices

    username = st.session_state["logeado"]
    for data in data_entrada:
        data["username"] = username  # asociar con el user
        inserted_data = collection.insert_one(data)

        if inserted_data.acknowledged:
            if idioma == 0:
                st.success(f"Data saved for {username}")
            elif idioma == 1:
                st.success(f"Data del usuario {username} guardada")

        else:
            if idioma == 0:
                st.error("Error while saving the data.")
            elif idioma == 1:
                st.error("Ocurrió un error mientras se guardaba la data.")

    client.close()


# mostrar todos los datos de la bd
def ver():
    idioma = st.session_state.idioma
    text = {}
    text['header'] = ['Saved data from', 'Data del usuario']
    text['delete'] = ['Delete', 'Borrar']
    text['document'] = ['Document', 'Archivo']
    text['download'] = ['Download', 'Descargar']

    client, db = conectar()
    collection = db.indices

    username = st.session_state["logeado"]
    # buscar data de la bd con el username
    data_from_collection = list(collection.find({"username": username}))

    if data_from_collection:
        st.header(f"{text['header'][idioma]} {username}")

        # boton para borrar todos los datos
        if st.button(f"Delete all {username}'s data"):
            # buscar los datos asociados al user
            result = collection.delete_many({"username": username})
            if result.deleted_count > 0:
                st.success(f"All documents for {username} deleted.")

        for data in data_from_collection:

            if data != data_from_collection[0]:
                st.write('---')

            # Crear un DataFrame sin incluir el campo 'username' e 'id'
            df = pd.DataFrame([data])
            df.drop(columns=["username", "_id"], inplace=True)
            st.write(df)

            col1, col2 = st.columns(2)

            with col1:
                # Agregar un botón para eliminar el documento
                if st.button('❌ 'f"{text['delete'][idioma]} {data['File']}, id: {data['_id']}"):
                    collection.delete_one({"_id": data["_id"]})
                    if idioma == 0:
                        st.success(f"Document {data['File']} deleted.")
                    elif idioma == 1:
                        st.success(f"Archivo {data['File']} borrado.")

            with col2:
                # Descargar el DataFrame como un archivo CSV
                csv_data = df.to_csv(index=False, encoding="utf-8")
                st.download_button(
                    label='⬇️ ' f"{text['download'][idioma]} CSV {data['File']}, id: {data['_id']}",
                    data=csv_data,
                    file_name=f"{data['File']}.csv",
                    mime="text/csv",
                )

    client.close()


# auth, busca si esta el user y password (hash) en la coleccion users
def auth(username, password):
    client, db = conectar()
    collection = db.users

    user_data = collection.find_one({"username": username})

    if user_data:
        hashed_password = user_data.get("password")
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return True
    else:
        return False
    client.close()


# login que utiliza el auth
def login():
    idioma = st.session_state.idioma
    text= {}
    text['username'] = ['Username', 'Nombre de usuario']
    text['password'] = ['Password', 'Contraseña']
    text['log_in'] = ['Log in', 'Iniciar sesión']
    text['msg_001'] = ['Login successful', 'Autenticación existosa']
    text['view_my_data'] = ['View my data', 'Ver mi data']
    text['msg_002'] = ['Incorrect credentials. Please try again.', 
                       'Credenciales incorrectas. Por favor, intente de nuevo']

    st.header("Login")
    username = st.text_input(text['username'][idioma], key='login_username')
    password = st.text_input(text['password'][idioma], type="password", key='login_password')

    if st.button(text['log_in'][idioma]):
        if auth(username, password):
            st.success(text['msg_001'][idioma])
            add_sesion_state("logeado", username)  # esto mantiene la sesion del usuario
            st.button(text['view_my_data'][idioma])
        else:
            st.error(text['msg_002'][idioma])


# crear user, cifrar con bcrypt
def create_user():
    idioma = st.session_state.idioma
    text = {}
    text['header'] = ['Create account', 'Crear cuenta']
    text['username'] = ['Username', 'Nombre de usuario']
    text['desired_password'] = ['Desired password', 'Nueva contraseña']
    text['confirm_password'] = ['Confirm password', 'Confirmar contraseña']
    text['register'] = ['Register', 'Registrarse']
    text['msg_001'] = ['Username already taken. Please choose another.', 
                         'El nombre de usuario ya existe. Por favor, escoja otro']
    text['msg_002'] = ['Registration successful. You can now log in.', 
                       'Usuario creado correctamente. Ahora puede logearse']
    text['msg_003'] = ['Passwords do not match. Please try again.', 
                       'Contraseña o nombre de usuario incorrecto. Por favor, intente nuevamente']
    
    
    st.header(text["header"][idioma])
    client, db = conectar()
    collection = db.users

    # username = st.text_input("Username")
    username = st.text_input(text["username"][idioma])
    password = st.text_input(text["desired_password"][idioma], type="password")
    confirm_password = st.text_input(text["confirm_password"][idioma], type="password")

    if st.button(text["register"][idioma]):
        # Check if the username is already taken
        existing_user = collection.find_one({"username": username})

        if existing_user:
            st.error(text["msg_001"][idioma])
        elif password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            st.success(text["msg_002"][idioma])
        else:
            st.error(text["msg_003"][idioma])

    client.close()
