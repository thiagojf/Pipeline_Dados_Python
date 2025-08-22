CREATE TABLE IF NOT exists public.cotacoes (
  id BIGSERIAL primary key,
  preco NUMERIC(18,6) not null,
  ativo TEXT not null,
  moeda CHAR(3) not null default 'USD',
  hora_request TIMESTAMPTZ not null,
  inserido_em  TIMESTAMPTZ not null default now()

);