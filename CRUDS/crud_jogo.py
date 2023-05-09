import psycopg2
from psycopg2 import Error
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="localhost",
    database="sistema_steam",
    user="manager",
    password="123"
)