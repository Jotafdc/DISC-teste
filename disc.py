import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
import os

# 1. CONFIGURAÇÃO E ESTILO (CSS)
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

# 2. CABEÇALHO
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    if os.path.exists(caminho_logo): 
        st.image(caminho_logo, width=150)
    st.title("PERFIL DE PERSONALIDADE")
    st.markdown("<p style='text-align:center;'>Responda com sinceridade. Escolha a opção que melhor descreve você.</p>", unsafe_allow_html=True)

# 3. IDENTIFICAÇÃO
with st.container():
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Completo", placeholder="Seu nome...")
    setor = c2.text_input("Setor", placeholder="Seu setor...")

st.markdown("---")

# 4. QUESTÕES - TESTE DISC CLÁSSICO (Opções Embaralhadas)
perguntas = [
    {"id": 1, "texto": "EU ME CONSIDERO UMA PESSOA:", "opcoes": {
        "I": "Extrovertida, comunicativa e animada.",
        "C": "Cuidadosa, detalhista e reflexiva.",
        "S": "Paciente, compreensiva e estável.",
        "D": "Determinada, focada e voltada para a ação."}},
        
    {"id": 2, "texto": "NO DIA A DIA, EU SOU MAIS:", "opcoes": {
        "C": "Lógico, analítico e organizado.",
        "S": "Calmo, constante e ponderado.",
        "D": "Direto, objetivo e apressado.",
        "I": "Entusiasmado, alegre e falante."}},
        
    {"id": 3, "texto": "MINHA MAIOR MOTIVAÇÃO É:", "opcoes": {
        "S": "Ajudar os outros e manter um ambiente seguro e pacífico.",
        "D": "Alcançar resultados, vencer e superar desafios.",
        "I": "Ser reconhecido, interagir e inspirar pessoas.",
        "C": "Fazer o trabalho com perfeição e aprender coisas novas."}},
        
    {"id": 4, "texto": "DIANTE DE UM PROBLEMA INESPERADO, EU COSTUMO:", "opcoes": {
        "D": "Agir rapidamente para resolver a situação.",
        "C": "Analisar todas as informações antes de dar um passo.",
        "I": "Buscar ideias e conversar com outras pessoas.",
        "S": "Tentar manter a harmonia e pedir orientação."}},
        
    {"id": 5, "texto": "A MAIORIA DAS PESSOAS ME VÊ COMO ALGUÉM:", "opcoes": {
        "I": "Carismático, popular e otimista.",
        "C": "Exigente, formal e muito disciplinado.",
        "D": "Forte, corajoso e independente.",
        "S": "Leal, confiável e um bom ouvinte."}},
        
    {"id": 6, "texto": "EU PREFIRO AMBIENTES QUE SEJAM:", "opcoes": {
        "S": "Seguros, amigáveis e tranquilos.",
        "I": "Divertidos, agitados e com muita gente.",
        "C": "Estruturados, silenciosos e bem organizados.",
        "D": "Desafiadores, competitivos e com muita liberdade."}},
        
    {"id": 7, "texto": "QUANDO CONVERSO COM ALGUÉM, EU GERALMENTE:", "opcoes": {
        "C": "Faço perguntas específicas para entender os detalhes lógicos.",
        "D": "Vou direto ao ponto e não gosto de enrolação.",
        "S": "Escuto com muita atenção e faço as pessoas se sentirem bem.",
        "I": "Falo bastante, gesticulo e conto histórias."}},
        
    {"id": 8, "texto": "O QUE ME DEIXA MAIS DESCONFORTÁVEL É:", "opcoes": {
        "I": "Ser rejeitado, ignorado ou ficar isolado.",
        "S": "Passar por mudanças repentinas e sem aviso.",
        "D": "Perder o controle da situação ou falhar publicamente.",
        "C": "Cometer erros ou ser criticado por falta de qualidade."}},
        
    {"id": 9, "texto": "SOB MUITO ESTRESSE, MINHA TENDÊNCIA É FICAR:", "opcoes": {
        "C": "Crítico, rígido e teimoso com as regras.",
        "D": "Impaciente, irritado e autoritário.",
        "I": "Emotivo, desorganizado e falar sem pensar.",
        "S": "Calado, retraído e ceder para evitar brigas."}},
        
    {"id": 10, "texto": "EM UM TRABALHO DE EQUIPE, EU GOSTO DE:", "opcoes": {
        "D": "Liderar, assumir a frente e dar a direção.",
        "S": "Cooperar, apoiar os colegas e fazer a minha parte bem feita.",
        "C": "Planejar as etapas, criar as planilhas e verificar a qualidade.",
        "I": "Motivar, animar o grupo e apresentar o projeto."}},
        
    {"id": 11, "texto": "EU COSTUMO TOMAR DECISÕES BASEADO EM:", "opcoes": {
        "I": "Na minha intuição e no que as pessoas vão achar.",
        "C": "Em fatos, números e dados concretos.",
        "S": "No consenso do grupo e no que for mais seguro.",
        "D": "No que vai trazer o resultado mais rápido."}},
        
    {"id": 12, "texto": "MINHA ATITUDE EM RELAÇÃO A REGRAS É:", "opcoes": {
        "S": "Seguir fielmente para manter a ordem e agradar a liderança.",
        "D": "Questionar se elas forem um obstáculo para o meu objetivo.",
        "I": "Esquecer algumas se elas forem muito burocráticas ou chatas.",
        "C": "Seguir à risca porque elas garantem que o certo será feito."}},
        
    {"id": 13, "texto": "EU ME SINTO REALIZADO QUANDO:", "opcoes": {
        "C": "Termino uma tarefa complexa com um nível de perfeição alto.",
        "I": "Sou o centro das atenções ou recebo muitos elogios.",
        "D": "Supero um grande obstáculo ou venço uma competição.",
        "S": "Sinto que sou útil, valorizado e ajudo minha equipe."}},
        
    {"id": 14, "texto": "MINHA FORMA DE ME EXPRESSAR É:", "opcoes": {
        "I": "Animada, expressiva e informal.",
        "C": "Precisa, cuidadosa e formal.",
        "S": "Suave, ponderada e amável.",
        "D": "Enérgica, afirmativa e rápida."}},
        
    {"id": 15, "texto": "EU VALORIZO MUITO:", "opcoes": {
        "S": "A segurança, a lealdade e a família.",
        "D": "O poder, a eficiência e a velocidade.",
        "C": "A lógica, a precisão e a justiça.",
        "I": "A popularidade, o status e a diversão."}},
        
    {"id": 16, "texto": "QUANDO COMEÇO ALGO NOVO, EU:", "opcoes": {
        "C": "Planejo todas as etapas, prevejo riscos e organizo o material.",
        "S": "Prefiro que me deem um passo a passo claro e apoio.",
        "D": "Quero ver a coisa acontecendo e os resultados logo.",
        "I": "Fico muito empolgado com as possibilidades e ideias."}},
        
    {"id": 17, "texto": "EM UMA DISCUSSÃO, EU GERALMENTE:", "opcoes": {
        "D": "Defendo minha opinião com força e não desisto fácil.",
        "I": "Tento contornar a situação com charme ou mudando de assunto.",
        "C": "Apresento argumentos lógicos e provas de que estou certo.",
        "S": "Evito o conflito a todo custo e prefiro ficar calado."}},
        
    {"id": 18, "texto": "PARA MIM, O SUCESSO É:", "opcoes": {
        "I": "Ter muitos amigos, influência e ser querido por todos.",
        "C": "Ser reconhecido como um especialista e fazer descobertas.",
        "S": "Ter uma vida equilibrada, paz de espírito e boas relações.",
        "D": "Estar no topo, ser o melhor e ter independência."}},
        
    {"id": 19, "texto": "EU ME COMUNICO MELHOR:", "opcoes": {
        "S": "Em conversas individuais, calmas e com empatia.",
        "D": "Dando instruções claras, curtas e diretas.",
        "I": "Falando em público ou contando histórias envolventes.",
        "C": "Através da escrita, e-mails detalhados ou gráficos."}},
        
    {"id": 20, "texto": "MINHA POSTURA CORPORAL NO DIA A DIA É:", "opcoes": {
        "C": "Contida, observadora e com poucas expressões.",
        "I": "Descontraída, com muitos gestos e expressões faciais.",
        "D": "Firme, inquieta e com passos rápidos.",
        "S": "Relaxada, receptiva e sem movimentos bruscos."}},
        
    {"id": 21, "texto": "EU NÃO SUPORTO:", "opcoes": {
        "I": "Ambientes tristes, monótonos e pessoas pessimistas.",
        "C": "Desorganização, trabalho mal feito e erros por falta de atenção.",
        "S": "Agressividade, arrogância e injustiça com os mais fracos.",
        "D": "Pessoas lentas, indecisas ou que dão desculpas."}},
        
    {"id": 22, "texto": "MEU FOCO PRINCIPAL ESTÁ:", "opcoes": {
        "D": "No futuro, nas metas e no que precisa ser conquistado.",
        "S": "No presente, na estabilidade e em manter a rotina funcionando.",
        "I": "No presente, nas pessoas e em aproveitar o momento.",
        "C": "No passado, nos detalhes e em como as coisas sempre foram feitas."}},
        
    {"id": 23, "texto": "QUANDO PRECISO CONVENCER ALGUÉM, EU:", "opcoes": {
        "S": "Mostro que a ideia é segura, não tem riscos e ajuda a todos.",
        "C": "Uso fatos irrefutáveis, lógica e dados concretos.",
        "D": "Mostro assertividade, cobro resultados e pressiono um pouco.",
        "I": "Uso meu carisma, meu entusiasmo e tento inspirar a pessoa."}},
        
    {"id": 24, "texto": "EU PREFIRO TAREFAS QUE:", "opcoes": {
        "C": "Exijam análise, concentração e perfeccionismo.",
        "D": "Tragam resultados imediatos e tenham alto impacto.",
        "S": "Sejam rotineiras, conhecidas e tenham um ritmo constante.",
        "I": "Envolvam interagir com o público ou trabalho criativo."}},
        
    {"id": 25, "texto": "EM RESUMO, EU SOU PRINCIPALMENTE:", "opcoes": {
        "I": "Um comunicador focado em pessoas.",
        "S": "Um parceiro focado em harmonia.",
        "C": "Um pensador focado em qualidade.",
        "D": "Um realizador focado em ação."}}
]

