
CREATE TABLE funcionamento (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dia INTEGER NOT NULL,
    abertura TIME,
    fechamento TIME,
    CONSTRAINT dia_valido CHECK (dia BETWEEN 0 AND 6)
);


CREATE TABLE contato (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    telefone VARCHAR(15) NOT NULL,
    whatsapp VARCHAR(15),
    email VARCHAR(80),
    rede_social VARCHAR(80),
    endereco VARCHAR(150)
);


CREATE TABLE tag (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE galeria (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    imagem_url VARCHAR(255) NOT NULL,
    ordem_exibicao INTEGER
);


CREATE TABLE galeria_tag (
    id_galeria INTEGER NOT NULL REFERENCES galeria(id) ON DELETE CASCADE,
    id_tag INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (id_galeria, id_tag)
);



CREATE TABLE usuario (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(80) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL
        CHECK (tipo IN ('ADMIN', 'PROFISSIONAL')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE profissional (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario INTEGER UNIQUE
        REFERENCES usuario(id) ON DELETE SET NULL,
    nome VARCHAR(100) NOT NULL,
    bio TEXT,
    imagem_url VARCHAR(255),
    ordem_exibicao INTEGER,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE jornada (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_profissional INTEGER NOT NULL
        REFERENCES profissional(id) ON DELETE RESTRICT,
    dia_semana INTEGER NOT NULL
        CHECK (dia_semana BETWEEN 0 AND 6),
    hora_inicio TIME,
    hora_fim TIME,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT horario_completo CHECK (
        (hora_inicio IS NULL AND hora_fim IS NULL)
        OR
        (
            hora_inicio IS NOT NULL
            AND hora_fim IS NOT NULL
            AND hora_inicio < hora_fim
        )
    )
);


CREATE TABLE excecao (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_profissional INTEGER NOT NULL
        REFERENCES profissional(id) ON DELETE RESTRICT,
    data_hora_inicio TIMESTAMPTZ NOT NULL,
    data_hora_fim TIMESTAMPTZ NOT NULL,
    tipo VARCHAR(20) NOT NULL
        CHECK (tipo IN ('FOLGA', 'FERIAS', 'HORA_EXTRA', 'BLOQUEIO')),
    descricao VARCHAR(255),

    CONSTRAINT horario_valido CHECK (
        data_hora_inicio < data_hora_fim
    )
);


CREATE TABLE categoria (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    ordem_exibicao INTEGER,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE carrossel (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_categoria INTEGER NOT NULL REFERENCES categoria(id) ON DELETE CASCADE,
	imagem_url VARCHAR(255) NOT NULL,
	ordem_exibicao INTEGER
);


CREATE TABLE servico (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_categoria INTEGER NOT NULL REFERENCES categoria(id) ON DELETE CASCADE,
	nome VARCHAR(100) NOT NULL,
	ordem_exibicao INTEGER,
	imagem_url VARCHAR(255),
	descricao VARCHAR(255),
	ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE subservico (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_servico INTEGER NOT NULL REFERENCES servico(id) ON DELETE CASCADE,
	nome VARCHAR(100) NOT NULL,
	ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE profissional_subservico (
	id_profissional INTEGER NOT NULL,
	id_subservico INTEGER NOT NULL,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	preco DECIMAL(10,2) NOT NULL,
	duracao_minutos INTEGER NOT NULL,
	descricao VARCHAR(255),
	imagem_url VARCHAR(255),
	ordem_exibicao INTEGER,
	PRIMARY KEY (id_profissional, id_subservico),
	FOREIGN KEY (id_profissional) REFERENCES profissional(id) ON DELETE RESTRICT,
	FOREIGN KEY (id_subservico) REFERENCES subservico(id) ON DELETE RESTRICT,
	CHECK (preco > 0),
	CHECK (duracao_minutos > 0)
);


CREATE TABLE pacote (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_categoria INTEGER NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
	nome VARCHAR(100) NOT NULL,
	preco DECIMAL(10,2) NOT NULL,
	ordem_exibicao INTEGER,
	imagem_url VARCHAR(255),
	descricao TEXT,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	CHECK (preco > 0)
);



CREATE TABLE pacote_item (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_pacote INTEGER NOT NULL REFERENCES pacote(id) ON DELETE RESTRICT,
	id_profissional INTEGER NOT NULL,
	id_subservico INTEGER NOT NULL,
	quantidade INTEGER NOT NULL,
	ordem_exibicao INTEGER,
	FOREIGN KEY (id_profissional, id_subservico)
	    REFERENCES profissional_subservico(id_profissional, id_subservico)
	    ON DELETE RESTRICT,
	UNIQUE (id_pacote, id_profissional, id_subservico),
	CHECK (quantidade > 0)
);


CREATE TABLE agendamento (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	id_profissional INTEGER NOT NULL,
	id_subservico INTEGER NOT NULL,
	id_pacote INTEGER
	    REFERENCES pacote(id) ON DELETE SET NULL,
	nome_cliente VARCHAR(100) NOT NULL,
	telefone_cliente VARCHAR(15) NOT NULL,
	data_hora_inicio TIMESTAMPTZ NOT NULL,
	data_hora_fim TIMESTAMPTZ NOT NULL,
	status VARCHAR(20) NOT NULL DEFAULT 'AGENDADO'
	    CHECK (status IN ('AGENDADO', 'CANCELADO', 'CONCLUIDO')),
	FOREIGN KEY (id_profissional, id_subservico)
	    REFERENCES profissional_subservico(
	        id_profissional,
	        id_subservico
	    ) ON DELETE RESTRICT,
	CHECK (data_hora_inicio < data_hora_fim)
);
