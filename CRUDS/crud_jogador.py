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


@app.route('/jogadores', methods=['GET'])
def get_jogadores():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM jogos.jogador;")
    jogos = cursor.fetchall()
    cursor.close()

    return jsonify(jogadores)


@app.route(f'/jogador/<int:id_jogador>', methods=['GET'])
def get_jogadorid(jogador_id):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogador WHERE id_jogador = {jogador_id};")
    jogador = cursor.fetchall()
    cursor.close()

    if not jogador:
        return jsonify({'erro': 'jogador nao encontrado'})

    return jsonify(jogador)


@app.route(f'/jogadores/add', methods=['POST'])
def post_jogador():

    jogador = request.get_json()
    id_jogador = jogador['id_jogador']

    if jogador.get('nickname') is None or jogador.get('usuario_email') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if not confere_jogador(id_jogador):
        return jsonify({'erro': 'ja existe jogador com esse id'})
    
    cur = conf.cursor()

    sql = f"INSERT INTO jogos.jogador VALUES ({jogador['id_jogador']},'{jogador['usuario_email']}',{jogador['nickname']},{jogador['nivel']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'jogador adicionado com exito'})


def confere_jogador(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogador WHERE id_jogador = {pk};")
    jogador = cursor.fetchall()
    cursor.close()
    return not jogador


def confere_email(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.usuario WHERE email_usuario = {pk};")
    album = cursor.fetchall()
    cursor.close()
    return not email




@app.route('/jogadores/<int:id_jogador>', methods=['PUT'])
def update_jogador(id_jogador):
    jogador = request.get_json()

    if jogador.get('usuario_email') is None or jogador.get('nickname') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_jogador(id_jogador):
        return jsonify({'erro': 'nao existe jogador com esse id'})

    if confere_email(jogador['usuario_email']):
        return jsonify({'erro': 'nao existe email com esse id'}) #essa parte ta confusa

    cur = conf.cursor()

    sql = f"UPDATE jogos.jogador SET nome_jogo = '{jogo['nome_jogo']}', preco_jogo = {jogo['preco']}," \
          f"id_album = {jogo['id_album']}, sequencia = {jogo['sequencia']}, id_categoria = {jogo['id_categoria']} WHERE id_jogo = {id_jogo} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'jogador editado com exito'})


@app.route('/jogadores/<int:id_jogador>', methods=['DELETE'])
def delete_jogador(id_jogador):

    if confere_jogador(id_jogador):
        return jsonify({'erro': 'nao existe jogador com esse id'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM jogos.jogador WHERE id_jogador = {id_jogador};")
    cursor.close()

    return jsonify({'sucesso': 'jogador excluido com exito'})


app.run(host='0.0.0.0', port=5000, debug=True)