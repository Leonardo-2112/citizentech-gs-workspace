"""Monta o .zip da entrega de Domain Driven Design Using Java (ZelaBairro).

Uso (nesta pasta):  python montar_zip.py
Saida: ZelaBairro_Java_1TDSPV.zip nesta pasta.

Conteudo do .zip (exigencias do PDF da disciplina):
  README.md                         integrantes e RM, como rodar, URL do Render e link do video
  identificacao.txt                 RM, nome e turma (regra geral da GS)
  documentacao.pdf                  documentacao tecnica (8 itens)
  zelabairro.sql                    script das tabelas, sequences e seed
  ZelaBairro.postman_collection.json  colecao para a demo (Postman/Insomnia)
  testes/                           script de teste com curl e a evidencia da ultima execucao
  zelabairro-api/                   projeto Spring Boot completo com o Dockerfile, SEM a pasta target/

Nunca entram: target/, .env (credenciais), .idea/, .vscode/, o jar do Maven Wrapper.
"""
import sys
import zipfile
from pathlib import Path

PASTA = Path(__file__).resolve().parent
PROJETO = PASTA / "zelabairro-api"
SAIDA = PASTA / "ZelaBairro_Java_1TDSPV.zip"

ARQUIVOS_RAIZ = ["identificacao.txt", "documentacao.pdf", "zelabairro.sql", "ZelaBairro.postman_collection.json"]
TESTES = ["testes/testar_endpoints.sh", "testes/evidencia_curl.txt", "testes/evidencia_integracao_ia.txt",
          "testes/evidencia_render.txt", "testes/evidencia_postman_render.txt"]
IGNORAR_PASTAS = {"target", ".idea", ".vscode", ".settings"}
IGNORAR_ARQUIVOS = {".env", "maven-wrapper.jar", ".classpath", ".project"}


def deve_entrar(caminho: Path) -> bool:
    partes = caminho.relative_to(PROJETO).parts
    if any(p in IGNORAR_PASTAS for p in partes):
        return False
    return caminho.name not in IGNORAR_ARQUIVOS and not caminho.name.endswith(".iml")


def main():
    faltando = [a for a in ARQUIVOS_RAIZ + TESTES if not (PASTA / a).exists()]
    if faltando:
        sys.exit(f"Faltam arquivos: {', '.join(faltando)}")

    with zipfile.ZipFile(SAIDA, "w", zipfile.ZIP_DEFLATED) as z:
        # README na raiz do .zip = o README do projeto
        z.write(PROJETO / "README.md", "README.md")
        for nome in ARQUIVOS_RAIZ + TESTES:
            z.write(PASTA / nome, nome)
        for arquivo in sorted(PROJETO.rglob("*")):
            if arquivo.is_file() and deve_entrar(arquivo):
                info = zipfile.ZipInfo.from_file(arquivo, f"zelabairro-api/{arquivo.relative_to(PROJETO).as_posix()}")
                if arquivo.name == "mvnw" or arquivo.suffix == ".sh":
                    info.external_attr = 0o755 << 16  # mantem permissao de execucao
                with open(arquivo, "rb") as f:
                    z.writestr(info, f.read(), zipfile.ZIP_DEFLATED)

    # Conferencia: nada de target/ nem .env dentro do .zip
    with zipfile.ZipFile(SAIDA) as z:
        nomes = z.namelist()
        proibidos = [n for n in nomes if "/target/" in n or n.endswith("/.env") or n == ".env"]
        if proibidos:
            sys.exit(f"ERRO: o .zip contem arquivos proibidos: {proibidos}")
        if z.testzip() is not None:
            sys.exit("ERRO: .zip corrompido")
    print(f"{SAIDA.name}: {len(nomes)} arquivos, {SAIDA.stat().st_size // 1024} KB (sem target/ e sem .env)")


if __name__ == "__main__":
    main()
