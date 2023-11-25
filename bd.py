import pymongo
import streamlit as st
import bcrypt
import pandas as pd
from utilidades import add_sesion_state
from dotenv import load_dotenv
import os

load_dotenv()


def conectar():
    client = pymongo.MongoClient(
        os.getenv('mongo_client')
    )
    db = client.Chromindex  # nombre de la bd
    return client, db


def guardar(data_entrada):
    client, db = conectar()
    collection = db.indices

    username = st.session_state["logeado"]
    for data in data_entrada:
        data["username"] = username
        inserted_data = collection.insert_one(data)

        if inserted_data.acknowledged:
            st.success(f"Data saved for {username}")
        else:
            st.error("Error while saving the data.")
    client.close()


def ver():
    client, db = conectar()
    collection = db.indices

    username = st.session_state["logeado"]
    # buscar data de la bd con el username
    data_from_collection = list(collection.find({"username": username}))

    if data_from_collection:
        st.header(f"Saved data from {username}")
        for data in data_from_collection:
            # Crear un DataFrame sin incluir el campo 'username' e 'id'
            df = pd.DataFrame([data])
            df.drop(columns=["username", "_id"], inplace=True)
            st.write(df)

            # Agregar un botón para eliminar el documento
            if st.button(f"Delete {data['File']}, id: {data['_id']}"):
                collection.delete_one({"_id": data["_id"]})
                st.success(f"Document {data['File']} deleted.")

            # Descargar el DataFrame como un archivo CSV
            csv_data = df.to_csv(index=False, encoding="utf-8")
            st.download_button(
                label=f"Download CSV {data['File']}, id: {data['_id']}",
                data=csv_data,
                file_name=f"{data['File']}.csv",
                mime="text/csv",
            )

    client.close()


# auth, busca si esta el user y password en la coleccion users
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
    st.header("Login")
    username = st.text_input("Username ")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if auth(username, password):
            st.success("Login successful")
            add_sesion_state("logeado", username)  # esto mantiene la sesion del usuario
            st.button("View my data")
        else:
            st.error("Incorrect credentials. Please try again.")


# crear user, cifrar con bcrypt
def create_user():
    st.header("Create account")
    client, db = conectar()
    collection = db.users

    username = st.text_input("Username")
    password = st.text_input("Desired Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        # Check if the username is already taken
        existing_user = collection.find_one({"username": username})

        if existing_user:
            st.error("Username already taken. Please choose another.")
        elif password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            collection.insert_one({"username": username, "password": hashed_password})
            st.success("Registration successful. You can now log in.")
        else:
            st.error("Passwords do not match. Please try again.")

    client.close()
