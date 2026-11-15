# EcoScoreEngine-API (Java) — resumo técnico

- Repositório: https://github.com/Leonardo-2112/EcoScoreEngine-API (deploy citado no README: https://ecoscoreengine-api.onrender.com)
- O que fazia: API REST do EcoScore Engine (GaiaTech, Challenge 2026 Sprint 4, 1TDSPV) que transformava ações sustentáveis em pontos, missões, níveis, créditos e saque em R$, com módulo B2B de campanhas ESG para empresas.

## Stack e versões

| Item | Valor | Fonte |
|---|---|---|
| Java | 21 | `pom.xml` (`java.version`) |
| Spring Boot | 4.1.2 (`spring-boot-starter-parent`) | `pom.xml` |
| Web | `spring-boot-starter-webmvc` (Spring MVC + Tomcat + Jackson) | `pom.xml` |
| Validação | `spring-boot-starter-validation` (Bean Validation, `jakarta.validation`) | `pom.xml` |
| Acesso a dados | `spring-boot-starter-jdbc` (só para o DataSource/HikariCP) — sem JPA | `pom.xml` |
| Driver | `com.oracle.database.jdbc:ojdbc17` (runtime) | `pom.xml` |
| Conversão DTO | `org.modelmapper:modelmapper` 3.2.0 | `pom.xml` |
| Hash de senha | `spring-security-crypto` (só BCrypt, sem Spring Security completo) | `pom.xml` |
| Build | Maven Wrapper (Maven 3.10.0), `finalName` = `ecoscore-api` | `.mvn/wrapper/maven-wrapper.properties`, `pom.xml` |
| Imagem | `eclipse-temurin:21-jdk` (build) → `eclipse-temurin:21-jre` (run) | `Dockerfile` |
| Pool | HikariCP, `maximum-pool-size=${DB_POOL_SIZE:4}`, `minimum-idle=1` | `application.properties` |

## Estrutura de pacotes

```
src/main/java/br/com/soulprime/
├── EcoScoreEngineApiApplication.java  @SpringBootApplication; fixa TimeZone America/Sao_Paulo
├── factory/    ConnectionFactory      @Component que recebe o DataSource e entrega Connection
├── config/     CorsFilter, ModelMapperConfig
├── model/      15 classes (1 por tabela), POJOs com associações por objeto
│   └── enums/  Perfil, StatusValidacao, StatusCampanha, TipoEvidencia...
├── dao/        14 DAOs @Repository (SQL + PreparedStatement + montagem do objeto)
├── bo/         @Service com regras de negócio, controle de acesso e transações
├── dto/        XxxRequestDto (entrada, Bean Validation), XxxResponseDto (saída), ErrorResponseDto
├── resource/   11 @RestController (equivalem aos "controllers")
└── exception/  7 exceções próprias + ApiExceptionHandler (@RestControllerAdvice)
src/main/resources/application.properties
```

Fluxo (do README): `CorsFilter → *Resource → *Bo → *Dao → ConnectionFactory → Oracle`; falhas → exceção → `ApiExceptionHandler` → `ErrorResponseDto`.

## Padrões que usamos

### Entidade / model
POJO puro, sem anotação, com construtor vazio + construtor só com id, getters/setters, associações como objeto e métodos de domínio simples (`isCreditado()`, `isAtivo()`). Ex.: `model/CategoriaAcao.java`, `model/RegistroAcao.java`:
```java
public class RegistroAcao {
    private int id;
    private Usuario usuario;        // FK como objeto
    private Acao acao;
    private LocalDateTime dataRealizacao;
    private StatusValidacao validacao;  // enum
    public boolean isCreditado() {
        return validacao == StatusValidacao.VALIDADA || validacao == StatusValidacao.PARCIAL;
    }
```
Status sempre como `enum` em `model/enums/`.

