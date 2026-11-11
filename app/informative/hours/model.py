from database import conect_database


def listar_todos():
    conexao = conect_database()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT dia, abertura, fechamento
        FROM funcionamento
        WHERE abertura IS NOT NULL AND fechamento IS NOT NULL
        ORDER BY dia, abertura
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [
        {"dia": r[0], "abertura": str(r[1])[:5], "fechamento": str(r[2])[:5]}
        for r in resultados
    ]


def substituir_dia(dia, horarios):
    conexao = conect_database()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM funcionamento WHERE dia = %s", (dia,))
        for h in horarios:
            cursor.execute(
                "INSERT INTO funcionamento (dia, abertura, fechamento) VALUES (%s, %s, %s)",
                (dia, h["abertura"], h["fechamento"]),
            )
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()