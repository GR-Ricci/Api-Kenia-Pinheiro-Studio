from database import conect_database


def inserir_carrossel(imagem_url, id_categoria, ordem_exibicao=None):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO carrossel (imagem_url, id_categoria, ordem_exibicao) VALUES (%s, %s, %s) RETURNING id",
        (imagem_url, id_categoria, ordem_exibicao),
    )
    id_carrossel = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_carrossel


def listar_carrosseis():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT c.id, c.imagem_url, c.id_categoria, cat.nome, c.ordem_exibicao
        FROM carrossel c
        JOIN categoria cat ON c.id_categoria = cat.id
        ORDER BY c.ordem_exibicao NULLS LAST, c.id
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {
            "id": r[0],
            "imagem_url": r[1],
            "id_categoria": r[2],
            "nome_categoria": r[3],
            "ordem_exibicao": r[4],
        }
        for r in resultados
    ]


def obter_carrossel(id_carrossel):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, imagem_url, id_categoria, ordem_exibicao FROM carrossel WHERE id = %s",
        (id_carrossel,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {
        "id": resultado[0],
        "imagem_url": resultado[1],
        "id_categoria": resultado[2],
        "ordem_exibicao": resultado[3],
    }


def atualizar_carrossel(id_carrossel, id_categoria, ordem_exibicao):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE carrossel SET id_categoria = %s, ordem_exibicao = %s WHERE id = %s",
        (id_categoria, ordem_exibicao, id_carrossel),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_carrossel(id_carrossel):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM carrossel WHERE id = %s", (id_carrossel,))
    conexao.commit()
    cursor.close()
    conexao.close()


def verificar_categoria_existe(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM categoria WHERE id = %s", (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def obter_nome_categoria(id_categoria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM categoria WHERE id = %s", (id_categoria,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None