# contém as regras e decisões da funcionalidade.

"""
Exemplo de uso:
criar_galeria(dados)
listar_galeria()
"""

from contact import model


def buscar_contato():
    contato = model.buscar_contato()
    if contato is None:
        raise ValueError("Contato não cadastrado")

    #desempacotamento
    telefone, whatsapp, email, rede_social, endereco = contato
    return {
        "telefone": telefone,
        "whatsapp": whatsapp,
        "email": email,
        "rede_social": rede_social,
        "endereco": endereco
    }