### Acesso a dados — JDBC puro
- Sem JPA/Hibernate/Spring Data. `ConnectionFactory` (`factory/ConnectionFactory.java`) recebe o `DataSource` do Spring (Hikari) pelo construtor e expõe `getConnection()`.
- Cada DAO recebe a `ConnectionFactory` pelo construtor (não o `DataSource` direto), guarda o SQL em constantes `static final`, usa try-with-resources e um método estático `getXxx(ResultSet)` para montar o model. Ex.: `dao/CategoriaAcaoDao.java`:
```java
private static final String INSERT_SQL = "INSERT INTO TB_CATEGORIA_ACAO (NM_CATEGORIA, DS_CATEGORIA) VALUES (?, ?)";
public void cadastrar(CategoriaAcao categoria) throws SQLException {
    try (Connection conexao = connectionFactory.getConnection();
         PreparedStatement stmt = conexao.prepareStatement(INSERT_SQL, new String[] {"ID_CATEGORIA"})) {
        stmt.setString(1, categoria.getNome());
        stmt.setString(2, categoria.getDescricao());
        stmt.executeUpdate();
        ResultSet resultSet = stmt.getGeneratedKeys();
        if (resultSet.next()) categoria.setId(resultSet.getInt(1));
    }
}
```
- `buscarPorId` lança `EntidadeNaoEncontradaException` quando o `ResultSet` vem vazio; `atualizar`/`remover` lançam a mesma exceção quando `executeUpdate() == 0`.
- **Sequences:** nenhum `NEXTVAL`/`SQ_` no código. O id é lido com `getGeneratedKeys()` passando o nome da coluna, o que indica coluna IDENTITY ou trigger no DDL (o DDL não está no repositório; não dá para confirmar).
- **Transações:** operações que gravam em várias tabelas ficam no BO, com uma `Connection` compartilhada e passada aos DAOs (`registroAcaoDao.cadastrar(conexao, registro)`), `setAutoCommit(false)` + `commit()`/`rollback()` (`bo/RegistroAcaoBo.java`, `CarteiraBo`, `AuthBo`, `CampanhaBo`, `EmpresaBo`, `MissaoBo`). Leitura com bloqueio `SELECT ... FOR UPDATE` em `UsuarioDao`, `CarteiraDao`, `RegistroAcaoDao`.

### DTOs e ModelMapper
- `config/ModelMapperConfig.java` expõe `@Bean ModelMapper` com configuração padrão (sem `typeMap`/`addMappings`).
- Resources injetam o `ModelMapper` e convertem nos dois sentidos: `mapper.map(dto, CategoriaAcao.class)` na entrada e `mapper.map(model, CategoriaResponseDto.class)` na saída. O "achatamento" automático é usado: `CarteiraResponseDto.usuarioId` ← `Carteira.usuario.id`.
- Também há DTOs de resumo para aninhar (`UsuarioResumoDto`, `AcaoResumoDto`, `EmpresaResumoDto`, `CampanhaResumoDto`).

### Validação (Bean Validation)
Anotações nos `*RequestDto` com mensagem em português e `@Valid @RequestBody` no resource. Usadas: `@NotBlank`, `@NotNull`, `@Size`, `@Email`, `@Pattern`, `@Min`, `@Max`, `@DecimalMin`, `@Past`. Ex.: `dto/CategoriaRequestDto.java`:
```java
@NotBlank(message = "Informe o nome da categoria.")
@Size(max = 50, message = "Nome com no maximo 50 caracteres.")
private String nome;
```
Validações que dependem de outro campo ficam no BO (`DadosInvalidosException`) e utilitários em `bo/ValidadorDados.java`.

### Controllers (resources) e status HTTP
`resource/CategoriaResource.java` é o modelo de CRUD:
```java
@PostMapping
public ResponseEntity<CategoriaResponseDto> cadastrar(..., @Valid @RequestBody CategoriaRequestDto dto, UriComponentsBuilder builder) throws SQLException {
    CategoriaAcao categoria = categoriaBo.cadastrar(usuarioLogado, mapper.map(dto, CategoriaAcao.class));
    URI uri = builder.path("/categorias/{id}").buildAndExpand(categoria.getId()).toUri();
    return ResponseEntity.created(uri).body(mapper.map(categoria, CategoriaResponseDto.class));
}
@DeleteMapping("/{id}")
public ResponseEntity<Void> remover(..., @PathVariable int id) throws ... {
    categoriaBo.remover(usuarioLogado, id);
    return ResponseEntity.noContent().build();
}
```
- 201 + `Location` (via `UriComponentsBuilder`), 200 (`ResponseEntity.ok` ou retorno direto de `List`), 204 (`noContent()`), 404 (`EntidadeNaoEncontradaException`), 409 (`ConflitoException` — nome duplicado, categoria com filhos), 422 (`RegraNegocioException`), 401/403/423 (acesso), 405, 500, 503 (health sem banco).
- Rotas aninhadas: `/usuarios/{id}/registros`, `/usuarios/{id}/conversoes`, `/campanhas/{id}/metricas`; filtros por query string (`?status=&categoriaId=`).
- `HealthResource`: `GET /` (info) e `GET /health` (testa `conexao.isValid(5)`; 200 ou 503).
- Identificação do usuário pelo header `X-Usuario-Id` checado em `bo/AcessoBo.java` (na v1.2 do Documento Base o ZelaBairro passou a usar o mesmo esquema, com o cabeçalho `X-Gestor-Id` conferido em `tb_gestor`; ver seção 8.5).

