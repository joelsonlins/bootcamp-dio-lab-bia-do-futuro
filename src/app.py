import json
import pandas as pd
import requests
import streamlit as st

# ========== CONFIGURAÇÃO ===========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b-cloud"

# ============ CARREGAR DADOS ============
perfil = json.load(open('.data/perfil_investidor.json'))
transacoes = pd.read_csv('.data/transacoes.csv')
historico = pd.read_csv('.data/historico_atendimento.csv')
produtos = json.load(open('.data/produtos_financeiros.json'))

# ============ NONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ========= SYSTEM PROMPT =========
SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
1. NUNCA recomende investimentos específicos - apenas explique como funciona;
2. JAMAIS responda a perguntas fora do tema de ensino de finanças pessoais. Quando ocorrer, responda lembrando seu papel de educador financeiro;
3. Use os dados fornecidos para dar exemplos personalizados;
4. Linguagem simples, como se explicasse para um amigo;
5. Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
6. Sempre pergunte se o cliente entendeu;
7. Responda de forma simples e direta, no máximo uns 3 parágrafos.
8. Quando ocorrer, responda lembrando o seu papel de educador financeiro;
"""

# ========= CHAMAR OLLAMA =========
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}
    
    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL,  json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ========== INTERFACE ===========
st.title("Edu, seu educador de finanças")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
