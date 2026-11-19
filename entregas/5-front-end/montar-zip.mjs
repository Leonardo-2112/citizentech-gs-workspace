#!/usr/bin/env node
// Monta o .zip da entrega de Front-End sem node_modules, dist, .git e .env.
// Uso (dentro do clone do repositório público):
//   node ../citizentech-gs-workspace/entregas/5-front-end/montar-zip.mjs
// ou indicando a pasta do projeto:
//   node montar-zip.mjs caminho/do/projeto [caminho/do/arquivo.zip]
// Só usa módulos nativos do Node (funciona no Windows, macOS e Linux).
import fs from 'node:fs'
import path from 'node:path'
import zlib from 'node:zlib'

const LIMITE_MB = 50
const IGNORAR_PASTAS = new Set(['node_modules', 'dist', '.git', '.vercel', '.idea', '.vscode'])
const IGNORAR_ARQUIVOS = [/^\.env$/, /^\.env\..*local$/, /\.zip$/i, /\.log$/i, /^\.DS_Store$/, /\.tsbuildinfo$/]

const origem = path.resolve(process.argv[2] ?? process.cwd())
const destino = path.resolve(process.argv[3] ?? path.join(path.dirname(origem), 'ZelaBairro_Front_1TDSPV.zip'))
const pastaRaiz = 'zelabairro-frontend' // nome da pasta dentro do zip

if (!fs.existsSync(path.join(origem, 'package.json'))) {
  console.error(`Não achei package.json em ${origem}. Rode dentro da pasta do projeto ou passe o caminho.`)
  process.exit(1)
}
for (const obrigatorio of ['README.md', 'identificacao.txt', 'index.html', 'src']) {
  if (!fs.existsSync(path.join(origem, obrigatorio))) {
    console.error(`Falta "${obrigatorio}" no projeto: a entrega ficaria incompleta.`)
    process.exit(1)
  }
}

// Lista os arquivos que vão para o zip
function listar(pasta, relativo = '') {
  const arquivos = []
  for (const item of fs.readdirSync(pasta, { withFileTypes: true })) {
    const caminhoRel = relativo ? `${relativo}/${item.name}` : item.name
    if (item.isDirectory()) {
      if (!IGNORAR_PASTAS.has(item.name)) arquivos.push(...listar(path.join(pasta, item.name), caminhoRel))
    } else if (item.isFile() && !IGNORAR_ARQUIVOS.some((padrao) => padrao.test(item.name))) {
      arquivos.push(caminhoRel)
    }
  }
  return arquivos
}

// CRC-32 (exigido pelo formato zip)
const tabelaCrc = Array.from({ length: 256 }, (_, n) => {
  let c = n
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
  return c >>> 0
})
function crc32(buffer) {
  let crc = 0xffffffff
  for (const byte of buffer) crc = tabelaCrc[(crc ^ byte) & 0xff] ^ (crc >>> 8)
  return (crc ^ 0xffffffff) >>> 0
}

// Data no formato do DOS, usado pelo zip
function dataDos(data) {
  const hora = (data.getHours() << 11) | (data.getMinutes() << 5) | Math.floor(data.getSeconds() / 2)
  const dia = ((data.getFullYear() - 1980) << 9) | ((data.getMonth() + 1) << 5) | data.getDate()
  return { hora, dia }
}

const arquivos = listar(origem).sort()
const partes = []
const central = []
let deslocamento = 0

for (const relativo of arquivos) {
  const conteudo = fs.readFileSync(path.join(origem, relativo))
  const comprimido = zlib.deflateRawSync(conteudo, { level: 9 })
  const usarDeflate = comprimido.length < conteudo.length
  const dados = usarDeflate ? comprimido : conteudo
  const nome = Buffer.from(`${pastaRaiz}/${relativo}`, 'utf8')
  const crc = crc32(conteudo)
  const { hora, dia } = dataDos(fs.statSync(path.join(origem, relativo)).mtime)

  const local = Buffer.alloc(30)
  local.writeUInt32LE(0x04034b50, 0)
  local.writeUInt16LE(20, 4)
  local.writeUInt16LE(0x0800, 6) // nomes em UTF-8
  local.writeUInt16LE(usarDeflate ? 8 : 0, 8)
  local.writeUInt16LE(hora, 10)
  local.writeUInt16LE(dia, 12)
  local.writeUInt32LE(crc, 14)
  local.writeUInt32LE(dados.length, 18)
  local.writeUInt32LE(conteudo.length, 22)
  local.writeUInt16LE(nome.length, 26)
  partes.push(local, nome, dados)

  const registro = Buffer.alloc(46)
  registro.writeUInt32LE(0x02014b50, 0)
  registro.writeUInt16LE(20, 4)
  registro.writeUInt16LE(20, 6)
  registro.writeUInt16LE(0x0800, 8)
  registro.writeUInt16LE(usarDeflate ? 8 : 0, 10)
  registro.writeUInt16LE(hora, 12)
  registro.writeUInt16LE(dia, 14)
  registro.writeUInt32LE(crc, 16)
  registro.writeUInt32LE(dados.length, 20)
  registro.writeUInt32LE(conteudo.length, 24)
  registro.writeUInt16LE(nome.length, 28)
  registro.writeUInt32LE(deslocamento, 42)
  central.push(registro, nome)

  deslocamento += local.length + nome.length + dados.length
}

const tamanhoCentral = central.reduce((soma, parte) => soma + parte.length, 0)
const fim = Buffer.alloc(22)
fim.writeUInt32LE(0x06054b50, 0)
fim.writeUInt16LE(arquivos.length, 8)
fim.writeUInt16LE(arquivos.length, 10)
fim.writeUInt32LE(tamanhoCentral, 12)
fim.writeUInt32LE(deslocamento, 16)

fs.writeFileSync(destino, Buffer.concat([...partes, ...central, fim]))
const tamanhoMb = fs.statSync(destino).size / (1024 * 1024)

console.log(`Zip criado: ${destino}`)
console.log(`${arquivos.length} arquivos, ${tamanhoMb.toFixed(2)} MB (limite ${LIMITE_MB} MB)`)
console.log('Fora do zip: node_modules, dist, .git e .env')
if (tamanhoMb > LIMITE_MB) {
  console.error('ATENÇÃO: passou de 50 MB (penalidade de -2). Remova imagens ou vídeos grandes.')
  process.exit(1)
}
