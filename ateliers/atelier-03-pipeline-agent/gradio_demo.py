"""
═══════════════════════════════════════════════════════════════════════════
Atelier 03 — Démo Gradio de l'agent ReAct (avec trace intermédiaire)
═══════════════════════════════════════════════════════════════════════════

Lance une interface Gradio locale (http://127.0.0.1:7860) où l'utilisateur
peut chatter avec l'agent et voir la trace ReAct (Thought→Action→Observation).

Lancer : python ateliers/atelier-03-pipeline-agent/gradio_demo.py
═══════════════════════════════════════════════════════════════════════════
"""

import gradio as gr
from homebutler.agent.react_agent import get_session_agent_debug


# Une instance d'agent (mémoire conversationnelle k=6).
_AGENT = get_session_agent_debug()


def chat(message: str, history: list[tuple[str, str]]) -> tuple[str, str]:
    """Appelle l'agent et retourne (réponse, trace ReAct formatée)."""
    result = _AGENT.invoke({
        "input": message,
        "chat_history": [],
    })
    answer = result.get("output", "")

    # Format de la trace pour affichage utilisateur (debug pédagogique).
    steps = result.get("intermediate_steps", [])
    trace_lines = []
    for i, (action, obs) in enumerate(steps, 1):
        trace_lines.append(
            f"### Step {i}\n"
            f"- **Action**: `{action.tool}`\n"
            f"- **Input**: {str(action.tool_input)[:200]}\n"
            f"- **Observation**: {str(obs)[:300]}"
        )
    trace_md = "\n\n".join(trace_lines) if trace_lines else "_Aucun outil appelé_"
    return answer, trace_md


with gr.Blocks(title="HomeButler — Démo agent ReAct") as demo:
    gr.Markdown("# HomeButler — Démo agent ReAct (atelier 03)\n\nL'agent dispose de 4 outils. Pose une question multi-outils :\n> *Il va faire -5°C demain, comment je prépare ma maison et que puis-je commander à un producteur local ?*")
    with gr.Row():
        with gr.Column(scale=2):
            chatbox = gr.Textbox(label="Question", lines=2, placeholder="Pose une question…")
            send_btn = gr.Button("Envoyer", variant="primary")
            reply = gr.Markdown(label="Réponse finale")
        with gr.Column(scale=3):
            trace = gr.Markdown(label="Trace ReAct (intermediate steps)")

    send_btn.click(fn=chat, inputs=[chatbox, gr.State([])], outputs=[reply, trace])


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
