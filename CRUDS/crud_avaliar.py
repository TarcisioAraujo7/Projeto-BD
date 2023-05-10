import psycopg2
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="localhost",
    dbname="steam2",
    user="manager",
    password="123"
)

app = Flask(__name__)


@app.route('/avaliacoes', methods=['GET'])
def get_avaliacoes():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM jogos.avalia;")
    avaliacoes = cursor.fetchall()
    cursor.close()

    return jsonify(avaliacoes)


@app.route(f'/avaliacoes/<int:id_jogador>/<int:id_jogo>', methods=['GET'])
def get_avaliacao(id_jogador, id_jogo):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.avalia WHERE id_jogador = {id_jogador} AND id_jogo = {id_jogo};")
    avaliacao = cursor.fetchall()
    cursor.close()

    if not avaliacao:
        return jsonify({'erro': 'avaliacao nao encontrada'})

    return jsonify(avaliacao)


@app.route(f'/avaliacoes/add', methods=['POST'])
def add_avaliacao():

    avaliacao = request.get_json()

    if avaliacao.get('id_jogo') is None or avaliacao.get('id_jogador') is None or avaliacao.get('avaliacao') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_jogo(avaliacao.get('id_jogo')) or confere_jogador(avaliacao.get('id_jogador')):
        return jsonify({'erro': 'id de jogador ou de jogo não cadastrado'})

    cur = conf.cursor()

    sql = f"INSERT INTO jogos.avalia VALUES ({avaliacao['id_jogador']},{avaliacao['id_jogo']},{avaliacao['avaliacao']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao adicionada com sucesso'})


def confere_jogo(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogo WHERE id_jogo = {pk};")
    jogo = cursor.fetchall()
    cursor.close()
    return not jogo


def confere_jogador(pk):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.jogador WHERE id_jogador = {pk};")
    album = cursor.fetchall()
    cursor.close()
    return not album


def confere_avalia(pk1, pk2):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.avalia WHERE id_jogador = {pk1} AND id_jogo = {pk2};")
    album = cursor.fetchall()
    cursor.close()
    return not album


@app.route('/avaliacoes/<int:id_jogador>/<int:id_jogo>', methods=['PUT'])
def update_avaliacao(id_jogador,id_jogo):
    avaliacao = request.get_json()

    if avaliacao.get('avaliacao') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    if confere_avalia(id_jogador, id_jogo):
        return jsonify({'erro': 'avaliação não encontrada'})

    cur = conf.cursor()

    sql = f"UPDATE jogos.avalia SET nota = {avaliacao['avaliacao']}" \
          f" WHERE id_jogador = {id_jogador} AND id_jogo = {id_jogo} ;"

    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao editada com sucesso'})


@app.route('/avaliacoes/<int:id_jogador>/<int:id_jogo>', methods=['DELETE'])
def delete_avaliacao(id_jogador, id_jogo):

    if confere_avalia(id_jogador, id_jogo):
        return jsonify({'erro': 'avaliacao nao encontrada'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM jogos.avalia WHERE id_jogador = {id_jogador} AND id_jogo = {id_jogo};")
    cursor.close()

    return jsonify({'sucesso': 'avaliacao excluida com sucesso'})


app.run(host='0.0.0.0', port=5000, debug=True)
