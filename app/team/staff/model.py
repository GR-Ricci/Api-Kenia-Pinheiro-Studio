from database import conect_database


def listar_staff():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            usuario.id,
            profissional.id,
            COALESCE(profissional.nome, usuario.email),
            usuario.email,
            usuario.tipo,
            usuario.ativo,
            profissional.imagem_url
        FROM usuario
        LEFT JOIN profissional ON profissional.id_usuario = usuario.id
        ORDER BY
            CASE usuario.tipo
                WHEN 'ADMIN' THEN 1
                ELSE 2
            END,
            usuario.ativo DESC,
            COALESCE(profissional.nome, usuario.email)
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {
            "id": r[0],
            "id_profissional": r[1],
            "nome": r[2],
            "email": r[3],
            "tipo": r[4],
            "ativo": r[5],
            "imagem_url": r[6],
        }
        for r in resultados
    ]


def obter_staff_completo(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            usuario.id,
            profissional.id,
            COALESCE(profissional.nome, usuario.email),
            usuario.email,
            usuario.tipo,
            usuario.ativo,
            profissional.imagem_url
        FROM usuario
        LEFT JOIN profissional ON profissional.id_usuario = usuario.id
        WHERE usuario.id = %s
    """, (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {
        "id": resultado[0],
        "id_profissional": resultado[1],
        "nome": resultado[2],
        "email": resultado[3],
        "tipo": resultado[4],
        "ativo": resultado[5],
        "imagem_url": resultado[6],
    }


def obter_usuario(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, tipo, ativo FROM usuario WHERE id = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not resultado:
        return None
    return {"id": resultado[0], "tipo": resultado[1], "ativo": resultado[2]}


def atualizar_ativo(id_usuario, ativo):
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuario SET ativo = %s WHERE id = %s", (ativo, id_usuario))
    conexao.commit()
    cursor.close()
    conexao.close()


def deletar_usuario_completo(id_usuario):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        # 1. Busca profissional (se existir)
        cursor.execute(
            "SELECT id FROM profissional WHERE id_usuario = %s", (id_usuario,)
        )
        row = cursor.fetchone()
        id_prof = row[0] if row else None

        # 2. Deleta dependências do profissional
        if id_prof:
            cursor.execute("DELETE FROM agendamento WHERE id_profissional = %s", (id_prof,))
            cursor.execute("DELETE FROM pacote_item WHERE id_profissional = %s", (id_prof,))
            cursor.execute("DELETE FROM jornada WHERE id_profissional = %s", (id_prof,))
            cursor.execute("DELETE FROM excecao WHERE id_profissional = %s", (id_prof,))
            cursor.execute(
                "DELETE FROM profissional_subservico WHERE id_profissional = %s",
                (id_prof,),
            )
            cursor.execute("DELETE FROM profissional WHERE id = %s", (id_prof,))

        # 3. Deleta o usuário (email some do banco)
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))

        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()