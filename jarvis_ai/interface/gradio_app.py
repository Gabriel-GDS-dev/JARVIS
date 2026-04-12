# ============================================================
# interface/gradio_app.py
# Interface web alternativa usando Gradio (mais simples e rápida)
#
# Como rodar:
#   python interface/gradio_app.py
# ============================================================

import requests
import gradio as gr

API_URL = "http://localhost:8000"


def chat(message: str, history: list, conversation_id_state: int):
    """
    Função chamada pelo Gradio a cada mensagem.
    Envia a mensagem para a API e retorna a resposta.
    """
    if not message.strip():
        return "", history, conversation_id_state

    try:
        response = requests.post(
            f"{API_URL}/chat/",
            json={"message": message, "conversation_id": conversation_id_state},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        reply = data["reply"]
        new_conv_id = data["conversation_id"]
        history.append((message, reply))
        return "", history, new_conv_id

    except requests.exceptions.ConnectionError:
        history.append((message, "❌ API não está rodando. Execute: uvicorn app.main:app --reload"))
        return "", history, conversation_id_state
    except Exception as e:
        history.append((message, f"❌ Erro: {str(e)}"))
        return "", history, conversation_id_state


def new_conversation():
    """Reinicia a conversa."""
    return [], None


def get_status():
    """Verifica o status do sistema."""
    try:
        resp = requests.get(f"{API_URL}/status", timeout=3)
        data = resp.json()
        api_ok = "✅ Online"
        ollama_ok = "✅ Online" if data.get("ollama") == "ok" else "❌ Offline — execute: ollama serve"
        model = data.get("model", "?")
        return f"**API:** {api_ok} | **Ollama:** {ollama_ok} | **Modelo:** `{model}`"
    except Exception:
        return "❌ **API Offline** — execute: `uvicorn app.main:app --reload`"


# ── Interface Gradio ─────────────────────────────────────────

with gr.Blocks(title="Jarvis AI", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🤖 Jarvis AI\nSua inteligência artificial pessoal local")

    # Estado interno (não visível)
    conversation_id_state = gr.State(value=None)

    with gr.Row():
        # Coluna do chat
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversa",
                height=500,
                show_copy_button=True,
            )
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Digite sua mensagem e pressione Enter...",
                    show_label=False,
                    scale=5,
                )
                send_btn = gr.Button("Enviar", variant="primary", scale=1)

            new_btn = gr.Button("🆕 Nova Conversa", variant="secondary")

        # Coluna de status
        with gr.Column(scale=1):
            gr.Markdown("### 📡 Status")
            status_btn = gr.Button("🔄 Verificar Status")
            status_output = gr.Markdown(value="Clique para verificar")

            gr.Markdown("### ℹ️ Comandos úteis")
            gr.Markdown("""
**Você pode dizer:**
- `salvar memória: [texto]`
- `listar memórias`
- `mostrar memórias`

**Iniciar a API:**
```
uvicorn app.main:app --reload
```

**Iniciar o Ollama:**
```
ollama serve
```
            """)

    # Eventos
    msg_input.submit(
        chat,
        inputs=[msg_input, chatbot, conversation_id_state],
        outputs=[msg_input, chatbot, conversation_id_state],
    )
    send_btn.click(
        chat,
        inputs=[msg_input, chatbot, conversation_id_state],
        outputs=[msg_input, chatbot, conversation_id_state],
    )
    new_btn.click(
        new_conversation,
        outputs=[chatbot, conversation_id_state],
    )
    status_btn.click(
        get_status,
        outputs=status_output,
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,   # True = gera link público temporário (útil para testes)
        show_api=False,
    )
