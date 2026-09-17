# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""


from database import conectar_banco

def listar_emails():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, email FROM usuario WHERE ativo = TRUE")
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados
