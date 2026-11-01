# representa as tabelas e os dados usados no banco.


"""
Exemplo de uso:
Galeria(id=1, imagem_url="imagem.jpg")
"""

# fala com o banco: lê o contato do estúdio (telefone, WhatsApp, e-mail, rede social e endereço).

from database import conect_database


def buscar_contato():
    # o estúdio tem um contato só: se houver mais de uma linha, vale a primeira
    conexao = conect_database()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT telefone, whatsapp, email, rede_social, endereco
        FROM contato
        ORDER BY id
        LIMIT 1
    """)
    contato = cursor.fetchone()

    cursor.close()
    conexao.close()
    return contato
