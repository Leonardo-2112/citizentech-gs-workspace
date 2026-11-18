# 4 · Domain Driven Design Using Java — API ZelaBairro

Depende do **Banco** pronto no Oracle. Base: Documento Base v1.5, seção 8 (pacotes, endpoints, JSON, login 8.5, fotos); padrão do projeto anterior em [`docs/referencias/02-EcoScoreEngine-API.md`](../../docs/referencias/02-EcoScoreEngine-API.md); plano seção 3.

> **Repositório próprio:** o deploy no Render (obrigatório) é feito a partir de um repositório GitHub, então a versão final da API vai para um repositório separado (ex.: `zelabairro-api`, pode ser privado; o Render conecta com repositório privado). Esta pasta serve para desenvolver e guardar a cópia de trabalho e os links.

## O que tem nesta pasta
| Arquivo | Conteúdo |
|---|---|
| `zelabairro-api/` | Projeto Spring Boot (pacotes `model`, `dao`, `dto`, `controller`, `exception`, `handler`, `config` + `bo`) com `Dockerfile` multi-stage e `README.md` (integrantes, como rodar, Render) |
| `zelabairro.sql` | Cópia **idêntica** do script da pasta `2-banco-de-dados` |
| `documentacao.pdf` | Os 8 itens do PDF da disciplina. Gerado por `gerar_documentacao.py` (`uv run --with reportlab python gerar_documentacao.py`) |
| `ZelaBairro.postman_collection.json` | Coleção Postman/Insomnia com todos os endpoints; pasta **99 - Erros para a demo** (400, 401, 403, 404, 405, 409) |
| `testes/testar_endpoints.sh` | 117 verificações com curl (`./testar_endpoints.sh URL_BASE`); evidências em `testes/evidencia_*.txt` |
| `identificacao.txt` | RM, nome e turma |
| `montar_zip.py` | Monta `ZelaBairro_Java_1TDSPV.zip` **sem `target/` e sem `.env`** (`python montar_zip.py`) |
| `imagens/der.png` | Modelo relacional do Data Modeler (usado no PDF) |

## Checklist
- [x] JDBC puro com `DataSource` no construtor, `PreparedStatement`, try-with-resources e `sq_tb_*.NEXTVAL` (sem JPA/Hibernate/Spring Data)
- [x] DTOs de entrada e saída + ModelMapper + Bean Validation com `@Valid`; handler com o JSON de erro da seção 8.3 (sem stack trace nem SQL)
- [x] CRUD de Cidadao, Gestor, Bairro, Categoria e Ocorrencia + rotas aninhadas (atualizações, apoios, fotos, `/bairros/{id}/ocorrencias`, `/categorias/{id}/ocorrencias`)
- [x] Status 201 + Location, 200, 204, 400 (com `campos`), 401, 403, 404, 405, 409 e 500 genérico — testados com curl
- [x] Regras com exceção própria: RN01, RN02, RN05, RN06, RN08, RN09, RN10, RN11, RN13, RN14, RN15, RN16, RN17, RN18
- [x] Login BCrypt (`POST /auth/login` → `{id, nome, perfil}`), rotas de gestor com `X-Gestor-Id`, senha nunca devolvida
- [x] Fotos em BLOB (RN18) com `X-Cidadao-Id`
- [x] CORS lendo `CORS_ORIGINS`, liberando `X-Gestor-Id` e `X-Cidadao-Id`
- [x] Credenciais só em variáveis de ambiente (`DB_URL`, `DB_USER`, `DB_PASSWORD`, `IA_API_URL`, `CORS_ORIGINS`)
- [x] Integração com a IA (desejável): previsão gravada; RN12 (IA fora do ar) e D3 (Iluminação) testadas
- [x] Dockerfile multi-stage testado localmente (build + container respondendo)
- [x] `documentacao.pdf`, coleção, README, `.zip` sem `target/`
- [x] Repositório https://github.com/Leonardo-2112/zelabairro-api e serviço no Render https://zelabairro-api-08ut.onrender.com (testado em 18/11: 117/117 com curl em `testes/evidencia_render.txt` e 57/57 da coleção em `testes/evidencia_postman_render.txt`)
- [ ] **Grupo:** preencher o link do vídeo em `gerar_documentacao.py` e `zelabairro-api/README.md`, gerar o PDF de novo e rodar `montar_zip.py`
- [ ] **Grupo:** gravar o vídeo (até 5 min, front integrado)
- [ ] **Grupo:** front consumindo a API (requisito 12) e `CORS_ORIGINS` com a URL da Vercel
- [x] API Flask de IA publicada em https://zelabairro-ia.onrender.com e `IA_API_URL` preenchida no serviço da API Java (18/11). O `testes/testar_endpoints.sh` aceita os dois casos (com previsão, ou nula pela RN12); rodado de novo no Render em 18/11 com a IA ligada: 117/117 e 57/57 da coleção, ocorrência criada com previsão. Antes da demo, abrir `https://zelabairro-ia.onrender.com/health` uns 2 minutos antes (cold start de 15 a 50 s; com timeout de 4 s, a 1ª ocorrência cairia na RN12)

