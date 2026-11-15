# 4 · Domain Driven Design Using Java — API ZelaBairro

Depende do **Banco** pronto no Oracle. Base: Documento Base v1.3, seção 8 (pacotes, endpoints, JSON, login 8.5, fotos); padrão do projeto anterior em [`docs/referencias/02-EcoScoreEngine-API.md`](../../docs/referencias/02-EcoScoreEngine-API.md); plano seção 3.

## O que colocar nesta pasta
| Arquivo | Conteúdo |
|---|---|
| `zelabairro-api/` | Projeto Spring Boot (pacotes `model`, `dao`, `dto`, `controller`, `exception`, `handler`, `config`) + `Dockerfile` multi-stage |
| `zelabairro.sql` | O **mesmo** script da pasta `2-banco-de-dados` (tabelas e sequences) |
| `documentacao.pdf` | Capa e links, solução, diagrama de classes, DER, endpoints com JSON, pacotes, regras e validações, deploy (nomes das variáveis, sem valores) |
| `README.md` (dentro do projeto) | Integrantes e RM, como rodar, URL do Render e link do vídeo |

## Checklist
- [ ] JDBC puro com `DataSource` no construtor (JPA/Hibernate: −20)
- [ ] DTOs + ModelMapper + Bean Validation; handler com o JSON de erro da seção 8.3 (sem stack trace)
- [ ] Status 201 + Location, 200, 204, 400, 401, 403, 404, 405 e 409 nos casos certos
- [ ] CORS liberando a Vercel e os cabeçalhos `X-Gestor-Id` e `X-Cidadao-Id`
- [ ] Credenciais só em variáveis de ambiente (`DB_URL`, `DB_USER`, `DB_PASSWORD`, `IA_API_URL`, `CORS_ORIGINS`) — senha no código: −10
- [ ] Publicada no Render; zip **sem `target/`**; vídeo de até 5 min mostrando o front integrado
