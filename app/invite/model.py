# representa as tabelas e os dados usados no banco.

"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""

# fala com o banco: lê e grava dados do convite e do usuário.

from database import conect_database

def criar_convite(token,tipo,expira_em):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO convite (token, tipo, expira_em ) VALUES(%s, %s, %s)",
                   (token,tipo,expira_em))


    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_convite(token):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, tipo, expira_em, usado FROM convite WHERE token = %s",(token,))

    convite = cursor.fetchone()

    cursor.close()
    conexao.close()
    return convite

def usar_convite(id_convite):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("UPDATE convite SET usado = TRUE WHERE id = %s", (id_convite,))

    conexao.commit()
    cursor.close()
    conexao.close()


def criar_usuario(email, senha_hash, tipo):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO usuario (email, senha_hash, tipo) VALUES(%s, %s, %s)",(email, senha_hash, tipo))

    conexao.commit()
    cursor.close()
    conexao.close()