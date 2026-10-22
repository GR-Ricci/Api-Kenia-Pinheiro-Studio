# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""
from database import conect_database


def dados_login(email):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, senha_hash, tipo, ativo FROM usuario WHERE email = %s", (email,))
    dados_usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return dados_usuario