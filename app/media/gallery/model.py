from database import conect_database


def inserir_galeria(imagem_url):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO galeria (imagem_url) VALUES (%s) RETURNING id",
        (imagem_url,),
    )
    id_galeria = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_galeria


def inserir_galeria_tag(id_galeria, id_tag):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO galeria_tag (id_galeria, id_tag) VALUES (%s, %s)",
        (id_galeria, id_tag),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_galeria_tags(id_galeria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM galeria_tag WHERE id_galeria = %s", (id_galeria,))
    conexao.commit()
    cursor.close()
    conexao.close()


def atualizar_imagem(id_galeria, imagem_url):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE galeria SET imagem_url = %s WHERE id = %s",
        (imagem_url, id_galeria),
    )
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_galeria(id_galeria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM galeria WHERE id = %s", (id_galeria,))
    conexao.commit()
    cursor.close()
    conexao.close()


def obter_galeria(id_galeria):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, imagem_url, ordem_exibicao FROM galeria WHERE id = %s",
        (id_galeria,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {
        "id": resultado[0],
        "imagem_url": resultado[1],
        "ordem_exibicao": resultado[2],
    }


def listar_galerias():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT g.id, g.imagem_url, g.ordem_exibicao, t.id, t.nome
        FROM galeria g
        LEFT JOIN galeria_tag gt ON g.id = gt.id_galeria
        LEFT JOIN tag t ON gt.id_tag = t.id
        ORDER BY g.ordem_exibicao NULLS LAST, g.id
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    fotos = {}
    for r in resultados:
        id_g, img, ordem, id_tag, nome_tag = r
        if id_g not in fotos:
            fotos[id_g] = {
                "id": id_g,
                "imagem_url": img,
                "ordem_exibicao": ordem,
                "tags": [],
            }
        if id_tag is not None:
            fotos[id_g]["tags"].append({"id": id_tag, "nome": nome_tag})

    return list(fotos.values())