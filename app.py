# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import pandas as pd

# --- Configurações Iniciais ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modelo da OpenAI que você deseja usar
OPENAI_MODEL_ID = "gpt-4o-mini" # Usando o modelo GPT-4o mini

# Inicializar o cliente da API da OpenAI
if not OPENAI_API_KEY:
    st.error("Erro Crítico: A API Key da OpenAI (OPENAI_API_KEY) não foi encontrada no arquivo .env.")
    st.stop()

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"Erro ao inicializar o cliente da API da OpenAI: {e}")
    st.stop()

# --- Funções do Sistema RAG ---
def retrieve_information(query: str, user_profile: str) -> str:
    context = ""
    query_lower = query.lower()
    if "enchente" in query_lower:
        if user_profile == "Vítima":
            context = "Situação de enchente: Procure um local alto e seguro. Evite contato com a água da enchente. Sinalize sua localização para equipes de resgate. Mantenha a calma. Telefones de emergência: Defesa Civil 199, Bombeiros 193."
            if "preso" in query_lower:
                context += " Se estiver preso, não tente atravessar áreas alagadas por conta própria, aguarde o resgate. Se possível, avise sobre sua condição e localização exata."
        elif user_profile == "Morador":
            context = "Alerta de enchente na região: Prepare um kit de emergência (água, comida, medicamentos, lanterna). Desligue a energia elétrica se houver risco de a água atingir sua casa. Mantenha-se informado pelos canais oficiais. Abrigos públicos: Ginásio Municipal, Escola Estadual Central."
        elif user_profile == "Familiar":
            context = "Informações sobre enchentes: Para localizar familiares, entre em contato com a Defesa Civil (199) ou verifique listas em abrigos (Ginásio Municipal, Escola Estadual Central). Evite espalhar boatos, busque informações oficiais."
    elif "incêndio florestal" in query_lower:
        if user_profile == "Vítima":
            context = "Situação de incêndio florestal próximo: Se receber ordem de evacuação, saia imediatamente. Cubra nariz e boca com um pano úmido. Se não puder sair, procure um local aberto e longe da vegetação densa. Ligue para 193 (Bombeiros)."
        elif user_profile == "Morador":
            context = "Alerta de incêndio florestal: Mantenha a vegetação ao redor da casa limpa. Tenha rotas de fuga planejadas. Se avistar fumaça ou focos de incêndio, ligue para 193. Não faça queimadas."
        elif user_profile == "Familiar":
            context = "Busca de informações sobre incêndio: Contate autoridades locais para status da situação e informações sobre áreas afetadas. Verifique notícias de fontes confiáveis."
    else:
        context = "Informações gerais sobre segurança em desastres: Mantenha um kit de emergência, tenha um plano familiar, mantenha-se informado por fontes oficiais e siga as orientações das autoridades."
    return context

