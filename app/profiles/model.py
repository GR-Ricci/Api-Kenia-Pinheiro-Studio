# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""
from database import conect_database

def get_usuario_logado(id_usuario_logado):

    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, bio,imagem_url from profissional WHERE id_usuario = %s", (id_usuario_logado,))
    dados_usuario = cursor.fetchone() #devolve a tupla completa do select

    cursor.close()
    conexao.close()
    return dados_usuario

def post_perfil(id_usuario_logado, dados):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO profissional (id_usuario, nome, bio, imagem_url) VALUES (%s, %s, %s, %s) RETURNING id", (id_usuario_logado, dados.nome, dados.bio, dados.imagem_url))

    id_profissional = cursor.fetchone()[0]  # Pega o ID novo que o banco gerou

    conexao.commit()
    cursor.close()
    conexao.close()

    return id_profissional

def update_perfil(id_usuario_logado, dados):
    conexao = conect_database()
    cursor = conexao.cursor()

    features = []
    values = []

    for k, v, in dados.items():
        features.append(f"{k} = %s")
        values.append(v)

    features_set = ", ".join(features)  # nome = %s, bio = %s

    values.append(id_usuario_logado)   # maria, cabelereira, 5

    sql = f"UPDATE profissional SET {features_set} WHERE id_usuario = %s;"


    cursor.execute(sql, tuple(values))

    # "UPDATE profissional SET nome = %s , bio = %s WHERE id_usuario_logado = %s;" , (maria, cabelereira, 5)

    conexao.commit()
    cursor.close()
    conexao.close()