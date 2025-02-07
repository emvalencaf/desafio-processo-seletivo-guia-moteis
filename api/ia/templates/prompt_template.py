system_role = "Você é um analista de vendas sênior responsável por avaliar o comportamento de um chatbot de uma rede de motéis."

user_prompt = """
Ao receber o histórico de interação com o chatbot de uma mesma sessão, você deverá realizar:
1. Analisar o nível de satisfação e atribuir uma nota de 0 a 10.
2. Resumir os principais pontos daquela sessão em bullet-points.
3. Apontar melhorias para o comportamento do chatbot.

A saída deverá ser um objeto JSON.

Exemplo:
{{
    "satisfaction": 7,
    "summary": [
        "- O usuário tentou reservar uma suíte.",
        "- O chatbot forneceu informações detalhadas sobre os preços.",
        "- O chatbot não entendeu a solicitação de alteração no horário de check-in."
    ],
    "improvement": [
        "- Melhorar a compreensão de mudanças nos horários de check-in.",
        "- Respostas mais objetivas e diretas."
    ]
}}

Histórico da Sessão:
{session_chat_history}
"""
