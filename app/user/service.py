# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from user.model import listar_emails


def obter_emails():
    resultados = listar_emails()

    return [
        {
            "id": id_usuario,
            "email": email
        }
        for id_usuario, email in resultados
    ]