# 5. LAYOUT EM COLUNAS
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

# 6. PROCESSAMENTO E ENVIO
st.write("---")
if st.button("SUBMETER TESTE"):
    if not nome or not setor or None in respostas.values():
        st.error("⚠️ Preencha nome, setor e todas as 25 questões.")
    else:
        scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        for q_id, resp in respostas.items():
            item = next(x for x in perguntas if x["id"] == q_id)
            letra = [k for k, v in item['opcoes'].items() if v == resp][0]
            scores[letra] += 1
        
        pct = {k: f"{round((v/25)*100, 1)}%" for k, v in scores.items()}
        perfil_final = " & ".join([k for k, v in scores.items() if v == max(scores.values())])

        # Exibe Gráfico Visual para o Usuário
        st.balloons()
        st.header(f"Seu Perfil Principal: {perfil_final}")
        
        df_res = pd.DataFrame({
            "Perfil": ["Dominância", "Influência", "Estabilidade", "Conformidade"],
            "Pontos": [scores["D"], scores["I"], scores["S"], scores["C"]]
        })
        fig = px.bar(df_res, x="Perfil", y="Pontos", color="Perfil", text_auto=True,
                     color_discrete_map={"Dominância": "#e74c3c", "Influência": "#f1c40f", "Estabilidade": "#3498db", "Conformidade": "#2ecc71"})
        st.plotly_chart(fig, use_container_width=True)

        # 7. SALVAR NO GOOGLE SHEETS COM SEGURANÇA E ALINHAMENTO
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Lê os dados ao vivo (ignorando o cache antigo)
            df_atual = conn.read(worksheet="Dados", ttl=0)
            
            # Limpa colunas e linhas residuais do Sheets
            df_atual = df_atual.loc[:, ~df_atual.columns.str.contains('^Unnamed')]
            df_atual = df_atual.dropna(subset=["Nome"])
            df_atual = df_atual[df_atual["Nome"].astype(str).str.strip() != ""]
            df_atual = df_atual[df_atual["Nome"].astype(str).str.strip().str.lower() != "nan"]
            
            # Nova linha formatada exatamente como o cabeçalho
            nova_linha = pd.DataFrame([{
                "Nome": nome, "Setor": setor, 
                "D": pct["D"], "I": pct["I"], "S": pct["S"], "C": pct["C"], 
                "Perfil": perfil_final
            }])
            
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            df_final = df_final.fillna("")
            
            # Salva
            conn.update(worksheet="Dados", data=df_final)
            st.success("✅ Resultados enviados com sucesso para o banco de dados da Print Mais!")
            
        except Exception as e:
            st.error("Erro técnico detalhado:")
            st.code(e)