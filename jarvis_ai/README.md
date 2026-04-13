# 🤖 Jarvis AI — IA Pessoal Local

Uma inteligência artificial pessoal rodando **100% localmente** na sua máquina.  
Sem pagar API, sem enviar dados para a nuvem. Seu Jarvis, seu controle.

---

## 📋 Índice

1. [O que é este projeto](#o-que-é-este-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação passo a passo](#instalação-passo-a-passo)
4. [Como rodar o projeto](#como-rodar-o-projeto)
5. [Estrutura de pastas](#estrutura-de-pastas)
6. [Como usar a API](#como-usar-a-api)
7. [Comandos internos do Jarvis](#comandos-internos-do-jarvis)
8. [Como subir no GitHub](#como-subir-no-github)
9. [Roadmap futuro](#roadmap-futuro)
10. [Problemas comuns](#problemas-comuns)

---

## O que é este projeto

O **Jarvis AI** é uma IA pessoal local composta por:

- **FastAPI** — backend e API REST
- **Ollama** — roda modelos de linguagem (LLMs) localmente
- **SQLite** — armazena histórico e memórias
- **Streamlit** — interface web para conversar com a IA

---

## Pré-requisitos

Antes de instalar o projeto, você precisa ter instalado:

### 1. Python 3.11 ou superior

**Windows:**
- Acesse https://python.org/downloads
- Baixe a versão 3.11+
- Na instalação, marque a opção **"Add Python to PATH"**
- Verifique no terminal: `python --version`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip

# Mac (com Homebrew)
brew install python@3.11
```

### 2. Ollama (modelo de IA local)

**Windows e Mac:**
- Acesse https://ollama.com/download
- Baixe e instale o Ollama
- Após instalar, abra o terminal e execute: `ollama --version`

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Git

**Windows:**
- Acesse https://git-scm.com/download/windows
- Baixe e instale com as configurações padrão

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt install git

# Mac
brew install git
```

---

## Instalação passo a passo

### Passo 1 — Clone ou baixe o projeto

Se você já tem o projeto no GitHub:
```bash
git clone https://github.com/SEU_USUARIO/jarvis-ai.git
cd jarvis-ai
```

Se você baixou o zip, extraia e entre na pasta:
```bash
cd jarvis_ai
```

### Passo 2 — Crie o ambiente virtual Python

O ambiente virtual isola as dependências do projeto das demais do seu sistema.

```bash
# Cria o ambiente virtual
python -m venv .venv
```

### Passo 3 — Ative o ambiente virtual

**Windows (Prompt de Comando):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```
> Se der erro no PowerShell, execute antes: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Linux / Mac:**
```bash
source .venv/bin/activate
```

> Se você já usa `venv` em vez de `.venv`, troque `.venv` por `venv` nos comandos acima.

✅ Quando ativado, você verá `(venv)` no início da linha do terminal.

### Passo 4 — Instale as dependências

```bash
pip install -r requirements.txt
```

Aguarde o download e instalação de todos os pacotes (pode levar alguns minutos na primeira vez).

### Passo 5 — Configure as variáveis de ambiente

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

Abra o arquivo `.env` em qualquer editor de texto e ajuste se necessário.  
Para começar, os valores padrão já funcionam.

### Passo 6 — Baixe um modelo de IA local

Abra um **novo terminal** (mantenha o terminal do projeto aberto) e execute:

```bash
# Inicia o servidor do Ollama
ollama serve
```

Em **outro terminal**, baixe o modelo (escolha um):

```bash
# Llama 3 — bom equilíbrio entre qualidade e velocidade (~4.7 GB)
ollama pull llama3

# Mistral — muito bom e mais leve (~4.1 GB)
ollama pull mistral

# Phi-3 Mini — muito rápido, ocupa menos RAM (~2.3 GB)
ollama pull phi3

# Gemma 2B — ultraleve para máquinas com pouca RAM (~1.7 GB)
ollama pull gemma:2b
```

> 💡 **Recomendação:** Se sua máquina tem menos de 8 GB de RAM, use `phi3` ou `gemma:2b`.  
> Se tem 8 GB ou mais, use `llama3` ou `mistral`.

Teste o modelo no terminal:
```bash
ollama run llama3
# Digite qualquer coisa para testar. Pressione Ctrl+D para sair.
```

Se você quiser usar um modelo diferente do `llama3`, edite o arquivo `.env`:
```
OLLAMA_MODEL=mistral
```

---

## Como rodar o projeto

Você precisará de **3 terminais** rodando ao mesmo tempo:

### Terminal 1 — Ollama (modelo de IA)

```bash
ollama serve
```

Deixe este terminal aberto. Você verá: `Listening on 127.0.0.1:11434`

### Terminal 2 — API FastAPI (backend)

```bash
# Ative o ambiente virtual (se ainda não estiver ativo)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Inicia o servidor da API
uvicorn app.main:app --reload --port 8000
```

Você verá:
```
🚀 Iniciando Jarvis AI...
✅ Banco de dados pronto.
📖 Documentação: http://localhost:8000/docs
INFO: Uvicorn running on http://0.0.0.0:8000
```

Abra no navegador: **http://localhost:8000/docs** — você verá a documentação interativa da API.

### Terminal 3 — Interface Web

**Opção A: Streamlit (recomendado)**
```bash
# Ative o ambiente virtual
source .venv/bin/activate   # Linux/Mac
# ou
.venv\Scripts\activate      # Windows

streamlit run interface/streamlit_app.py
```

Acesse: **http://localhost:8501**

### Execução com 1 clique (Windows)

Se você estiver usando Windows, abra o arquivo `run_jarvis.bat` na raiz do projeto (`jarvis_ai`) com duplo clique.
Isso abre duas janelas: uma executando a API FastAPI e outra executando o Streamlit.

> O script detecta automaticamente se o ambiente virtual está em `.venv` ou em `venv`.

No site, use a barra lateral para alternar entre:
- **Chat** — conversa normal com o Jarvis
- **Edição Assistida** — sugestões para cortes, roteiro e edição de vídeo
- **Recomendações** — bibliotecas, recursos e dicas práticas para melhorar seus vídeos

---

## Estrutura de pastas

```
jarvis_ai/
│
├── app/                          # Código principal da API
│   ├── main.py                   # Ponto de entrada do FastAPI
│   ├── api/
│   │   ├── routes_chat.py        # Endpoints de chat (/chat/*)
│   │   ├── routes_memory.py      # Endpoints de memória (/memory/*)
│   │   └── routes_health.py      # Health check (/health, /status)
│   ├── core/
│   │   ├── config.py             # Configurações (lidas do .env)
│   │   ├── database.py           # Configuração SQLite + SQLAlchemy
│   │   └── constants.py          # Constantes e prompt base
│   ├── models/
│   │   ├── chat.py               # Tabelas: conversations, messages
│   │   ├── memory.py             # Tabela: memories
│   │   └── user.py               # Tabela: users
│   ├── schemas/
│   │   ├── chat_schema.py        # Validação de dados do chat
│   │   └── memory_schema.py      # Validação de dados da memória
│   ├── services/
│   │   ├── llm_service.py        # Comunicação com o Ollama
│   │   ├── memory_service.py     # Lógica de memórias
│   │   ├── prompt_service.py     # Monta o contexto/prompt
│   │   └── assistant_service.py  # Orquestrador principal
│   └── utils/
│       └── logger.py             # Sistema de logs
│
├── interface/
│   └── streamlit_app.py          # Interface web (Streamlit)
│
├── data/
│   ├── app.db                    # Banco SQLite (criado automaticamente)
│   ├── uploads/                  # Arquivos enviados pelo usuário
│   └── logs/                     # Logs do sistema
│
├── tests/
│   ├── test_chat.py              # Testes dos endpoints de chat
│   └── test_memory.py            # Testes dos endpoints de memória
│
├── .env                          # Suas configurações (NÃO commitar)
├── .env.example                  # Modelo do .env (commitar este)
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

---

## Como usar a API

Com a API rodando, acesse **http://localhost:8000/docs** para uma interface gráfica de testes.

### Endpoints principais

#### Verificar se está funcionando
```
GET http://localhost:8000/health
```

#### Enviar uma mensagem
```
POST http://localhost:8000/chat/
Content-Type: application/json

{
    "message": "Olá! Quem é você?",
    "conversation_id": null
}
```

Resposta:
```json
{
    "reply": "Olá! Sou o Jarvis, sua inteligência artificial pessoal...",
    "conversation_id": 1,
    "message_id": 1
}
```

#### Continuar a mesma conversa
```json
{
    "message": "Me fale mais sobre você",
    "conversation_id": 1
}
```

#### Salvar uma memória
```
POST http://localhost:8000/memory/
{
    "content": "O usuário se chama João e trabalha com programação",
    "memory_type": "fato",
    "relevance": 1.0
}
```

---

## Comandos internos do Jarvis

Você pode digitar estes comandos diretamente no chat:

| Comando | Descrição |
|---------|-----------|
| `salvar memória: [texto]` | Salva o texto como memória |
| `salve como memória: [texto]` | Igual ao anterior |
| `listar memórias` | Mostra todas as memórias salvas |
| `mostrar memórias` | Igual ao anterior |

Exemplo:
```
Você: salvar memória: Prefiro respostas curtas e objetivas
Jarvis: ✅ Memória salva: "Prefiro respostas curtas e objetivas"
```

---

## Como subir no GitHub

### Passo 1 — Crie uma conta no GitHub

Acesse https://github.com e crie sua conta (gratuita).

### Passo 2 — Configure o Git na sua máquina

Abra o terminal e execute:
```bash
git config --global user.name "Seu Nome Aqui"
git config --global user.email "seuemail@exemplo.com"
```

### Passo 3 — Inicie o repositório Git

Dentro da pasta do projeto:
```bash
# Inicia o Git na pasta
git init

# Verifica os arquivos que serão commitados
# O .env NÃO deve aparecer aqui (está no .gitignore)
git status
```

### Passo 4 — Faça o primeiro commit

```bash
# Adiciona todos os arquivos ao staging
git add .

# Cria o primeiro commit
git commit -m "feat: estrutura inicial do Jarvis AI"
```

### Passo 5 — Crie o repositório no GitHub

1. Acesse https://github.com/new
2. Nome do repositório: `jarvis-ai` (ou outro nome que preferir)
3. Descrição: `IA pessoal local tipo Jarvis — FastAPI + Ollama + SQLite`
4. Deixe como **Público** ou **Privado** (sua escolha)
5. **NÃO** marque "Add a README file" (já temos o nosso)
6. Clique em **"Create repository"**

### Passo 6 — Conecte e envie para o GitHub

Copie os comandos que o GitHub mostrar após criar o repositório. Serão parecidos com:

```bash
# Adiciona o repositório remoto (substitua SEU_USUARIO pelo seu usuário do GitHub)
git remote add origin https://github.com/SEU_USUARIO/jarvis-ai.git

# Define a branch principal
git branch -M main

# Envia o código para o GitHub
git push -u origin main
```

O GitHub pedirá seu usuário e senha (ou token de acesso).

> ⚠️ **Atenção:** O GitHub parou de aceitar senha direta. Você precisa criar um **Personal Access Token**:
> 1. Acesse: https://github.com/settings/tokens
> 2. Clique em "Generate new token (classic)"
> 3. Marque a permissão `repo`
> 4. Copie o token gerado
> 5. Use o token no lugar da senha quando o Git pedir

### Passo 7 — Atualizações futuras

Sempre que fizer mudanças e quiser salvar no GitHub:
```bash
# Veja o que mudou
git status

# Adicione as mudanças
git add .

# Faça o commit com uma mensagem descritiva
git commit -m "feat: adiciona sistema de tarefas"

# Envia para o GitHub
git push
```

### Boas práticas de commit

Use prefixos para organizar seus commits:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudança na documentação
- `refactor:` refatoração de código
- `test:` adição ou melhoria de testes

---

## Como rodar os testes

```bash
# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Roda todos os testes
pytest tests/ -v

# Roda apenas os testes de chat
pytest tests/test_chat.py -v

# Roda apenas os testes de memória
pytest tests/test_memory.py -v
```

---

## Roadmap futuro

- [ ] Sistema de tarefas (criar, concluir, listar)
- [ ] Upload e leitura de arquivos PDF e TXT
- [ ] Busca semântica com embeddings (RAG)
- [ ] Reconhecimento e síntese de voz
- [ ] Automações do computador
- [ ] Migração para PostgreSQL
- [ ] Sistema de múltiplos usuários com login

---

## Problemas comuns

### ❌ "Ollama não está rodando"
**Solução:** Abra um terminal e execute `ollama serve`. Deixe aberto.

### ❌ "ModuleNotFoundError"
**Solução:** O ambiente virtual não está ativo. Execute:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`
> Se estiver usando `venv` em vez de `.venv`, troque `.venv` por `venv`.

### ❌ "Port 8000 already in use"
**Solução:** Outra instância já está rodando. Use outra porta:
```bash
uvicorn app.main:app --reload --port 8001
```

### ❌ "Model not found"
**Solução:** Baixe o modelo antes. Execute: `ollama pull llama3`

### ❌ Resposta muito lenta
**Possíveis causas:**
- Pouca RAM disponível — feche outros programas
- Modelo muito grande — use `phi3` ou `gemma:2b`
- CPU lenta — seja paciente, LLMs locais são pesados

### ❌ Erro ao ativar o venv no PowerShell (Windows)
**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Depois tente ativar novamente.
