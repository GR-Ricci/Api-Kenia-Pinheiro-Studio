import shutil
from pathlib import Path

from catalog.package import model

PASTA_UPLOAD = Path(__file__).resolve().parents[3] / "upload"
PASTA_PREVIEW = PASTA_UPLOAD / "pacotepreview"
PASTA_PACOTE = PASTA_UPLOAD / "pacote"


def _validar_itens(id_profissional, itens):
    if not itens:
        raise ValueError("Pacote precisa ter ao menos um subserviço.")

    ids_vistos = set()
    for item in itens:
        if item.quantidade <= 0:
            raise ValueError("Quantidade de cada subserviço precisa ser maior que zero.")
        if item.id_subservico in ids_vistos:
            raise ValueError("Subserviço duplicado no pacote. Use a quantidade para repetir.")
        ids_vistos.add(item.id_subservico)

        if not model.subservico_existe(item.id_subservico):
            raise ValueError(f"Subserviço {item.id_subservico} não encontrado.")

        if not model.subservico_no_portfolio(id_profissional, item.id_subservico):
            model.inserir_vinculo_placeholder(id_profissional, item.id_subservico)


def _mover_imagem_preview(imagem_url):
    if not imagem_url:
        return
    origem = PASTA_PREVIEW / imagem_url
    if origem.is_file():
        PASTA_PACOTE.mkdir(parents=True, exist_ok=True)
        shutil.move(str(origem), str(PASTA_PACOTE / imagem_url))


def _obter_dono_pacote(id_pacote):
    itens = model.obter_itens_de_pacotes([id_pacote])
    lista = itens.get(id_pacote, [])
    return lista[0]["id_profissional"] if lista else None


def _pode_editar(usuario_logado, id_dono_pacote):
    if usuario_logado["tipo"] == "ADMIN":
        return True
    id_prof_logado = model.obter_id_profissional_por_usuario(usuario_logado["id"])
    return id_prof_logado is not None and id_prof_logado == id_dono_pacote


def _montar(pacote_dict, itens):
    primeiro = itens[0] if itens else None
    return {
        **pacote_dict,
        "id_profissional": primeiro["id_profissional"] if primeiro else None,
        "nome_profissional": primeiro["nome_profissional"] if primeiro else None,
        "imagem_profissional_url": primeiro["imagem_profissional_url"] if primeiro else None,
        "itens": [
            {
                "id": i["id"],
                "id_subservico": i["id_subservico"],
                "nome_subservico": i["nome_subservico"],
                "nome_servico": i["nome_servico"],
                "nome_categoria": i["nome_categoria"],
                "quantidade": i["quantidade"],
                "preco_unitario": i["preco_unitario"],
                "duracao_minutos": i["duracao_minutos"],
                "imagem_url": i["imagem_url"],
            }
            for i in itens
        ],
    }


def _obter_completo(id_pacote):
    pacote = model.obter_pacote(id_pacote)
    if not pacote:
        return None
    itens_por_pacote = model.obter_itens_de_pacotes([id_pacote])
    return _montar(pacote, itens_por_pacote.get(id_pacote, []))


def criar(usuario_logado, dados):
    id_prof = model.obter_id_profissional_por_usuario(usuario_logado["id"])
    if not id_prof:
        raise ValueError(
            "Usuário sem perfil profissional. Cadastre o perfil antes de criar pacotes."
        )

    if dados.id_categoria is not None:
        if not model.categoria_existe(dados.id_categoria):
            raise ValueError("Categoria inválida.")
        id_cat = dados.id_categoria
    else:
        id_cat = model.obter_ou_criar_categoria_pacotes()

    _validar_itens(id_prof, dados.itens)
    _mover_imagem_preview(dados.imagem_url)

    id_pacote = model.criar_pacote_completo(
        id_categoria=id_cat,
        nome=dados.nome,
        preco=dados.preco,
        imagem_url=dados.imagem_url,
        descricao=dados.descricao,
        ativo=dados.ativo,
        id_profissional=id_prof,
        itens=dados.itens,
    )
    return _obter_completo(id_pacote)


def listar_do_profissional(id_profissional):
    pacotes = model.listar_pacotes_por_profissional(id_profissional)
    if not pacotes:
        return []
    ids = [p["id"] for p in pacotes]
    itens_por_pacote = model.obter_itens_de_pacotes(ids)
    return [_montar(p, itens_por_pacote.get(p["id"], [])) for p in pacotes]


def listar_todos():
    pacotes = model.listar_todos_pacotes()
    if not pacotes:
        return []
    ids = [p["id"] for p in pacotes]
    itens_por_pacote = model.obter_itens_de_pacotes(ids)
    return [_montar(p, itens_por_pacote.get(p["id"], [])) for p in pacotes]


def obter(id_pacote, usuario_logado):
    completo = _obter_completo(id_pacote)
    if not completo:
        raise ValueError("Pacote não encontrado.")
    id_dono = completo["id_profissional"]
    if not _pode_editar(usuario_logado, id_dono):
        raise ValueError("Acesso negado a este pacote.")
    return completo


def atualizar(id_pacote, usuario_logado, dados):
    atual = model.obter_pacote(id_pacote)
    if not atual:
        raise ValueError("Pacote não encontrado.")

    id_dono = _obter_dono_pacote(id_pacote)
    if not _pode_editar(usuario_logado, id_dono):
        raise ValueError("Acesso negado a este pacote.")

    if dados.id_categoria is not None:
        if not model.categoria_existe(dados.id_categoria):
            raise ValueError("Categoria inválida.")
        id_cat = dados.id_categoria
    else:
        id_cat = atual["id_categoria"]

    _validar_itens(id_dono, dados.itens)

    _mover_imagem_preview(dados.imagem_url)

    model.atualizar_pacote_completo(
        id_pacote=id_pacote,
        id_categoria=id_cat,
        nome=dados.nome,
        preco=dados.preco,
        imagem_url=dados.imagem_url,
        descricao=dados.descricao,
        ativo=dados.ativo,
        id_profissional=id_dono,
        itens=dados.itens,
    )
    return _obter_completo(id_pacote)


def impacto_delete(id_pacote, usuario_logado):
    if not model.obter_pacote(id_pacote):
        raise ValueError("Pacote não encontrado.")
    id_dono = _obter_dono_pacote(id_pacote)
    if not _pode_editar(usuario_logado, id_dono):
        raise ValueError("Acesso negado a este pacote.")
    return model.contar_impacto_delete(id_pacote)


def remover(id_pacote, usuario_logado, force=False):
    if not model.obter_pacote(id_pacote):
        raise ValueError("Pacote não encontrado.")
    id_dono = _obter_dono_pacote(id_pacote)
    if not _pode_editar(usuario_logado, id_dono):
        raise ValueError("Acesso negado a este pacote.")

    impacto = model.contar_impacto_delete(id_pacote)
    if impacto["agendamentos"] > 0 and not force:
        raise ValueError(f"IMPACTO:{impacto['agendamentos']}")

    model.deletar_pacote(id_pacote)


def criar_subservico_rapido(id_profissional, nome):
    if not nome or not nome.strip():
        raise ValueError("Nome obrigatório.")
    nome = nome.strip()

    id_sub = model.criar_subservico_pacote(nome)
    model.inserir_vinculo_placeholder(id_profissional, id_sub)

    info = model.obter_info_subservico(id_sub)
    return {
        "id_subservico": id_sub,
        "nome_subservico": info[0],
        "nome_servico": info[1],
        "nome_categoria": info[2],
    }