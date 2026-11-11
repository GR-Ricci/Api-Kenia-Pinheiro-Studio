from database import conect_database


def inserir_tag(nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO tag (nome) VALUES (%s) RETURNING id",
        (nome,),
    )
    id_tag = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    return id_tag


def verificar_tag_existente(nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM tag WHERE LOWER(nome) = LOWER(%s)", (nome,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def listar_tags():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM tag ORDER BY nome")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [{"id": r[0], "nome": r[1]} for r in resultados]


def atualizar_tag(id_tag, nome):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("UPDATE tag SET nome = %s WHERE id = %s", (nome, id_tag))
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_tag(id_tag):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tag WHERE id = %s", (id_tag,))
    conexao.commit()
    cursor.close()
    conexao.close()


def obter_tag(id_tag):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM tag WHERE id = %s", (id_tag,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return {"id": resultado[0], "nome": resultado[1]} if resultado else None