def generate_augmented_response(user_query: str, retrieved_context: str, user_profile: str) -> str:
    system_prompt = f"""Você é um assistente virtual especializado em orientar pessoas durante desastres naturais.
    Sua missão é fornecer informações claras, precisas, empáticas e acionáveis.
    Você DEVE usar as "Informações Relevantes Recuperadas" para basear sua resposta.
    NÃO invente informações que não foram recuperadas, especialmente números de telefone, endereços específicos ou detalhes factuais não fornecidos no contexto.
    Se as informações recuperadas não forem totalmente suficientes, você pode complementar com conselhos gerais de segurança relevantes para o contexto do desastre mencionado e o perfil do usuário, mas sempre indique claramente quando uma informação é um conselho geral e não parte dos dados recuperados.
    Se a consulta for vaga, peça mais detalhes de forma gentil para poder ajudar melhor.
    Responda diretamente à pergunta do usuário.
    Priorize a segurança e o bem-estar. Seja empático, calmo e direto.
    O perfil do usuário atual é: {user_profile}"""

    user_content_prompt = f"""
    **Consulta do Usuário:**
    "{user_query}"

    **Informações Relevantes Recuperadas (use estas informações para basear sua resposta):**
    "{retrieved_context}"

    Com base no seu papel, no perfil do usuário, na consulta e nas informações recuperadas, forneça a orientação adequada:
    """

    print("\n--- CONSOLE DEBUG: INÍCIO DE generate_augmented_response (OpenAI) ---")
    print(f"CONSOLE DEBUG: Timestamp: {pd.Timestamp.now()}")
    print(f"CONSOLE DEBUG: Usando OPENAI_MODEL_ID: {OPENAI_MODEL_ID}")
    print(f"CONSOLE DEBUG: Comprimento System Prompt: {len(system_prompt)}, User Prompt: {len(user_content_prompt)}")
    print("---------------------------------------------------------")

    try:
        print(f"CONSOLE DEBUG: {pd.Timestamp.now()} - Tentando chamar OpenAI API com modelo de CHAT...")
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content_prompt}
            ],
            max_tokens=800, 
            temperature=0.4, 
            top_p=1.0,
        )
        full_response = response.choices[0].message.content.strip()
        
        print(f"CONSOLE DEBUG: {pd.Timestamp.now()} - Chamada à API OpenAI (Chat) retornou.")
        print(f"CONSOLE DEBUG: {pd.Timestamp.now()} - Resposta bruta do modelo (primeiros 300 chars): '{full_response[:300]}...'")
        print(f"CONSOLE DEBUG: {pd.Timestamp.now()} - Comprimento total da resposta bruta: {len(full_response)}")
        if response.usage:
            print(f"CONSOLE DEBUG: Uso de tokens: {response.usage}")
        print("--- CONSOLE DEBUG: FIM DE generate_augmented_response (SUCESSO OpenAI) ---\n")
        return full_response

    except Exception as e:
        st.error("!!!!!!!!!! OCORREU UMA EXCEÇÃO AO CHAMAR A API DA OPENAI (DETALHES NA UI ABAIXO) !!!!!!!!!!!")
        error_type_name = type(e).__name__
        st.error(f"Tipo da Exceção: {error_type_name}")
        st.error(f"Mensagem da Exceção: {str(e)}")

        print("\n!!!!!!!!!! OCORREU UMA EXCEÇÃO AO CHAMAR A API DA OPENAI (CONSOLE LOG) !!!!!!!!!!!")
        print(f"CONSOLE DEBUG: Timestamp da Exceção: {pd.Timestamp.now()}")
        print(f"Tipo da Exceção: {error_type_name}")
        print(f"Mensagem da Exceção: {str(e)}")

        if hasattr(e, 'http_status'):
            st.error(f"HTTP Status: {e.http_status}")
            print(f"HTTP Status: {e.http_status}")
        if hasattr(e, 'code'):
            st.error(f"OpenAI Error Code: {e.code}")
            print(f"OpenAI Error Code: {e.code}")
        if hasattr(e, 'param'):
            st.error(f"Error Param: {e.param}")
            print(f"Error Param: {e.param}")
        if hasattr(e, 'body'):
            st.error(f"Error Body: {e.body}") # Tentar mostrar o corpo do erro bruto
            print(f"Error Body: {e.body}")
        elif hasattr(e, 'json_body'): # Se o corpo for JSON
             st.error(f"Error JSON Body: {json.dumps(e.json_body, indent=2)}")
             print(f"Error JSON Body: {json.dumps(e.json_body, indent=2)}")
        
        print("--- CONSOLE DEBUG: FIM DE generate_augmented_response (EXCEÇÃO OpenAI) ---\n")
        return "Desculpe, ocorreu um problema ao tentar gerar sua resposta com a OpenAI. Verifique a interface e o console para mais detalhes sobre o erro."

# --- Interface Streamlit ---
st.set_page_config(page_title="Assistente de Desastres", layout="wide")

st.title("🆘 Assistente Virtual para Desastres Naturais")
st.caption(f"Utilizando o modelo: {OPENAI_MODEL_ID} (via OpenAI API)")

st.sidebar.header("👤 Perfil do Usuário")
user_profile_options = ["Vítima", "Morador", "Familiar"]
selected_profile = st.sidebar.selectbox(
    "Selecione seu perfil para receber orientação adequada:",
    user_profile_options,
    index=0 
)

st.info(
    f"**Você está interagindo como: {selected_profile}**\n"
    "A orientação será adaptada a este perfil."
)

user_query = st.text_area("❓ Descreva sua situação ou dúvida:", height=150, placeholder="Ex: Estou em uma área de enchente e a água está subindo. O que faço?")

if st.button("Enviar Pergunta e Obter Orientação", type="primary", use_container_width=True):
    if not user_query:
        st.warning("Por favor, digite sua pergunta para que eu possa ajudar.")
    else:
        with st.spinner("Processando sua solicitação... Buscando informações e gerando orientação..."):
            st.subheader("Contexto Recuperado (Informações de Apoio):")
            with st.expander("Clique para ver os dados recuperados (simulado)", expanded=False):
                st.write(f"DEBUG UI: Buscando informações para: '{user_query}' (Perfil: {selected_profile})...")
                retrieved_info = retrieve_information(user_query, selected_profile)
                if retrieved_info:
                    st.markdown(f"```\n{retrieved_info}\n```")
                    st.write(f"DEBUG UI: Contexto recuperado: {retrieved_info}")
                else:
                    st.caption("Nenhum contexto específico foi recuperado para esta consulta.")

            st.subheader("💡 Orientação do Assistente:")
            final_response = generate_augmented_response(user_query, retrieved_info, selected_profile)
            st.markdown(final_response)

st.sidebar.markdown("---")
st.sidebar.warning(
    "**Atenção:** Este é um assistente virtual para demonstração e apoio.\n\n"
    "Em situações reais de emergência, **sempre siga as orientações das autoridades locais** "
    "e contate os serviços de emergência (Bombeiros: 193, Defesa Civil: 199, SAMU: 192)."
)