import psycopg2
from psycopg2 import Error
from flask import Flask, request, jsonify

# Configuração do banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="seu_banco_de_dados",
    user="seu_usuario",
    password="sua_senha"
)