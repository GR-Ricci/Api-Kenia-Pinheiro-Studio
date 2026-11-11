from team.staff import model


def listar_todos():
    return model.listar_staff()


def alterar_status(id_usuario, dados):
    usuario = model.obter_usuario(id_usuario)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    model.atualizar_ativo(id_usuario, dados.ativo)
    return {"ok": True}


def remover(id_usuario):
    usuario = model.obter_usuario(id_usuario)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    model.deletar_usuario_completo(id_usuario)
    return {"ok": True}