### Exceções próprias e @RestControllerAdvice
- `exception/`: `EntidadeNaoEncontradaException` (checked, `extends Exception`), `ConflitoException`, `RegraNegocioException`, `DadosInvalidosException`, `NaoAutenticadoException`, `AcessoNegadoException`, `ContaBloqueadaException` (todas `RuntimeException`).
- `exception/ApiExceptionHandler.java` mapeia cada uma para um status e ainda trata `MethodArgumentNotValidException` (400), `HttpMessageNotReadableException` (400 JSON inválido), `MethodArgumentTypeMismatchException` (400), `NoResourceFoundException` (404), `HttpRequestMethodNotSupportedException` (405), `SQLIntegrityConstraintViolationException` (409), `SQLException` e `Exception` (500 com mensagem genérica, sem SQL).
- Formato de erro: `ErrorResponseDto {erro, detalhe}`, ex. `{"erro": "Not Found", "detalhe": "Acao 999 nao encontrada."}`. No 400 de Bean Validation devolve um `Map` campo → mensagem (`{"email": "E-mail invalido."}`), fora do formato padrão.

### CORS
Filtro próprio `config/CorsFilter.java` (`@Component`, `@Order(HIGHEST_PRECEDENCE)`, `implements Filter`): lê `app.cors.origins=${CORS_ORIGINS:*}`, devolve a origem se estiver na lista, libera `GET, POST, PUT, PATCH, DELETE, OPTIONS`, expõe o header `Location` e responde 200 no preflight `OPTIONS`.

### Configuração por variáveis de ambiente
`application.properties`: `server.port=${PORT:8080}`, `spring.datasource.url=${DB_URL}`, `username=${DB_USER}`, `password=${DB_PASSWORD}`, `${DB_POOL_SIZE:4}`, `${CORS_ORIGINS:*}`. Também `spring.jackson.default-property-inclusion=non_null`, `spring.mvc.problemdetails.enabled=false`, `server.error.include-message=always`. `.env` no `.dockerignore`/fora do Git; o README cita `.env.example`, mas ele não está no clone.

### Dockerfile — multi-stage
```dockerfile
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN chmod +x mvnw && ./mvnw -B -q dependency:go-offline
COPY src/ src/
RUN ./mvnw -B -q package -DskipTests
FROM eclipse-temurin:21-jre
COPY --from=build /app/target/ecoscore-api.jar app.jar
ENTRYPOINT ["sh", "-c", "java -Xmx384m -jar app.jar"]
```
(Também `ENV TZ=America/Sao_Paulo` e `EXPOSE 8080`.)

### Testes e Swagger/OpenAPI
Não há. A pasta `src/` só tem `main/` (sem `src/test`), nenhum `@Test`, nenhuma dependência springdoc/swagger.

## Como rodava / deploy
- Local: copiar `.env.example` → `.env` com `DB_URL`, `DB_USER`, `DB_PASSWORD`; `set -a; . ./.env; set +a; ./mvnw spring-boot:run`; testar `http://localhost:8080/health` (esperado `{"status":"UP","banco":"UP"}`). Pela IDE: importar como Maven e definir as 3 variáveis na Run Configuration.
- Docker: `docker build -t ecoscore-api .` e `docker run -p 8080:8080 --env-file .env ecoscore-api`.
- Nuvem: Render via Dockerfile (porta pela variável `PORT`), front na Vercel com `CORS_ORIGINS`. Banco: Oracle da FIAP com tabelas criadas pelos scripts da disciplina de BD (`00_EcoScore_DDL.sql`, `01_EcoScore_Carga_Inicial.sql`, não incluídos no repositório).
- Entrega: `entrega/EcoScoreEngine-API.zip` (142 arquivos), PDF em `docs/`, diagramas de classes e MER em `docs/diagramas/`.

## Mapa para o ZelaBairro

