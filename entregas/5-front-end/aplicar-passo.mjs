#!/usr/bin/env node
// Aplica um passo do PLANO_DE_COMMITS.md no clone do repositório público.
// Copia, de entregas/5-front-end/passos/NN/, exatamente os arquivos que o passo cria ou altera,
// na versão daquele momento do projeto.
//
// Uso (dentro do clone do repositório público, que fica ao lado do workspace):
//   node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 07
//   node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs --listar
// Só usa módulos nativos do Node (funciona no Windows, macOS e Linux).
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync, spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const pastaScript = path.dirname(fileURLToPath(import.meta.url))
const pastaPassos = path.join(pastaScript, 'passos')
const workspace = path.resolve(pastaScript, '..', '..')

function sair(mensagem) {
  console.error(`\nERRO: ${mensagem}\n`)
  process.exit(1)
}

// Lista todos os arquivos de uma pasta (caminhos relativos, com "/")
function listarArquivos(pasta, relativo = '') {
  const arquivos = []
  for (const item of fs.readdirSync(pasta, { withFileTypes: true })) {
    const caminhoRel = relativo ? `${relativo}/${item.name}` : item.name
    if (item.isDirectory()) arquivos.push(...listarArquivos(path.join(pasta, item.name), caminhoRel))
    else arquivos.push(caminhoRel)
  }
  return arquivos.sort()
}

function git(argumentos) {
  return execFileSync('git', argumentos, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()
}

const passosDisponiveis = fs.existsSync(pastaPassos)
  ? fs.readdirSync(pastaPassos).filter((nome) => /^\d{2}$/.test(nome)).sort()
  : []
if (passosDisponiveis.length === 0) sair(`não achei a pasta de passos em ${pastaPassos}.`)

const argumento = process.argv[2]

if (!argumento || argumento === '--ajuda' || argumento === '-h') {
  console.log('Uso: node <caminho>/aplicar-passo.mjs NN   (ex.: 07)')
  console.log('     node <caminho>/aplicar-passo.mjs --listar')
  process.exit(argumento ? 0 : 1)
}

if (argumento === '--listar') {
  for (const passo of passosDisponiveis) {
    const arquivos = listarArquivos(path.join(pastaPassos, passo))
    console.log(`${passo}: ${arquivos.join(', ')}`)
  }
  process.exit(0)
}

// Aceita "7", "07" ou "passo07"
const numero = String(Number(argumento.replace(/\D/g, ''))).padStart(2, '0')
if (!passosDisponiveis.includes(numero)) {
  sair(`o passo "${argumento}" não existe. Passos disponíveis: ${passosDisponiveis[0]} a ${passosDisponiveis.at(-1)}.`)
}

// 1) Precisa estar dentro de um repositório git
let raizRepositorio
try {
  raizRepositorio = path.resolve(git(['rev-parse', '--show-toplevel']))
} catch {
  sair('esta pasta não é um repositório git. Entre na pasta do clone do repositório público (cd zelabairro-frontend) e rode de novo.')
}

// 2) Não pode ser o próprio workspace (o projeto vai para o repositório público)
const workspaceReal = fs.realpathSync(workspace)
const raizReal = fs.realpathSync(raizRepositorio)
if (raizReal === workspaceReal || raizReal.startsWith(workspaceReal + path.sep)) {
  sair('você está dentro do citizentech-gs-workspace. Rode este comando dentro do clone do repositório PÚBLICO.')
}

// 3) Avisa se está numa branch que não é de feature
let branch = ''
try {
  branch = git(['rev-parse', '--abbrev-ref', 'HEAD'])
} catch {
  branch = ''
}
if (branch === 'main' || branch === 'develop') {
  sair(`você está na branch "${branch}". Crie a branch do passo antes: git checkout -b feature/<nome-curto>`)
}

// 4) Copia os arquivos do passo
const origem = path.join(pastaPassos, numero)
const arquivos = listarArquivos(origem)
console.log(`\nPasso ${numero} -> ${raizRepositorio} (branch ${branch || '?'})\n`)

let mexeuNoPackage = false
for (const relativo of arquivos) {
  const destino = path.join(raizRepositorio, ...relativo.split('/'))
  const existia = fs.existsSync(destino)
  fs.mkdirSync(path.dirname(destino), { recursive: true })
  fs.copyFileSync(path.join(origem, ...relativo.split('/')), destino)
  console.log(`  ${existia ? 'alterado' : 'novo    '}  ${relativo}`)
  if (relativo === 'package.json') mexeuNoPackage = true
}

console.log(`\n${arquivos.length} arquivo(s) copiado(s).`)

// 5) Instala as dependências quando o passo mexe no package.json ou quando ainda não há node_modules.
//    "npm ci" instala exatamente o package-lock.json e nunca altera esse arquivo.
if (mexeuNoPackage || !fs.existsSync(path.join(raizRepositorio, 'node_modules'))) {
  console.log('\nInstalando dependências (npm ci)...')
  const resultado = spawnSync('npm', ['ci', '--no-audit', '--no-fund'], {
    cwd: raizRepositorio,
    stdio: 'inherit',
    shell: process.platform === 'win32', // no Windows o npm é um .cmd
  })
  if (resultado.status !== 0) sair('o npm ci falhou. Confira a internet e a versão do Node (node -v) e rode o comando de novo.')
}

// 6) Mostra com qual nome e e-mail o commit vai sair (precisa ser o e-mail da sua conta do GitHub)
let autor = ''
try {
  autor = `${git(['config', 'user.name'])} <${git(['config', 'user.email'])}>`
} catch {
  sair('o git ainda não tem seu nome e e-mail. Rode o bloco "configurar meu usuário" do Passo 0.')
}
console.log(`\nO commit deste passo vai sair como: ${autor}\n`)
