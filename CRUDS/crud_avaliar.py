import psycopg2
from flask import Flask, request, jsonify

# Configuração do banco de dados
conf = psycopg2.connect(
    host="localhost",
    dbname="steam2",
    user="manager",
    password="123"
)

app = Flask(_name_)


@app.route('/avaliacoes', methods=['GET'])
def get_avaliacoes():
    cursor = conf.cursor()
    cursor.execute("SELECT * FROM jogos.avaliacao;")
    avaliacoes = cursor.fetchall()
    cursor.close()

    return jsonify(avaliacoes)


@app.route(f'/avaliacoes/<int:id_jogador>', methods=['GET'])
def get_avaliacao(id_jogador):
    cursor = conf.cursor()
    cursor.execute(f"SELECT * FROM jogos.avaliacao WHERE id_jogador = {id_jogador};")
    avaliacao = cursor.fetchall()
    cursor.close()

    if not avaliacao:
        return jsonify({'erro': 'avaliacao nao encontrada'})

    return jsonify(avaliacao)


@app.route(f'/avaliacoes/add', methods=['POST'])
def add_avaliacao():

    avaliacao = request.get_json()

    if avaliacao.get('idJogo') is None or avaliacao.get('idJogador') is None or avaliacao.get('avaliacao') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    cur = conf.cursor()

    sql = f"INSERT INTO jogos.avaliacao VALUES ({avaliacao['idJogo']},{avaliacao['idJogador']},{avaliacao['avaliacao']});"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao adicionada com sucesso'})


@app.route('/avaliacoes/<int:id_jogador>', methods=['PUT'])
def update_avaliacao(id_jogador):
    avaliacao = request.get_json()

    if avaliacao.get('idJogo') is None or avaliacao.get('avaliacao') is None:
        return jsonify({'erro': 'faltam campos obrigatorios'})

    cur = conf.cursor()

    sql = f"UPDATE jogos.avaliacao SET id_jogo = {avaliacao['idJogo']}, avaliacao = {avaliacao['avaliacao']}" \
          f" WHERE id_jogador = {id_jogador} ;"
    print(sql)
    cur.execute(sql)
    conf.commit()
    cur.close()

    return jsonify({'sucesso': 'avaliacao editada com sucesso'})


@app.route('/avaliacoes/<int:id_jogador>', methods=['DELETE'])
def delete_avaliacao(id_jogador):

    if not get_avaliacao(id_jogador):
        return jsonify({'erro': 'avaliacao nao encontrada'})

    cursor = conf.cursor()
    cursor.execute(f"DELETE FROM jogos.avaliacao WHERE id_jogador = {id_jogador};")
    cursor.close()

    return jsonify({'sucesso': 'avaliacao excluida com sucesso'})


app.run(host='0.0.0.0', port=5000, debug=True)
