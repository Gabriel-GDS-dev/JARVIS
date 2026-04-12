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


# ── Funções auxiliares ───────────────────────────────────────

def check_api_status():
    """Verifica se a API está online."""
    try:
        response = requests.get(f"{API_URL}/status", timeout=3)
        return response.json()
    except Exception:
        return None


def send_message(message: str, conversation_id: int = None):
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
            "description": "Editor rápido e gratuito para celular, ótimo para cortes curtos e usos em TikTok e Reels.",
        },
        {
            "title": "DaVinci Resolve",
            "description": "Ferramenta poderosa para edição e correção de cor, boa para quem busca qualidade profissional sem custo.",
        },
        {
            "title": "Opusclip",
            "description": "Use para separar automaticamente clipes de vídeos mais longos e gerar cortes para redes sociais.",
        },
        {
            "title": "Shotcut / OpenShot",
            "description": "Alternativas gratuitas para edição de vídeo no desktop quando você precisa de mais controle.",
        },
        {
            "title": "Mixkit / Pexels / Pixabay",
            "description": "Bibliotecas gratuitas de vídeos, músicas e imagens para enriquecer seus conteúdos.",
        },
        {
            "title": "Freesound / Artlist / Epidemic Sound",
            "description": "Recursos de áudio e músicas para deixar seus vídeos mais profissionais. Use o gratuito e teste opções pagas quando precisar de qualidade extra.",
        },
    ]


def get_resource_recommendations():
    """Retorna recomendações de ferramentas e temas para melhorar seus vídeos."""
    return [
        {
            "title": "Estratégia de conteúdo",
            "description": "Faça lives, corte os melhores momentos e publique clipes no TikTok e YouTube Shorts.",
        },
        {
            "title": "Roteiro simples",
            "description": "Defina gancho, desenvolvimento e chamada para ação em vídeos curtos para manter o público até o final.",
        },
        {
            "title": "Atenção ao som",
            "description": "Use música ou efeitos leves para dar ritmo, mas mantenha o foco na narrativa principal.",
        },
        {
            "title": "Identidade visual",
            "description": "Use cores e padrões similares em todos os vídeos para facilitar a identificação do seu conteúdo.",
        },
    ]


# ── Inicializa o estado da sessão ────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "active_section" not in st.session_state:
    st.session_state.active_section = "Chat"

if "edit_messages" not in st.session_state:
    st.session_state.edit_messages = []

if "edit_conversation_id" not in st.session_state:
    st.session_state.edit_conversation_id = None


# ── Sidebar ──────────────────────────────────────────────────

