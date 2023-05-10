import psycopg2
from psycopg2 import Error
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="localhost",
    dbname="steam2",
    user="manager",
    password="123"
)

app = Flask(__name__)


@app.route('/jogos', methods=['GET'])
def get_jogos():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM jogos.jogo;")
    jogos = cursor.fetchall()
    cursor.close()

    return jsonify(jogos)


@app.route(f'/jogos/<int:jogo_id>', methods=['GET'])
def get_jogoid(jogo_id):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogo WHERE id_jogo = {jogo_id};")
    jogo = cursor.fetchall()
    cursor.close()

    if not jogo:
        return jsonify({'erro': 'jogo nao encontrado'})

    return jsonify(jogo)


@app.route(f'/jogos/add', methods=['POST'])
def post_jogo():

    jogo = request.get_json()
    id_jogo = jogo['id_jogo']

    if jogo.get('nome_jogo') is None or jogo.get('id_categoria') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if not confere_jogo(id_jogo):
        return jsonify({'erro': 'ja existe jogo com esse id'})

    if jogo.get('id_album') is None or confere_album(jogo['id_album']):
        return jsonify({'erro': 'nao foi informado album ou foi informado um id de album invalido'})

    if confere_cat(jogo['id_categoria']):
        return jsonify({'erro': 'nao existe categoria com esse id'})

    cur = conf.cursor()
    if jogo.get('sequencia') is None:
        jogo['sequencia'] = 'NULL'

    sql = f"INSERT INTO jogos.jogo VALUES ({jogo['id_jogo']},'{jogo['nome_jogo']}',{jogo['preco']},{jogo['id_album']},{jogo['sequencia']}, {jogo['id_categoria']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'jogo adicionado com exito'})


def confere_jogo(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogo WHERE id_jogo = {pk};")
    jogo = cursor.fetchall()
    cursor.close()
    return not jogo


def confere_album(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.album WHERE id_album = {pk};")
    album = cursor.fetchall()
    cursor.close()
    return not album


def confere_cat(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.categoria WHERE id_categoria = {pk};")
    categoria = cursor.fetchall()
    cursor.close()
    return not categoria


@app.route('/jogos/<int:id_jogo>', methods=['PUT'])
def update_jogo(id_jogo):
    jogo = request.get_json()

    if jogo.get('nome_jogo') is None or jogo.get('id_categoria') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_jogo(id_jogo):
        return jsonify({'erro': 'nao existe jogo com esse id'})

    if jogo.get('id_album') is None or confere_album(jogo['id_album']):
        return jsonify({'erro': 'nao foi informado album ou foi informado um id de album invalido'})

    if confere_cat(jogo['id_categoria']):
        return jsonify({'erro': 'nao existe categoria com esse id'})

    cur = conf.cursor()
    if jogo.get('sequencia') is None:
        jogo['sequencia'] = 'NULL'

    sql = f"UPDATE jogos.jogo SET nome_jogo = '{jogo['nome_jogo']}', preco_jogo = {jogo['preco']}," \
          f"id_album = {jogo['id_album']}, sequencia = {jogo['sequencia']}, id_categoria = {jogo['id_categoria']} WHERE id_jogo = {id_jogo} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'jogo editado com exito'})


@app.route('/jogos/<int:id_jogo>', methods=['DELETE'])
def delete_jogo(id_jogo):

    if confere_jogo(id_jogo):
        return jsonify({'erro': 'nao existe jogo com esse id'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM jogos.jogo WHERE id_jogo = {id_jogo};")
    cursor.close()

    return jsonify({'sucesso': 'jogo excluido com exito'})


app.run(host='0.0.0.0', port=5000, debug=True)
