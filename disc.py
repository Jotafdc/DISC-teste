import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
import os

# CONFIGURAÇÃO E ESTILO (CSS)
st.set_page_config(page_title="DISC Print Mais", layout="wide", page_icon="📊")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_atual, "image_7d6f47.png")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b1c24, #1a2a40, #2d1b33);
        background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px), linear-gradient(135deg, #0b1c24, #1a2a40, #2d1b33);
        background-size: 40px 40px, 100% 100%;
        color: white !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 210, 255, 0.4); margin-bottom: 15px;
    }
    .stRadio > label, h1, h2, h3, p, label { color: #ffffff !important; font-weight: bold !important; }
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white !important;
        font-weight: bold; width: 100%; border-radius: 8px; height: 3.5em; font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# CABEÇALHO
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    if os.path.exists(caminho_logo): 
        st.image(caminho_logo, width=150)
    st.title("PERFIL DE PERSONALIDADE")

# IDENTIFICAÇÃO
with st.container():
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Completo", placeholder="Seu nome...")
    setor = c2.text_input("Setor", placeholder="Seu setor...")

st.markdown("---")

# QUESTÕES (D, I, S, C)
perguntas = [
    {"id": 1, "texto": "EU SOU:", "opcoes": {"I": "Idealista, criativo e visionário.", "S": "Divertido, espiritual e benéfico.", "C": "Confiável, minucioso e previsível.", "D": "Focado, determinado e persistente."}},
    {"id": 2, "texto": "EU GOSTO DE:", "opcoes": {"D": "Ser piloto.", "S": "Conversar com os passageiros.", "C": "Planejar a viagem.", "I": "Explorar novas rotas."}},
    {"id": 3, "texto": "QUEM QUISER SE DAR BEM COMIGO:", "opcoes": {"I": "Me dê liberdade.", "C": "Me deixe saber suas expectativas.", "D": "Lidere, siga ou saia do caminho.", "S": "Seja amigável, carinhoso e compreensivo."}},
    {"id": 4, "texto": "PARA BONS RESULTADOS É PRECISO:", "opcoes": {"I": "Ter incertezas.", "C": "Controlar o essencial.", "S": "Diversão e celebração.", "D": "Planejar e obter resultados."}},
    {"id": 5, "texto": "EU ME DIVIRTO QUANDO:", "opcoes": {"D": "Estou me exercitando.", "I": "Tenho novidades.", "S": "Estou com os outros.", "C": "Determino as regras."}},
    {"id": 6, "texto": "EU PENSO QUE:", "opcoes": {"S": "Unidos venceremos, divididos perderemos.", "D": "O ataque é melhor que a defesa.", "I": "É bom ser manso, mas tenha um porrete.", "C": "Um homem prevenido vale por dois."}},
    {"id": 7, "texto": "MINHA PREOCUPAÇÃO É:", "opcoes": {"I": "Gerar a ideia global.", "S": "Fazer com que as pessoas gostem.", "C": "Fazer com que funcione.", "D": "Fazer a tarefa."}},
    {"id": 8, "texto": "EU PREFIRO:", "opcoes": {"I": "Perguntar do que responder.", "C": "Ter todos os detalhes.", "D": "Ter vantagens ao meu favor.", "S": "Que todos tenham a chance de ser ouvido."}},
    {"id": 9, "texto": "EU GOSTO DE:", "opcoes": {"D": "Fazer progresso.", "S": "Construir memórias.", "C": "Fazer sentido.", "I": "Tornar as pessoas confortáveis."}},
    {"id": 10, "texto": "EU GOSTO DE CHEGAR:", "opcoes": {"D": "Na frente.", "S": "Junto.", "C": "Na hora.", "I": "Em outro lugar."}},
    {"id": 11, "texto": "UM ÓTIMO DIA PRA MIM É:", "opcoes": {"D": "Consigo fazer muitas coisas.", "S": "Me divirto com meus amigos.", "C": "Tudo segue conforme o planejado.", "I": "Desfruto de coisas novas e estimulantes."}},
    {"id": 12, "texto": "EU VEJO A MORTE COMO:", "opcoes": {"I": "Uma grande aventura misteriosa.", "S": "Oportunidade para rever pessoas queridas.", "C": "Um modo de receber recompensas.", "D": "Algo que sempre chega muito cedo."}},
    {"id": 13, "texto": "MINHA FILOSOFIA DE VIDA É:", "opcoes": {"D": "Sou um ganhador, mas há perdedores.", "S": "Para ganhar, ninguém precisa perder.", "C": "Para ganhar é preciso seguir as regras.", "I": "Para ganhar é necessário inventar novas regras."}},
    {"id": 14, "texto": "EU SEMPRE GOSTEI DE:", "opcoes": {"I": "Explorar novas ideias.", "C": "Evitar surpresas.", "D": "Focalizar na meta.", "S": "Realizar uma abordagem natural."}},
    {"id": 15, "texto": "EU GOSTO DE MUDANÇAS SE:", "opcoes": {"D": "Me der uma vantagem competitiva.", "S": "For divertido e puder ser compartilhado.", "I": "Me der mais liberdade e variedade.", "C": "Melhorar ou me der mais controle."}},
    {"id": 16, "texto": "NÃO EXISTE NADA ERRADO EM:", "opcoes": {"D": "Se colocar na frente.", "S": "Colocar os outros na frente.", "I": "Mudar de ideia.", "C": "Ser consistente."}},
    {"id": 17, "texto": "BUSCO CONSELHOS EM:", "opcoes": {"D": "Pessoas bem sucedidas.", "S": "Anciãos e conselheiros.", "C": "Autoridades no assunto.", "I": "Outros lugares, os mais estranhos."}},
    {"id": 18, "texto": "MEU LEMA É:", "opcoes": {"I": "Fazer o que precisa ser feito.", "C": "Fazer bem feito.", "S": "Fazer junto com o grupo.", "D": "Simplesmente fazer."}},
    {"id": 19, "texto": "EU GOSTO DE:", "opcoes": {"I": "Complexidade, mesmo se confuso.", "C": "Ordem e sistematização.", "S": "Calor humano e animação.", "D": "Coisas claras e simples."}},
    {"id": 20, "texto": "TEMPO PARA MIM É:", "opcoes": {"D": "Algo que detesto desperdiçar.", "S": "Um grande período.", "C": "Uma flecha que leva ao inevitável.", "I": "Irrelevante."}},
    {"id": 21, "texto": "SE EU FOSSE BILIONÁRIO:", "opcoes": {"S": "Faria doações para muitas entidades.", "C": "Criaria uma poupança avantajada.", "I": "Faria o que desse na cabeça.", "D": "Exibiria bastante com algumas pessoas."}},
    {"id": 22, "texto": "EU ACREDITO QUE:", "opcoes": {"D": "O destino é mais importante que a caminhada.", "S": "A caminhada é mais importante que o destino.", "C": "Um centavo economizado é um centavo ganho.", "I": "Bastam um navio e uma estrela para navegar."}},
    {"id": 23, "texto": "EU ACREDITO AINDA QUE:", "opcoes": {"D": "Aquele que hesita está perdido.", "C": "De grão em grão a galinha enche o papo.", "S": "E o que vai, volta.", "I": "O cego não diferencia o sorriso nem careta."}},
    {"id": 24, "texto": "EU ACREDITO AINDA QUE:", "opcoes": {"C": "É melhor prudência do que arrependimento.", "I": "A autoridade deve ser desafiada.", "D": "Ganhar é fundamental.", "S": "O coletivo é mais importante que o individual."}},
    {"id": 25, "texto": "EU PENSO QUE:", "opcoes": {"I": "Não é fácil ficar encurralado.", "C": "É preferível olhar, antes de pular.", "S": "Duas cabeças pensam melhor do que uma.", "D": "Se não sabe competir, fique em casa."}},
]

# LAYOUT COLUNAS
respostas = {}
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 PARTE I")
    for p in perguntas[0:8]: respostas[p['id']] = st.radio(f"**{p['id']} - {p['texto']}**", options=list(p['opcoes'].values()), index=None, key=f"q{p['id']}")
with col2:
    st.subheader("📍 PARTE II")
    for p in perguntas[8:16]: respostas[p['id']] = st.radio(f"**{p['id']} - {p['texto']}**", options=list(p['opcoes'].values()), index=None, key=f"q{p['id']}")
with col3:
    st.subheader("📍 PARTE III")
    for p in perguntas[16:25]: respostas[p['id']] = st.radio(f"**{p['id']} - {p['texto']}**", options=list(p['opcoes'].values()), index=None, key=f"q{p['id']}")

# PROCESSAMENTO E ENVIO
st.write("---")
if st.button("SUBMETER TESTE"):
    if not nome or not setor or None in respostas.values():
        st.error("⚠️ Preencha nome, setor e todas as questões.")
    else:
        scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        for q_id, resp in respostas.items():
            item = next(x for x in perguntas if x["id"] == q_id)
            letra = [k for k, v in item['opcoes'].items() if v == resp][0]
            scores[letra] += 1
        
        pct = {k: f"{round((v/25)*100, 1)}%" for k, v in scores.items()}
        perfil_final = " & ".join([k for k, v in scores.items() if v == max(scores.values())])

        st.balloons()
        st.header(f"Resultado: {perfil_final}")

        try:
            # Conecta na planilha
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # 1. Lê a aba 'Dados'
            df_atual = conn.read(worksheet="Dados")
            
            # 2. O SEGREDO ESTÁ AQUI: Limpa as linhas vazias que causam o erro 400
            df_atual = df_atual.dropna(how="all")
            
            # 3. Cria a nova linha
            nova_linha = pd.DataFrame([{
                "Nome": nome, 
                "Setor": setor, 
                "D": pct["D"], 
                "I": pct["I"], 
                "S": pct["S"], 
                "C": pct["C"], 
                "Perfil": perfil_final
            }])
            
            # 4. Junta os dados antigos com o novo
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            
            # 5. Preenche qualquer NaN residual com texto vazio (proteção extra)
            df_final = df_final.fillna("")
            
            # 6. Envia de volta para o Google Sheets
            conn.update(worksheet="Dados", data=df_final)
            
            st.success("✅ Salvo com sucesso no banco de dados da Print Mais!")
            st.balloons()
            
        except Exception as e:
            st.error("Erro técnico detalhado:")
            st.code(e)