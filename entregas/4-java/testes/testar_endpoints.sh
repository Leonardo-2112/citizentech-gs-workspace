#!/usr/bin/env bash
# Testa todos os endpoints da API ZelaBairro (Documento Base 8.2) com curl e confere o status HTTP.
# Uso:  ./testar_endpoints.sh [URL_BASE]      (padrao: http://localhost:8080)
# Precisa de: curl, jq e python3. Roda contra um banco com o seed do zelabairro.sql.
# Cria registros de teste (cidadao, gestor, bairro, categoria, ocorrencias) e remove o que der.
# As senhas abaixo sao de contas de TESTE criadas pelo proprio script, nao do banco.

BASE="${1:-http://localhost:8080}"
SUF="$(date +%s)"                 # sufixo para e-mails e nomes unicos a cada execucao
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
OK=0; FALHA=0

# req NOME STATUS_ESPERADO METODO ROTA [corpo-json] [cabecalhos...]
req() {
  local nome="$1" esperado="$2" metodo="$3" rota="$4" corpo="${5:-}"; shift 5 2>/dev/null || shift $#
  local args=(-s -o "$TMP/corpo" -D "$TMP/cab" -w '%{http_code}' -X "$metodo" "$BASE$rota")
  [ -n "$corpo" ] && args+=(-H 'Content-Type: application/json' --data "$corpo")
  for h in "$@"; do args+=(-H "$h"); done
  STATUS=$(curl "${args[@]}")
  BODY=$(cat "$TMP/corpo")
  LOCATION=$(grep -i '^location:' "$TMP/cab" | tr -d '\r' | cut -d' ' -f2)
  if [ "$STATUS" = "$esperado" ]; then OK=$((OK+1)); r="OK   "; else FALHA=$((FALHA+1)); r="FALHA"; fi
  echo "[$r] $nome"
  echo "        $metodo $rota -> $STATUS (esperado $esperado)${LOCATION:+  Location: $LOCATION}"
  echo "        $(echo "$BODY" | head -c 300)"
}
# envia arquivo multipart: upl NOME ESPERADO ROTA ARQUIVO [cabecalho]
upl() {
  local nome="$1" esperado="$2" rota="$3" arq="$4" cab="${5:-X-Nada: 0}"
  STATUS=$(curl -s -o "$TMP/corpo" -D "$TMP/cab" -w '%{http_code}' -X POST "$BASE$rota" -H "$cab" -F "arquivo=@$arq")
  BODY=$(cat "$TMP/corpo"); LOCATION=$(grep -i '^location:' "$TMP/cab" | tr -d '\r' | cut -d' ' -f2)
  if [ "$STATUS" = "$esperado" ]; then OK=$((OK+1)); r="OK   "; else FALHA=$((FALHA+1)); r="FALHA"; fi
  echo "[$r] $nome"
  echo "        POST $rota ($(basename "$arq")) -> $STATUS (esperado $esperado)${LOCATION:+  Location: $LOCATION}"
  echo "        $(echo "$BODY" | head -c 300)"
}
confere() { # confere NOME CONDICAO_BASH
  if eval "$2"; then OK=$((OK+1)); echo "[OK   ] $1"; else FALHA=$((FALHA+1)); echo "[FALHA] $1"; fi
}
id() { echo "$BODY" | jq -r '.id'; }