## Decisões registradas (Documento Base ambíguo ou divergente)
| # | Decisão | Motivo |
|---|---|---|
| J1 | `riscoAtraso` sai como **"ALTO"/"BAIXO"** (ou `null`), não "S"/"N" como no exemplo da seção 8.3 | D4: sem porcentagem e em linguagem do cidadão. **O Documento Base 8.3 precisa ser atualizado** (o front deve ler ALTO/BAIXO) |
| J2 | A saída da ocorrência ganhou `idAutor`, e a categoria aninhada traz também `descricao` e `idOrgao` | O front precisa saber se o usuário logado é o autor (fotos, RN18); RN13 continua: nada de e-mail/telefone |
| J3 | `GET /cidadaos` (lista pública) devolve só `{id, nome}` com o primeiro nome; `GET /cidadaos/{id}` devolve o perfil completo (sem senha) | RN13 vale para listagens; o perfil é usado pelo próprio cidadão. Sem token, o id é público (mesma limitação da seção 8.5) |
| J4 | `PUT /cidadaos/{id}` e `PUT /gestores/{id}` recebem o mesmo DTO do cadastro, com senha obrigatória (regrava o hash) | Mais simples; a seção 8.2 não define um DTO de edição |
| J5 | `PUT /ocorrencias/{id}` usa `OcorrenciaEdicaoRequestDto` (sem `idCidadao`): o autor não muda. A previsão da IA **não** é recalculada | Seção 7.4: a IA é chamada uma vez, na criação |
| J6 | Atualizações não têm DELETE; o `PUT` só corrige o comentário | O histórico de status é auditoria (RN06); apagar quebraria o status atual |
| J7 | `DELETE /ocorrencias/{id}` sem apoios e sem atualizações remove as fotos junto (mesma transação) | RN09 só barra apoios/atualizações; as fotos são do próprio autor |
| J8 | Rotas extras: `GET /orgaos` (só leitura), `GET .../atualizacoes/{id}`, `GET .../apoios/{idCidadao}`, `GET /health` | O front precisa listar órgãos nos formulários; o `Location` do 201 aponta para uma rota que existe |
| J9 | Falta de `X-Gestor-Id` / `X-Cidadao-Id` → **403** (não 400) | RN16/RN18: quem não se identifica não tem permissão |
| J10 | Remover cidadão com ocorrências/apoios e gestor com atualizações/gestores cadastrados → 409 | "Remoção de registro com filhos" do PDF |
| J11 | Atrasada (RN11) é sempre `false` para CANCELADA; dias em aberto vão até a data de resolução quando RESOLVIDA | Cancelada não está "atrasada"; RESOLVIDA usa a data real |
| J12 | Timeout da IA: 4 s (variável `IA_TIMEOUT_MS`); se a 1ª chamada falhar, a 2ª não é feita | "Timeout curto" do pedido; com a Flask dormindo no Render, a ocorrência cai na RN12 |

Nenhuma divergência com o PDF dos professores: as rotas seguem a seção 8.2 do Documento Base (o PDF dá só exemplos), e regra violada / remoção com filhos usam 409 como o PDF pede.
