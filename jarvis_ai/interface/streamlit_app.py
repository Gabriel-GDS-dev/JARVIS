# ============================================================
# interface/streamlit_app.py
# Interface web do Jarvis usando Streamlit
#
# Como rodar:
#   streamlit run interface/streamlit_app.py
# ============================================================

import streamlit as st
import requests

# ── Configuração da página ───────────────────────────────────
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# URL base da API FastAPI
API_URL = "http://localhost:8000"


# ── CSS customizado ───────────────────────────────────────────

st.markdown(
    """
    <style>
    body, .block-container {
        background: #020617;
        color: #e2e8f0;
    }
    .reportview-container .main .block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .message-card {
        border-radius: 24px;
        padding: 18px 20px;
        margin-bottom: 14px;
        width: fit-content;
        max-width: 72%;
        line-height: 1.7;
        border: 1px solid rgba(148, 163, 184, 0.15);
    }
    .message-user {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: #ffffff;
        margin-left: auto;
    }
    .message-assistant {
        background: #111827;
        color: #e2e8f0;
        margin-right: auto;
    }
    .message-label {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }
    .streamlit-expanderHeader {
        color: #e2e8f0;
    }
    .css-1v0mbdj.egzxvld0 {
        background: #020617;
    }
    .css-1d391kg {
        background: #020617;
    }
    .sidebar .stButton>button {
        background-color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_api_status():
    """Verifica se a API está online."""
    try:
        response = requests.get(f"{API_URL}/status", timeout=3)
        return response.json()
    except Exception:
        return None


def send_message(message: str, conversation_id: int = None): # type: ignore
    """Envia mensagem para a API e retorna a resposta."""
    try:
        response = requests.post(
            f"{API_URL}/chat/",
            json={"message": message, "conversation_id": conversation_id},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ API não está rodando. Execute: uvicorn app.main:app --reload")
        return None
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return None


def get_memories():
    """Busca todas as memórias salvas."""
    try:
        response = requests.get(f"{API_URL}/memory/", timeout=5)
        return response.json()
    except Exception:
        return []


def save_memory(content: str, memory_type: str):
    """Salva uma nova memória via API."""
    try:
        response = requests.post(
            f"{API_URL}/memory/",
            json={"content": content, "memory_type": memory_type, "relevance": 1.0},
            timeout=10,
        )
        return response.status_code == 201
    except Exception:
        return False


def delete_memory(memory_id: int):
    """Deleta uma memória pelo ID."""
    try:
        requests.delete(f"{API_URL}/memory/{memory_id}", timeout=5)
    except Exception:
        pass


def get_conversations():
    """Lista as conversas recentes."""
    try:
        response = requests.get(f"{API_URL}/chat/conversations", timeout=5)
        return response.json()
    except Exception:
        return []


def get_video_editing_recommendations():
    """Retorna uma lista de recomendações úteis para edição de vídeo."""
    return [
        {
            "title": "CapCut",
            "description": "Editor rápido e gratuito para celular, ideal para conteúdo curto e cortado.",
        },
        {
            "title": "DaVinci Resolve",
            "description": "Editor profissional com correção de cor avançada e controle total.",
        },
        {
            "title": "Opusclip",
            "description": "Automatiza cortes e gera clipes virais otimizados para redes sociais.",
        },
        {
            "title": "Mixkit / Pexels / Pixabay",
            "description": "Recursos gratuitos de mídia para enriquecer seus vídeos com imagens e áudio.",
        },
    ]


def get_resource_recommendations():
    """Retorna recomendações de ferramentas e temas para melhorar seus vídeos."""
    return [
        {
            "title": "Estratégia de conteúdo",
            "description": "Faça lives, corte os melhores momentos e publique nos canais certos.",
        },
        {
            "title": "Roteiro direto",
            "description": "Use gancho, desenvolvimento e CTA para manter o público engajado.",
        },
        {
            "title": "Som e ritmo",
            "description": "Escolha trilhas e cortes que acompanhem a emoção do vídeo.",
        },
        {
            "title": "Identidade visual",
            "description": "Padronize estilo, cores e tipografia para sua marca pessoal.",
        },
    ]


def render_message(role: str, content: str):
    """Renderiza uma mensagem com estilo profissional."""
    label = "Você" if role == "user" else "Jarvis"
    css_class = "message-user" if role == "user" else "message-assistant"
    content_html = content.replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="message-card {css_class}">
            <div class="message-label">{label}</div>
            <div>{content_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Estado da sessão ─────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Chat"

if "edit_messages" not in st.session_state:
    st.session_state.edit_messages = []

if "edit_conversation_id" not in st.session_state:
    st.session_state.edit_conversation_id = None

if "memory_refresh" not in st.session_state:
    st.session_state.memory_refresh = 0


def reset_chat():
    st.session_state.messages = []
    st.session_state.conversation_id = None


def reset_edit():
    st.session_state.edit_messages = []
    st.session_state.edit_conversation_id = None


# ── Sidebar ──────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style="padding-bottom: 12px;">
            <h1 style="margin: 0; font-size: 2rem; letter-spacing: -0.03em;">Jarvis AI</h1>
            <p style="margin: 6px 0 0; color: #94a3b8; font-size: 0.95rem;">Assistente local para chat, memórias e edição de vídeo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### Navegação")
    nav_cols = st.columns([1, 1, 1])
    modes = ["Chat", "Edição Assistida", "Recomendações"]
    icons = ["💬", "✂️", "📌"]
    for idx, mode in enumerate(modes):
        if nav_cols[idx].button(f"{icons[idx]} {mode}", key=f"nav_{mode}", use_container_width=True):
            st.session_state.active_tab = mode
            st.experimental_rerun() # pyright: ignore[reportAttributeAccessIssue]

    st.markdown("---")

    st.markdown("### Status do sistema")
    status = check_api_status()
    if status:
        st.success("API: Online")
        if status.get("ollama") == "ok":
            st.success("Ollama: Online")
        else:
            st.error("Ollama: Offline")
            st.warning("Execute `ollama serve`")
        st.markdown(f"**Modelo:** `{status.get('model', 'desconhecido')}`")
    else:
        st.error("API: Offline")
        st.warning("Execute `uvicorn app.main:app --reload`")

    st.markdown("---")

    st.markdown("### Ações rápidas")
    if st.button("Nova conversa", use_container_width=True, key="quick_reset_chat"):
        reset_chat()
        st.experimental_rerun() # type: ignore
    if st.button("Reiniciar edição", use_container_width=True, key="quick_reset_edit"):
        reset_edit()
        st.experimental_rerun() # type: ignore

    st.markdown("---")

    st.markdown("### Conversas recentes")
    conversations = get_conversations()
    if conversations:
        for conv in conversations[:5]:
            title = conv.get("title") or f"Conversa #{conv['id']}"
            if len(title) > 42:
                title = title[:42] + "..."
            if st.button(title, key=f"conv_{conv['id']}", use_container_width=True):
                try:
                    resp = requests.get(f"{API_URL}/chat/conversations/{conv['id']}/messages")
                    data = resp.json()
                    st.session_state.messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in data.get("messages", [])
                    ]
                    st.session_state.conversation_id = conv["id"]
                    st.experimental_rerun() # type: ignore
                except Exception:
                    st.error("Erro ao carregar conversa.")
    else:
        st.info("Nenhuma conversa encontrada.")

    st.markdown("---")

    st.markdown("### Memórias")
    with st.expander("Adicionar memória"):
        mem_content = st.text_area("Conteúdo", placeholder="Ex: Prefiro respostas curtas")
        mem_type = st.selectbox("Tipo", ["fato", "preferencia", "tarefa", "nota"])
        if st.button("Salvar memória", key="save_memory"):
            if mem_content.strip():
                if save_memory(mem_content.strip(), mem_type):
                    st.success("Memória salva com sucesso.")
                    st.session_state.memory_refresh += 1
                else:
                    st.error("Erro ao salvar memória.")
            else:
                st.warning("Digite o conteúdo da memória.")

    memories = get_memories()
    if memories:
        for mem in memories:
            st.write(f"- **[{mem['memory_type']}]** {mem['content']}")
    else:
        st.info("Nenhuma memória salva ainda.")

    st.markdown("---")
    st.caption("Jarvis AI — Local, completo e confiável")


# ── Página principal ─────────────────────────────────────────

st.markdown("# Jarvis AI")
st.markdown("### Assistente local para chat, memórias e edição de vídeo.")
st.markdown("---")

if st.session_state.active_tab == "Chat":
    st.subheader("Chat")
    st.write("Converse com o Jarvis e use comandos de memória como `salvar memória:` e `listar memórias`.")
    if st.session_state.conversation_id:
        st.info(f"Conversa ativa: #{st.session_state.conversation_id}")

    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"])

    user_input = st.chat_input("Digite uma mensagem para o Jarvis...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        result = send_message(user_input, st.session_state.conversation_id) # type: ignore
        if result:
            reply = result["reply"]
            st.session_state.conversation_id = result["conversation_id"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun() # type: ignore

elif st.session_state.active_tab == "Edição Assistida":
    st.subheader("Edição Assistida")
    st.write("Peça ao Jarvis para sugerir melhorias de edição, cortes, ritmo e estilo de vídeo.")
    if st.session_state.edit_conversation_id:
        st.info(f"Sessão de edição ativa: #{st.session_state.edit_conversation_id}")

    for msg in st.session_state.edit_messages:
        render_message(msg["role"], msg["content"])

    edit_request = st.text_area("Descreva o que você quer melhorar no seu vídeo:", height=140)
    if st.button("Enviar pedido de edição"):
        if edit_request.strip():
            st.session_state.edit_messages.append({"role": "user", "content": edit_request})
            result = send_message(edit_request, st.session_state.edit_conversation_id) # type: ignore
            if result:
                st.session_state.edit_conversation_id = result["conversation_id"]
                st.session_state.edit_messages.append({"role": "assistant", "content": result["reply"]})
                st.experimental_rerun() # type: ignore
        else:
            st.warning("Descreva o que você deseja melhorar.")

else:
    st.subheader("Recomendações")
    st.write("Sugestões práticas para bibliotecas, recursos e estratégias de vídeo.")
    left, right = st.columns(2)
    with left:
        st.markdown("### Ferramentas e recursos")
        for item in get_video_editing_recommendations():
            st.markdown(f"**{item['title']}**\n{item['description']}")
    with right:
        st.markdown("### Dicas de estratégia")
        for item in get_resource_recommendations():
            st.markdown(f"**{item['title']}**\n{item['description']}")