# Arquivos de teste para as fotos (RN18)
python3 - "$TMP" <<'PY'
import sys, struct, zlib, os
d = sys.argv[1]
def png(w, h):
    raw = b''.join(b'\x00' + b'\x80\x40\x20' * w for _ in range(h))
    def chunk(t, data): return struct.pack('>I', len(data)) + t + data + struct.pack('>I', zlib.crc32(t + data) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')
open(os.path.join(d, 'foto.png'), 'wb').write(png(8, 8))
open(os.path.join(d, 'texto.txt'), 'w').write('isto nao e uma imagem')
open(os.path.join(d, 'grande.jpg'), 'wb').write(b'\xff\xd8\xff\xe0' + os.urandom(3 * 1024 * 1024))
PY

echo "=== ZelaBairro API - teste de endpoints em $BASE ($(date '+%d/%m/%Y %H:%M')) ==="
echo; echo "--- Saude ---"
req "Health: API e banco no ar" 200 GET /health
req "Rota inexistente devolve 404 em JSON" 404 GET /rota-que-nao-existe

echo; echo "--- Cidadaos (cadastro publico) ---"
req "Cadastrar cidadao" 201 POST /cidadaos "{\"nome\":\"Teste Cidadao Silva\",\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"senha123\",\"telefone\":\"(11) 99999-0000\"}"
CID=$(id)
confere "Resposta do cadastro nao traz senha (RN15)" '! echo "$BODY" | grep -qi senha'
req "Cadastrar com e-mail repetido (RN02)" 409 POST /cidadaos "{\"nome\":\"Outro\",\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"senha123\"}"
req "Cadastro invalido devolve 400 com campos" 400 POST /cidadaos '{"nome":"","email":"nao-e-email","senha":"123"}'
confere "Erro 400 lista os campos invalidos" '[ "$(echo "$BODY" | jq ".campos | length")" -ge 3 ]'
req "JSON mal formado" 400 POST /cidadaos '{"nome": '
req "Listar cidadaos (RN13: so primeiro nome)" 200 GET /cidadaos
confere "Listagem publica sem e-mail (RN13)" '! echo "$BODY" | grep -q "@"'
req "Buscar cidadao por id" 200 GET /cidadaos/$CID
req "Buscar cidadao inexistente" 404 GET /cidadaos/999999
req "Atualizar cidadao" 200 PUT /cidadaos/$CID "{\"nome\":\"Teste Cidadao Souza\",\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"senha456\",\"telefone\":\"(11) 98888-0000\"}"

echo; echo "--- Login (RN15) ---"
req "Login do cidadao" 200 POST /auth/login "{\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"senha456\"}"
confere "Perfil CIDADAO no login" '[ "$(echo "$BODY" | jq -r .perfil)" = "CIDADAO" ]'
req "Login com senha errada" 401 POST /auth/login "{\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"errada99\"}"
req "Login com e-mail inexistente (mesma mensagem)" 401 POST /auth/login '{"email":"ninguem@email.exemplo.com","senha":"qualquer1"}'
req "Login sem e-mail" 400 POST /auth/login '{"senha":"x"}'

echo; echo "--- Gestores (RN16, RN17) ---"
GBODY="{\"nome\":\"Gestor Teste\",\"email\":\"gestor.$SUF@prefeitura.exemplo.gov.br\",\"senha\":\"gestor123\",\"idOrgao\":1}"
req "Cadastrar gestor sem X-Gestor-Id" 403 POST /gestores "$GBODY"
req "Cadastrar gestor com X-Gestor-Id inexistente" 403 POST /gestores "$GBODY" "X-Gestor-Id: 999999"
req "Gestor 1 (seed) cadastra outro gestor" 201 POST /gestores "$GBODY" "X-Gestor-Id: 1"
GID=$(id)
confere "Fica registrado quem cadastrou (RN17)" '[ "$(echo "$BODY" | jq -r .idGestorCadastro)" = "1" ]'
req "Gestor com e-mail ja usado por cidadao (RN02)" 409 POST /gestores "{\"nome\":\"Gestor Dup\",\"email\":\"teste.$SUF@email.exemplo.com\",\"senha\":\"gestor123\",\"idOrgao\":1}" "X-Gestor-Id: 1"
req "Gestor com orgao inexistente" 404 POST /gestores "{\"nome\":\"Gestor X\",\"email\":\"x.$SUF@prefeitura.exemplo.gov.br\",\"senha\":\"gestor123\",\"idOrgao\":999}" "X-Gestor-Id: 1"
req "Login do gestor" 200 POST /auth/login "{\"email\":\"gestor.$SUF@prefeitura.exemplo.gov.br\",\"senha\":\"gestor123\"}"
confere "Perfil GESTOR no login" '[ "$(echo "$BODY" | jq -r .perfil)" = "GESTOR" ]'
req "Listar gestores" 200 GET /gestores "" "X-Gestor-Id: 1"
req "Listar gestores sem cabecalho" 403 GET /gestores
req "Buscar gestor" 200 GET /gestores/$GID "" "X-Gestor-Id: 1"
req "Buscar gestor inexistente" 404 GET /gestores/999999 "" "X-Gestor-Id: 1"
req "Atualizar gestor" 200 PUT /gestores/$GID "{\"nome\":\"Gestor Teste Editado\",\"email\":\"gestor.$SUF@prefeitura.exemplo.gov.br\",\"senha\":\"gestor123\",\"idOrgao\":3}" "X-Gestor-Id: 1"
req "Listar orgaos (so leitura)" 200 GET /orgaos

echo; echo "--- Bairros (RN14) ---"
req "Cadastrar bairro" 201 POST /bairros "{\"nome\":\"Bairro Teste $SUF\",\"subprefeitura\":\"Lapa\",\"populacao\":1000}"
BID=$(id)
req "Bairro repetido" 409 POST /bairros "{\"nome\":\"Bairro Teste $SUF\",\"subprefeitura\":\"Lapa\"}"
req "Bairro invalido" 400 POST /bairros '{"nome":"","populacao":-5}'
req "Listar bairros" 200 GET /bairros
req "Buscar bairro" 200 GET /bairros/$BID
req "Buscar bairro inexistente" 404 GET /bairros/999999
req "Atualizar bairro" 200 PUT /bairros/$BID "{\"nome\":\"Bairro Teste $SUF B\",\"subprefeitura\":\"Lapa\",\"populacao\":2000}"
req "Ocorrencias do bairro 1 (1:N)" 200 GET /bairros/1/ocorrencias
req "Ocorrencias de bairro inexistente" 404 GET /bairros/999999/ocorrencias
req "Excluir bairro com ocorrencias (RN14)" 409 DELETE /bairros/1

echo; echo "--- Categorias (RN14) ---"
req "Cadastrar categoria" 201 POST /categorias "{\"nome\":\"Categoria Teste $SUF\",\"descricao\":\"Teste\",\"prazoDias\":12,\"gravidade\":3,\"idOrgao\":1}"
KID=$(id)
req "Categoria com gravidade 6" 400 POST /categorias '{"nome":"X","prazoDias":12,"gravidade":6,"idOrgao":1}'
req "Categoria com orgao inexistente" 404 POST /categorias "{\"nome\":\"Cat $SUF\",\"prazoDias\":12,\"gravidade\":3,\"idOrgao\":999}"
req "Categoria com nome repetido" 409 POST /categorias '{"nome":"Buraco na via","prazoDias":12,"gravidade":3,"idOrgao":1}'
req "Listar categorias" 200 GET /categorias
req "Buscar categoria" 200 GET /categorias/$KID
req "Atualizar categoria" 200 PUT /categorias/$KID "{\"nome\":\"Categoria Teste $SUF B\",\"prazoDias\":20,\"gravidade\":2,\"idOrgao\":4}"
req "Ocorrencias da categoria 1 (1:N)" 200 GET /categorias/1/ocorrencias
req "Excluir categoria com ocorrencias (RN14)" 409 DELETE /categorias/1

echo; echo "--- Ocorrencias (RN03, RN04, RN09, RN10, RN12) ---"
req "Registrar ocorrencia" 201 POST /ocorrencias "{\"descricao\":\"Buraco grande perto do ponto de onibus\",\"endereco\":\"Rua de Teste, 100\",\"idCidadao\":$CID,\"idCategoria\":1,\"idBairro\":1}"
OID=$(id)
confere "Nasce ABERTA (RN04)" '[ "$(echo "$BODY" | jq -r .status)" = "ABERTA" ]'
# Com IA_API_URL configurada e a Flask acordada, a previsao vem preenchida; sem IA (ou IA fora do ar), vem nula (RN12)
if [ "$(echo "$BODY" | jq -r .prazoPrevistoDias)" = "null" ]; then
  confere "Sem previsao da IA: prazo e risco nulos (RN12)" '[ "$(echo "$BODY" | jq -r .riscoAtraso)" = "null" ]'
else
  confere "Previsao da IA gravada: prazo em dias e risco ALTO/BAIXO (D4)" '[ "$(echo "$BODY" | jq -r ".prazoPrevistoDias > 0 and (.riscoAtraso == \"ALTO\" or .riscoAtraso == \"BAIXO\")")" = "true" ]'
fi
confere "Autor so com primeiro nome (RN13)" '[ "$(echo "$BODY" | jq -r .autor)" = "Teste" ]'
req "Descricao curta (RN03)" 400 POST /ocorrencias "{\"descricao\":\"curta\",\"endereco\":\"\",\"idCidadao\":$CID,\"idCategoria\":1,\"idBairro\":1}"
req "Categoria inexistente" 404 POST /ocorrencias "{\"descricao\":\"Descricao valida com mais de dez\",\"endereco\":\"Rua X\",\"idCidadao\":$CID,\"idCategoria\":999,\"idBairro\":1}"
req "Listar ocorrencias (por prioridade, RN10)" 200 GET /ocorrencias
confere "Lista ordenada pela pontuacao (maior primeiro)" '[ "$(echo "$BODY" | jq "[.[].pontuacaoPrioridade | select(. != null)] | . == (sort | reverse)")" = "true" ]'
req "Filtrar por status e bairro" 200 GET "/ocorrencias?status=ABERTA&idBairro=1"
req "Filtro com status invalido" 400 GET "/ocorrencias?status=QUALQUER"
req "Buscar ocorrencia" 200 GET /ocorrencias/$OID
req "Buscar ocorrencia inexistente" 404 GET /ocorrencias/999999
req "Editar ocorrencia ABERTA" 200 PUT /ocorrencias/$OID '{"descricao":"Buraco grande perto do ponto de onibus (editado)","endereco":"Rua de Teste, 102","idCategoria":1,"idBairro":1}'
req "Metodo nao suportado" 405 PATCH /ocorrencias/$OID

echo; echo "--- Apoios (RN08) ---"
req "Autor apoiando a propria ocorrencia" 409 POST /ocorrencias/$OID/apoios "{\"idCidadao\":$CID}"
req "Cidadao 2 apoia" 201 POST /ocorrencias/$OID/apoios '{"idCidadao":2}'
req "Apoio repetido" 409 POST /ocorrencias/$OID/apoios '{"idCidadao":2}'
req "Apoio sem idCidadao" 400 POST /ocorrencias/$OID/apoios '{}'
req "Listar apoios" 200 GET /ocorrencias/$OID/apoios
req "Buscar apoio" 200 GET /ocorrencias/$OID/apoios/2
req "Retirar apoio" 204 DELETE /ocorrencias/$OID/apoios/2
req "Retirar apoio que nao existe" 404 DELETE /ocorrencias/$OID/apoios/2
req "Cidadao 3 apoia de novo" 201 POST /ocorrencias/$OID/apoios '{"idCidadao":3}'

echo; echo "--- Atualizacoes de status (RN05, RN06, RN16) ---"
req "Mudar status sem ser gestor" 403 POST /ocorrencias/$OID/atualizacoes '{"status":"EM_ANDAMENTO"}'
req "Transicao proibida ABERTA -> RESOLVIDA (RN05)" 409 POST /ocorrencias/$OID/atualizacoes '{"status":"RESOLVIDA"}' "X-Gestor-Id: $GID"
req "Status invalido" 400 POST /ocorrencias/$OID/atualizacoes '{"status":"PARADA"}' "X-Gestor-Id: $GID"
req "Gestor muda para EM_ANDAMENTO" 201 POST /ocorrencias/$OID/atualizacoes '{"status":"EM_ANDAMENTO","comentario":"Equipe agendada"}' "X-Gestor-Id: $GID"
AID=$(id)
req "Listar historico (1:N)" 200 GET /ocorrencias/$OID/atualizacoes
req "Buscar atualizacao" 200 GET /ocorrencias/$OID/atualizacoes/$AID
req "Corrigir comentario" 200 PUT /ocorrencias/$OID/atualizacoes/$AID '{"comentario":"Equipe agendada para amanha"}' "X-Gestor-Id: $GID"
req "Editar ocorrencia EM_ANDAMENTO (RN09)" 409 PUT /ocorrencias/$OID '{"descricao":"Nao pode mais editar esta ocorrencia","endereco":"Rua X","idCategoria":1,"idBairro":1}'
req "Gestor resolve" 201 POST /ocorrencias/$OID/atualizacoes '{"status":"RESOLVIDA","comentario":"Buraco tapado"}' "X-Gestor-Id: $GID"
req "Ocorrencia resolvida" 200 GET /ocorrencias/$OID
confere "dataResolucao preenchida e prioridade nula (RN06, RN10)" '[ "$(echo "$BODY" | jq -r ".dataResolucao != null and .prioridade == null")" = "true" ]'
req "RESOLVIDA e final (RN05)" 409 POST /ocorrencias/$OID/atualizacoes '{"status":"CANCELADA"}' "X-Gestor-Id: $GID"
req "Apoiar ocorrencia resolvida (RN08)" 409 POST /ocorrencias/$OID/apoios '{"idCidadao":4}'
req "Excluir ocorrencia com historico (RN09)" 409 DELETE /ocorrencias/$OID

echo; echo "--- Fotos (RN18) ---"
req "Nova ocorrencia para fotos" 201 POST /ocorrencias "{\"descricao\":\"Lixo acumulado na esquina da praca\",\"endereco\":\"Praca de Teste\",\"idCidadao\":$CID,\"idCategoria\":3,\"idBairro\":$BID}"
FOID=$(id)
upl "Foto sem X-Cidadao-Id" 403 /ocorrencias/$FOID/fotos "$TMP/foto.png"
upl "Foto de quem nao e o autor" 403 /ocorrencias/$FOID/fotos "$TMP/foto.png" "X-Cidadao-Id: 2"
upl "Arquivo que nao e JPG/PNG" 400 /ocorrencias/$FOID/fotos "$TMP/texto.txt" "X-Cidadao-Id: $CID"
upl "Foto maior que 2 MB" 400 /ocorrencias/$FOID/fotos "$TMP/grande.jpg" "X-Cidadao-Id: $CID"
upl "Autor envia foto 1" 201 /ocorrencias/$FOID/fotos "$TMP/foto.png" "X-Cidadao-Id: $CID"
FID=$(id)
upl "Autor envia foto 2" 201 /ocorrencias/$FOID/fotos "$TMP/foto.png" "X-Cidadao-Id: $CID"
upl "Autor envia foto 3" 201 /ocorrencias/$FOID/fotos "$TMP/foto.png" "X-Cidadao-Id: $CID"
upl "Quarta foto" 409 /ocorrencias/$FOID/fotos "$TMP/foto.png" "X-Cidadao-Id: $CID"
req "Listar fotos (sem os bytes)" 200 GET /ocorrencias/$FOID/fotos
TIPO=$(curl -s -o /dev/null -w '%{content_type}' "$BASE/fotos/$FID")
confere "GET /fotos/{id} devolve a imagem (image/png)" '[ "$TIPO" = "image/png" ]'
req "Foto inexistente" 404 GET /fotos/999999
req "Remover foto (autor)" 204 DELETE /ocorrencias/$FOID/fotos/$FID "" "X-Cidadao-Id: $CID"
req "Remover foto sem ser autor" 403 DELETE /ocorrencias/$FOID/fotos/$((FID+1)) "" "X-Cidadao-Id: 2"
req "Excluir ocorrencia sem apoios/historico (fotos saem junto)" 204 DELETE /ocorrencias/$FOID
req "Ocorrencia excluida" 404 GET /ocorrencias/$FOID

echo; echo "--- Painel do gestor ---"
req "Painel sem ser gestor" 403 GET /painel/bairros
req "Painel por bairro" 200 GET /painel/bairros "" "X-Gestor-Id: 1"

echo; echo "--- CORS ---"
CORS=$(curl -s -o /dev/null -D - -X OPTIONS "$BASE/ocorrencias" -H 'Origin: http://localhost:5173' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: X-Gestor-Id' | tr -d '\r')
confere "Preflight libera http://localhost:5173 e X-Gestor-Id/X-Cidadao-Id" 'echo "$CORS" | grep -qi "access-control-allow-origin: http://localhost:5173" && echo "$CORS" | grep -qi "X-Gestor-Id, X-Cidadao-Id"'
CORS2=$(curl -s -o /dev/null -D - "$BASE/health" -H 'Origin: https://site-estranho.exemplo.com' | tr -d '\r')
confere "Origem nao liberada nao recebe Allow-Origin" '! echo "$CORS2" | grep -qi "access-control-allow-origin"'

echo; echo "--- Remocoes finais ---"
req "Excluir cidadao com ocorrencias" 409 DELETE /cidadaos/$CID
req "Excluir gestor com atualizacoes" 409 DELETE /gestores/$GID "" "X-Gestor-Id: 1"
req "Cadastrar gestor descartavel" 201 POST /gestores "{\"nome\":\"Gestor Descartavel\",\"email\":\"desc.$SUF@prefeitura.exemplo.gov.br\",\"senha\":\"gestor123\",\"idOrgao\":2}" "X-Gestor-Id: 1"
req "Excluir gestor sem vinculos" 204 DELETE /gestores/$(id) "" "X-Gestor-Id: 1"
req "Cadastrar cidadao descartavel" 201 POST /cidadaos "{\"nome\":\"Cidadao Descartavel\",\"email\":\"desc.$SUF@email.exemplo.com\",\"senha\":\"senha123\"}"
req "Excluir cidadao sem vinculos" 204 DELETE /cidadaos/$(id)
req "Excluir categoria sem ocorrencias" 204 DELETE /categorias/$KID
req "Excluir bairro sem ocorrencias" 204 DELETE /bairros/$BID
req "Excluir de novo" 404 DELETE /bairros/$BID

echo; echo "=== Resultado: $OK OK, $FALHA FALHA ==="
[ "$FALHA" = 0 ]
