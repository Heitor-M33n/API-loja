-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE IF NOT EXISTS public.clientes (
	id SERIAL PRIMARY KEY,
	nome varchar(100) NOT NULL,
	email varchar(100) NOT NULL UNIQUE,
	cpf varchar(11) NOT NULL UNIQUE
);

-- Drop table

-- DROP TABLE public.produtos;

CREATE TABLE IF NOT EXISTS public.produtos (
	id SERIAL PRIMARY KEY,
	produto varchar(100) NOT NULL,
	estoque INT NOT NULL,
	preco numeric(10, 2) NOT NULL
);

-- Drop table

-- DROP TABLE public.pedidos;

CREATE TABLE IF NOT EXISTS public.pedidos (
	id SERIAL PRIMARY KEY,
	id_cliente INT NOT NULL,
	id_produto INT NOT NULL,
	data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	
	CONSTRAINT fk_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES public.clientes(id),

    CONSTRAINT fk_produto
    FOREIGN KEY (id_produto)
    REFERENCES public.produtos(id)
);