| Padrão encontrado | Como aplicar no ZelaBairro |
|---|---|
| Model POJO + construtor `(int id)` + FK como objeto | `Ocorrencia` com `Cidadao autor`, `Categoria categoria`, `Bairro bairro`; `Categoria` com `Orgao orgao` (só leitura); `Atualizacao` com `Ocorrencia`; `Apoio` com `Cidadao` + `Ocorrencia` |
| Status como enum em `model/enums` | `StatusOcorrencia {ABERTA, EM_ANDAMENTO, RESOLVIDA, CANCELADA}`, com método `podeIrPara(novo)` para RN05; `Prioridade {ALTA, MEDIA, BAIXA}` |
| SQL em constantes + `getXxx(ResultSet)` | `OcorrenciaDao.getOcorrencia(rs)` lendo `cd_ocorrencia`, `ds_ocorrencia`, `st_ocorrencia`, `dt_abertura`... com JOIN em `tb_categoria`, `tb_orgao`, `tb_bairro`, `tb_cidadao` |
| `getGeneratedKeys(new String[]{"ID_..."})` | Trocar por `VALUES (sq_tb_ocorrencia.NEXTVAL, ?, ...)` e ler a chave com `new String[]{"cd_ocorrencia"}` |
| 404 por `ResultSet` vazio / `executeUpdate()==0` | Igual em todos os DAOs de `Cidadao`, `Bairro`, `Categoria`, `Ocorrencia` |
| `existeNome(...)` + `ConflitoException` (409) | `CidadaoDao.existeEmail` (RN02), `BairroDao`/`CategoriaDao.contarOcorrencias` antes do DELETE (RN14) |
| Transação no BO com uma `Connection` | `POST /ocorrencias/{id}/atualizacoes`: inserir `tb_atualizacao` + `UPDATE tb_ocorrencia` (status e `dt_resolucao`, RN06) com commit/rollback |
| `RegraNegocioException` | Transição inválida (RN05), apoio duplicado/próprio/fechado (RN08), edição fora de ABERTA (RN09) — mas devolvendo **409**, não 422 |
| `RequestDto` com Bean Validation | `OcorrenciaRequestDto` (`@NotBlank @Size(min=10,max=500)`, `@NotNull @Positive` nos ids), `CidadaoRequestDto` (`@Email`), `AtualizacaoRequestDto`, `ApoioRequestDto` |
| `ResponseDto` + `ResumoDto` aninhado | `OcorrenciaResponseDto` com `CategoriaResumoDto`, `BairroResumoDto`, `autor` = primeiro nome (RN13), campos calculados (RN10/RN11) |
| ModelMapper com achatamento | `categoria.orgao.nome` → `orgao`; campos calculados preenchidos no BO após o `map` |
| `ResponseEntity.created(uri)` / `noContent()` | Todos os POST (inclusive aninhados) e DELETE da seção 8.2 |
| `CorsFilter` com `CORS_ORIGINS` | Reaproveitar praticamente igual, liberando o cabeçalho `X-Gestor-Id` (v1.2) nos headers permitidos do CORS |
| `HealthResource` `/health` | Manter para o Render e para checar o banco antes da demo |
| Dockerfile multi-stage | Reaproveitar, trocando o nome do jar |

## Lacunas frente às exigências da GS 2026/2

1. **Nomes de colunas**: chaves `ID_` (ex.: `ID_CATEGORIA`) em vez de `cd_`; status em `DS_STATUS`/`DS_VALIDACAO` em vez de `st_`; tabelas e colunas em maiúsculas. Exigido: `tb_`, `cd_`, `nm_`, `ds_`, `dt_`, `st_`, `nr_`, `fl_`.
2. **Sequences**: o código não usa `sq_tb_*.NEXTVAL`; depende de geração automática no banco. A GS exige sequence `sq_tb_nome`.
3. **DataSource no DAO**: os DAOs recebem `ConnectionFactory` (que encapsula o DataSource). A GS pede "DataSource recebido pelo construtor" no DAO — mais seguro injetar `DataSource` direto ou explicar a factory como wrapper.
4. **Nome dos pacotes**: `resource` em vez de `controller`; handler dentro de `exception` (não há pacote `handler`); camadas extras `bo` e `factory`. A GS lista `model/dao/dto/controller/exception/handler/config`.
5. **Formato de erro**: `{erro, detalhe}` e, no 400, um `Map` solto. O Documento Base pede `{status, erro, mensagem, caminho, timestamp, campos[]}` em todos os erros.
6. **Status da regra de negócio**: usava 422 (`UNPROCESSABLE_CONTENT`); a GS define 409 para regra violada e remoção com filhos.
7. **Script SQL**: DDL/carga não estavam no repositório; a GS exige o script de tabelas e sequences dentro do .zip.
8. **Integração externa**: não havia chamada a outra API; o ZelaBairro precisa de `IA_API_URL` e fallback (RN12).
9. **Datas**: models com `LocalDateTime`; o JSON do ZelaBairro pede `AAAA-MM-DD` (usar `LocalDate` nos DTOs).
10. Sem testes automatizados e sem Swagger (não exigidos, mas a demo será por Insomnia/Postman).