with st.sidebar:
    st.title("🤖 Jarvis AI")
    st.markdown("---")

    st.subheader("📁 Seções")
    st.session_state.active_section = st.radio(
        "Escolha uma área:",
        ["Chat", "Edição Assistida", "Recomendações"],
        index=["Chat", "Edição Assistida", "Recomendações"].index(st.session_state.active_section),
        key="active_section_radio",
    )

    st.markdown("---")

    # Status do sistema
    st.subheader("📡 Status do Sistema")
    status = check_api_status()
    if status:
        st.success(f"API: ✅ Online")
        ollama_status = status.get("ollama", "desconhecido")
        if ollama_status == "ok":
            st.success(f"Ollama: ✅ Online")
            st.info(f"Modelo: `{status.get('model', '?')}`")
        else:
            st.error(f"Ollama: ❌ Offline")
            st.warning("Execute `ollama serve` no terminal")
    else:
        st.error("API: ❌ Offline")
        st.warning("Execute: `uvicorn app.main:app --reload`")

    st.markdown("---")

    # Nova conversa
    st.subheader("💬 Conversa")
    if st.button("🆕 Nova Conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.rerun()

    # Histórico de conversas
    conversations = get_conversations()
    if conversations:
        st.subheader("📜 Conversas Recentes")
        for conv in conversations[:5]:
            title = conv.get("title") or f"Conversa #{conv['id']}"
            if len(title) > 30:
                title = title[:30] + "..."
            if st.button(f"💬 {title}", key=f"conv_{conv['id']}", use_container_width=True):
                st.session_state.conversation_id = conv["id"]
                # Carrega mensagens da conversa selecionada
                try:
                    resp = requests.get(f"{API_URL}/chat/conversations/{conv['id']}/messages")
                    data = resp.json()
                    st.session_state.messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in data.get("messages", [])
                    ]
                    st.rerun()
                except Exception:
                    pass

    st.markdown("---")

    # Memórias
    st.subheader("🧠 Memórias")

    # Adicionar nova memória
    with st.expander("➕ Adicionar Memória"):
        mem_content = st.text_area("Conteúdo:", placeholder="Ex: Prefiro respostas curtas")
        mem_type = st.selectbox("Tipo:", ["fato", "preferencia", "tarefa", "nota"])
        if st.button("Salvar Memória"):
            if mem_content.strip():
                if save_memory(mem_content.strip(), mem_type):
                    st.success("✅ Memória salva!")
                    st.rerun()
                else:
                    st.error("Erro ao salvar memória.")
            else:
                st.warning("Digite o conteúdo da memória.")

    # Lista de memórias
    memories = get_memories()
    if memories:
        for mem in memories:
            with st.expander(f"[{mem['memory_type']}] {mem['content'][:40]}..."):
                st.write(mem["content"])
                st.caption(f"Relevância: {mem['relevance']} | ID: {mem['id']}")
                if st.button("🗑️ Deletar", key=f"del_mem_{mem['id']}"):
                    delete_memory(mem["id"])
                    st.rerun()
    else:
        st.info("Nenhuma memória salva ainda.")

    st.markdown("---")
    st.caption("Jarvis AI v1.0 — Local & Privado")


# ── Área principal ───────────────────────────────────────────

if st.session_state.active_section == "Chat":
    st.title("💬 Converse com o Jarvis")

    conv_label = f"Conversa #{st.session_state.conversation_id}" if st.session_state.conversation_id else "Nova Conversa"
    st.caption(f"🗂️ {conv_label}")

    # Exibe o histórico de mensagens
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Campo de entrada do usuário
    if user_input := st.chat_input("Digite sua mensagem..."):

        # Exibe a mensagem do usuário imediatamente
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Envia para a API e exibe a resposta
        with st.chat_message("assistant"):
            with st.spinner("Jarvis está pensando..."):
                result = send_message(user_input, st.session_state.conversation_id)

            if result:
                reply = result["reply"]
                st.session_state.conversation_id = result["conversation_id"]
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            else:
                st.error("Não foi possível obter uma resposta.")

elif st.session_state.active_section == "Edição Assistida":
    st.title("🛠️ Edição Assistida")
    st.write(
        "Receba sugestões de cortes, ritmo, roteiro e recursos para seus vídeos. "
        "Peça recomendações específicas para CapCut, DaVinci, Opusclip ou seu estilo de conteúdo."
    )
    st.info("As alterações são aplicadas imediatamente na interface. Não é preciso fechar e abrir o site de novo.")

    for msg in st.session_state.edit_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if edit_input := st.chat_input("Descreva o que você quer melhorar no seu vídeo..."):
        st.session_state.edit_messages.append({"role": "user", "content": edit_input})
        with st.chat_message("user"):
            st.markdown(edit_input)

        with st.chat_message("assistant"):
            with st.spinner("Jarvis está analisando seu pedido de edição..."):
                result = send_message(edit_input, st.session_state.edit_conversation_id)

            if result:
                reply = result["reply"]
                st.session_state.edit_conversation_id = result["conversation_id"]
                st.session_state.edit_messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            else:
                st.error("Não foi possível obter uma resposta.")

elif st.session_state.active_section == "Recomendações":
    st.title("📚 Recomendações de Bibliotecas e Recursos")
    st.write(
        "Aqui estão sugestões práticas para tornar seus vídeos mais interessantes, fáceis de editar e melhores para as redes sociais."
    )

    for item in get_video_editing_recommendations():
        st.markdown(f"**{item['title']}** — {item['description']}")

    st.markdown("---")
    st.subheader("Dicas rápidas de conteúdo")
    for item in get_resource_recommendations():
        st.markdown(f"**{item['title']}** — {item['description']}")
