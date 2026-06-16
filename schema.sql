CREATE TABLE IF NOT EXISTS clientes (
	id SERIAL PRIMARY KEY,
	nome varchar(100) NOT NULL,
	email varchar(100) NOT NULL UNIQUE,
	cpf varchar(11) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS produtos (
	id SERIAL PRIMARY KEY,
	produto varchar(100) NOT NULL,
	estoque INT NOT NULL,
	preco numeric(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
	id SERIAL PRIMARY KEY,
	id_cliente INT NOT NULL,
	id_produto INT NOT NULL,
	data TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	
	CONSTRAINT fk_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id)
	ON DELETE CASCADE,

    CONSTRAINT fk_produto
    FOREIGN KEY (id_produto)
    REFERENCES produtos(id)
	ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);