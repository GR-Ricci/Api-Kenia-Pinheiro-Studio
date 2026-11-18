from database import conect_database


def dados_login(email):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, senha_hash, tipo, ativo, superadmin FROM usuario WHERE email = %s", (email,))
    dados_usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return dados_usuario

def buscar_ativo(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("SELECT ativo FROM usuario WHERE id = %s", (id_usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None  # usuário não existe
    return resultado[0]  # True ou False