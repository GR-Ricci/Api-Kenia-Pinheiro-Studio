from informative.hours import model


def obter():
    rows = model.listar_todos()
    por_dia = {i: [] for i in range(7)}
    for r in rows:
        por_dia[r["dia"]].append({"abertura": r["abertura"], "fechamento": r["fechamento"]})
    return [{"dia": d, "horarios": por_dia[d]} for d in range(7)]


def atualizar_dia(dia, dados):
    if dia < 0 or dia > 6:
        raise ValueError("Dia inválido (0-6).")
    for slot in dados.horarios:
        if slot.abertura >= slot.fechamento:
            raise ValueError("Abertura deve ser menor que fechamento.")
    model.substituir_dia(dia, [h.model_dump() for h in dados.horarios])
    return {"dia": dia, "horarios": [h.model_dump() for h in dados.horarios]}