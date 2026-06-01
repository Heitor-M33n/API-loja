-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE IF NOT EXISTS public.clientes (
	id SERIAL PRIMARY KEY,
	nome varchar(100) NOT NULL,
	email varchar(100) NOT NULL,
	cpf varchar(11) NOT NULL
);

-- Drop table

-- DROP TABLE public.produtos;

CREATE TABLE IF NOT EXISTS public.produtos (
	id SERIAL PRIMARY KEY,
	produto varchar(100) NOT NULL,
	estoque INT NOT NULL,
	preco numeric(10, 2) NOT NULL,
);

-- Drop table

-- DROP TABLE public.pedidos;

CREATE TABLE IF NOT EXISTS public.pedidos (
	id SERIAL NOT NULL,
	id_cliente INT NOT NULL,
	id_produto INT NOT NULL,
	data_pedido date DEFAULT CURRENT_DATE NOT NULL,
	CONSTRAINT pedidos_pkey PRIMARY KEY (id),
	CONSTRAINT pedidos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente) ON DELETE CASCADE
);