Já atendia: JDBC puro sem JPA, ModelMapper, Bean Validation com `@Valid`, `@RestControllerAdvice` sem stack trace/SQL, 201+Location/204/404/405/409, CORS, variáveis de ambiente (`DB_URL`, `DB_USER`, `DB_PASSWORD`, `CORS_ORIGINS` com os mesmos nomes), Docker multi-stage e Render.

## Esqueleto sugerido para a API do ZelaBairro

```
br/com/<grupo>/zelabairro/
├── ZelaBairroApiApplication.java
├── config/      CorsConfig (filtro, CORS_ORIGINS), ModelMapperConfig, RestClientConfig (IA_API_URL)
├── model/       Cidadao, Bairro, Orgao, Categoria, Ocorrencia, Atualizacao, Apoio
│   └── enums/   StatusOcorrencia, Prioridade
├── dao/         CidadaoDao, BairroDao, CategoriaDao, OcorrenciaDao, AtualizacaoDao, ApoioDao
│                (DataSource no construtor; SQL com sq_tb_*.NEXTVAL; métodos com Connection p/ transação)
├── service/     CidadaoService, BairroService, CategoriaService, OcorrenciaService,
│                AtualizacaoService, ApoioService, PrioridadeService (RN10/RN11), IaClient (RN12)
├── dto/         CidadaoRequestDto/ResponseDto, BairroRequestDto/ResponseDto, CategoriaRequestDto/ResponseDto,
│                OcorrenciaRequestDto/ResponseDto, AtualizacaoRequestDto/ResponseDto, ApoioRequestDto/ResponseDto,
│                CategoriaResumoDto, BairroResumoDto, ErroResponseDto, CampoErroDto, PainelBairroDto
├── controller/  CidadaoController, BairroController, CategoriaController, OcorrenciaController
│                (inclui /ocorrencias/{id}/atualizacoes e /apoios), PainelController, HealthController
├── exception/   RecursoNaoEncontradoException (404), ConflitoException (409),
│                RegraNegocioException (409, mensagem com "RNxx")
└── handler/     GlobalExceptionHandler (@RestControllerAdvice → ErroResponseDto)
src/main/resources/application.properties  (PORT, DB_URL, DB_USER, DB_PASSWORD, IA_API_URL, CORS_ORIGINS)
sql/zelabairro_ddl.sql · Dockerfile (multi-stage) · README.md
```
Observação: a camada `service` (o antigo `bo`) não é exigida pela GS, mas o grupo já sabe explicá-la; se mantida, apresentar como "onde ficam as regras RNxx e as transações".

## Termos que o grupo já domina

- Camadas controller (resource) → service (BO) → DAO → banco; padrão DAO e Connection Factory
- JDBC: `DataSource`, `Connection`, `PreparedStatement`, `ResultSet`, try-with-resources, `getGeneratedKeys`
- Transação manual: `setAutoCommit(false)`, `commit`, `rollback`; `SELECT ... FOR UPDATE`
- Pool de conexões HikariCP
- DTO de entrada/saída e ModelMapper (inclusive achatamento `usuario.id` → `usuarioId`)
- Bean Validation com `@Valid` (`@NotBlank`, `@Size`, `@Email`, `@Pattern`, `@NotNull`, `@Past`)
- `@RestControllerAdvice` + `@ExceptionHandler`; exceções próprias checked e unchecked
- `ResponseEntity`, 201 + `Location` com `UriComponentsBuilder`, 204, 404, 405, 409
- CORS e requisição preflight `OPTIONS`
- Variáveis de ambiente com `${VAR:padrao}`, Dockerfile multi-stage, deploy no Render, health check
