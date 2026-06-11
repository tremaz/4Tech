import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from pathlib import Path

import theme
from metrics import (
    processar_excel,
    calcular_metrics_gupy,
    calcular_metrics_supplygo,
    detectar_fonte,
)

st.set_page_config(
    page_title="Safra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html {
        scroll-behavior: smooth;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global font */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 0;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #334155;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a;
    }
    .sidebar-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    .sidebar-subtitle {
        font-size: 0.9rem;
        font-style: italic;
        color: #94a3b8;
        text-align: center;
        margin-top: 0;
        padding-top: 0;
        margin-bottom: 1.5rem;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: none;
        color: #000000;
        text-align: left;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 400;
        transition: all 0.2s;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 0, 0, 0.05);
        color: #000000;
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: rgba(0, 0, 0, 0.08);
        border-left: 3px solid #3b82f6;
        color: #000000;
        font-weight: 600;
    }
    
    /* Main content background */
    .main .block-container {
        background: #ffffff;
        padding: 32px;
    }
    
    /* Metric cards */
    .stMetric {
        background: #f8fafc;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e2e8f0;
        margin: 32px 0;
    }
</style>
""", unsafe_allow_html=True)


def carregar_dados_locais():
    dados = {}
    gupy_path = Path("./Participants-36809.xlsx")
    supplygo_path = Path("./Relatório SupplyGo - Desafio_Hack-ta-on.xlsx")

    if gupy_path.exists():
        try:
            df = pd.read_excel(gupy_path, index_col=None, keep_default_na=False, na_values="nan")
            dados["gupy"] = calcular_metrics_gupy(df)
            dados["gupy_df"] = df
        except Exception as e:
            st.warning(f"Erro ao carregar Gupy: {e}")

    if supplygo_path.exists():
        try:
            df = pd.read_excel(
                supplygo_path,
                header=6,
                index_col=None,
                keep_default_na=False,
                na_values="nan",
                sheet_name="Relatorio",
            )
            dados["supplygo"] = calcular_metrics_supplygo(df)
            dados["supplygo_df"] = df
        except Exception as e:
            st.warning(f"Erro ao carregar SupplyGo: {e}")

    return dados


def render_kpi_card(label, value, delta=None, delta_color="normal", card_color="blue"):
    color_map = {
        "blue": ("#dbeafe", "#bfdbfe", "#3b82f6", "#1e40af"),
        "green": ("#dcfce7", "#bbf7d0", "#22c55e", "#166534"),
        "yellow": ("#fef3c7", "#fde68a", "#f59e0b", "#92400e"),
        "purple": ("#f3e8ff", "#e9d5ff", "#a855f7", "#6b21a8"),
        "pink": ("#fce7f3", "#fbcfe8", "#ec4899", "#9f1239"),
        "teal": ("#ccfbf1", "#99f6e4", "#14b8a6", "#115e59"),
    }

    bg_start, bg_end, border, text_color = color_map.get(card_color, color_map["blue"])

    delta_html = ""
    if delta is not None:
        delta_icon = "▲" if delta_color == "good" else "▼" if delta_color == "bad" else "●"
        delta_text_color = "#22c55e" if delta_color == "good" else "#ef4444" if delta_color == "bad" else "#f59e0b"
        delta_html = f'<div style="font-size: 12px; color: {delta_text_color}; margin-top: 8px;">{delta_icon} {delta}</div>'

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {bg_start} 0%, {bg_end} 100%); 
                border-radius: 12px; 
                padding: 20px; 
                border-left: 4px solid {border};
                margin-bottom: 16px;">
        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; margin-bottom: 8px;">{label}</div>
        <div style="font-size: 32px; font-weight: 800; color: {text_color}; line-height: 1;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_grafico_status(dados, titulo="Distribuição de Status"):
    if not dados:
        return
    fig = go.Figure(data=[
        go.Pie(
            labels=list(dados.keys()),
            values=list(dados.values()),
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set2),
        )
    ])
    fig.update_layout(title=titulo, margin=dict(t=40, b=20, l=20, r=20), height=350)
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_barras(agrupamentos, titulo, x_field="nome", y_field="taxa_conclusao", cor="concluido"):
    if not agrupamentos:
        st.info("Sem dados para exibir.")
        return
    df = pd.DataFrame(agrupamentos)
    if df.empty:
        return
    df = df.head(20)
    fig = px.bar(
        df,
        x=x_field,
        y=y_field,
        color=cor if cor in df.columns else None,
        title=titulo,
        labels={x_field: "Grupo", y_field: "Taxa de Conclusão (%)"},
        color_continuous_scale="Viridis",
    )
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_progresso(agrupamentos, titulo):
    if not agrupamentos:
        st.info("Sem dados de progresso para exibir.")
        return
    df = pd.DataFrame(agrupamentos)
    if df.empty:
        return
    df = df.head(20)
    fig = px.bar(
        df,
        x="nome",
        y="progresso_medio",
        color="concluido",
        title=titulo,
        labels={"nome": "Grupo", "progresso_medio": "Progresso Médio (%)"},
        color_continuous_scale="Teal",
    )
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def render_tabela(df):
    if df is None or df.empty:
        st.info("Sem dados de colaboradores.")
        return
    colunas = [c for c in df.columns if not c.startswith("_")]
    st.dataframe(df[colunas].head(200), use_container_width=True, height=400)


def gerar_excel_export(dados):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if "gupy" in dados:
            resumo_gupy = pd.DataFrame([dados["gupy"]["resumo"]])
            resumo_gupy.to_excel(writer, sheet_name="Resumo Gupy", index=False)
            if dados["gupy"].get("por_estado"):
                pd.DataFrame(dados["gupy"]["por_estado"]).to_excel(writer, sheet_name="Gupy por Estado", index=False)
            if dados["gupy"].get("por_area"):
                pd.DataFrame(dados["gupy"]["por_area"]).to_excel(writer, sheet_name="Gupy por Área", index=False)
            if "gupy_df" in dados:
                dados["gupy_df"].to_excel(writer, sheet_name="Gupy Colaboradores", index=False)

        if "supplygo" in dados:
            resumo_sg = pd.DataFrame([dados["supplygo"]["resumo"]])
            resumo_sg.to_excel(writer, sheet_name="Resumo SupplyGo", index=False)
            if dados["supplygo"].get("por_estado"):
                pd.DataFrame(dados["supplygo"]["por_estado"]).to_excel(writer, sheet_name="SupplyGo por Estado", index=False)
            if dados["supplygo"].get("por_gerencia"):
                pd.DataFrame(dados["supplygo"]["por_gerencia"]).to_excel(writer, sheet_name="SupplyGo por Gerência", index=False)
            if "supplygo_df" in dados:
                dados["supplygo_df"].to_excel(writer, sheet_name="SupplyGo Colaboradores", index=False)

    return output.getvalue()


def pagina_resumo_geral(dados):
    st.markdown('<h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">Resumo Geral</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #64748b; margin: 0 0 32px 0;">Visão consolidada de todas as plataformas de treinamento</p>', unsafe_allow_html=True)
    
    if "gupy" not in dados and "supplygo" not in dados:
        st.warning("Nenhum dado disponível. Adicione uma planilha.")
        return
    
    total_geral = 0
    concluidos_geral = 0
    
    if "gupy" in dados:
        r = dados["gupy"]["resumo"]
        total_geral += r["total"]
        concluidos_geral += r["concluido"]
    
    if "supplygo" in dados:
        r = dados["supplygo"]["resumo"]
        total_geral += r["total"]
        concluidos_geral += r["concluido"]
    
    taxa_geral = round(concluidos_geral / total_geral * 100, 1) if total_geral > 0 else 0
    progresses = []
    if "gupy" in dados:
        progresses.append(dados["gupy"]["resumo"]["progresso_medio"])
    if "supplygo" in dados:
        progresses.append(dados["supplygo"]["resumo"]["progresso_medio"])
    progresso_medio = round(sum(progresses) / len(progresses), 1) if progresses else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Geral", total_geral, card_color="blue")
    with col2:
        render_kpi_card("Concluídos", concluidos_geral, card_color="green")
    with col3:
        render_kpi_card("Taxa de Conclusão", f"{taxa_geral}%", card_color="yellow")
    with col4:
        render_kpi_card("Progresso Médio", f"{progresso_medio}%", card_color="purple")
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if "gupy" in dados:
            render_grafico_barras(dados["gupy"]["por_estado"][:10], "Conclusão por Estado (Top 10)")
    with col2:
        if "gupy" in dados:
            render_grafico_status(dados["gupy"]["status_distribution"], "Status Gupy")
    
    st.divider()
    
    st.markdown('<h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 32px 0 16px 0;">Por Plataforma</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "gupy" in dados:
            r = dados["gupy"]["resumo"]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                        border-radius: 12px; padding: 20px; border: 1px solid #bfdbfe;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                    <div style="width: 32px; height: 32px; background: #3b82f6; border-radius: 8px; 
                                display: flex; align-items: center; justify-content: center; 
                                color: white; font-weight: 700;">G</div>
                    <div style="font-size: 16px; font-weight: 700; color: #1e40af;">Gupy</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Total</div>
                        <div style="font-size: 20px; font-weight: 700; color: #1e40af;">{r['total']}</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Concluídos</div>
                        <div style="font-size: 20px; font-weight: 700; color: #16a34a;">{r['concluido']}</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Taxa</div>
                        <div style="font-size: 20px; font-weight: 700; color: #d97706;">{r['taxa_conclusao']}%</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Dias Médios</div>
                        <div style="font-size: 20px; font-weight: 700; color: #9333ea;">{r['dias_medios_conclusao']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if "supplygo" in dados:
            r = dados["supplygo"]["resumo"]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                        border-radius: 12px; padding: 20px; border: 1px solid #bbf7d0;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                    <div style="width: 32px; height: 32px; background: #22c55e; border-radius: 8px; 
                                display: flex; align-items: center; justify-content: center; 
                                color: white; font-weight: 700;">S</div>
                    <div style="font-size: 16px; font-weight: 700; color: #166534;">SupplyGo</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Total</div>
                        <div style="font-size: 20px; font-weight: 700; color: #166534;">{r['total']}</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Concluídos</div>
                        <div style="font-size: 20px; font-weight: 700; color: #16a34a;">{r['concluido']}</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Taxa</div>
                        <div style="font-size: 20px; font-weight: 700; color: #d97706;">{r['taxa_conclusao']}%</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Problemas</div>
                        <div style="font-size: 20px; font-weight: 700; color: #dc2626;">{r['problema_plataforma']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if "gupy" in dados:
            render_grafico_barras(dados["gupy"]["por_estado"], "Gupy - Conclusão por Estado")
    with col2:
        if "supplygo" in dados:
            render_grafico_barras(dados["supplygo"]["por_estado"], "SupplyGo - Conclusão por Estado")


def pagina_por_plataforma(dados):
    st.markdown('<h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">Por Plataforma</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #64748b; margin: 0 0 32px 0;">Análise detalhada por plataforma de treinamento</p>', unsafe_allow_html=True)

    if "gupy" not in dados and "supplygo" not in dados:
        st.warning("Nenhum dado disponível.")
        return

    plataforma = st.selectbox("Selecione a plataforma", [k for k in ["gupy", "supplygo"] if k in dados])

    if plataforma == "gupy" and "gupy" in dados:
        r = dados["gupy"]["resumo"]
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_kpi_card("Total", r["total"], card_color="blue")
        with c2:
            render_kpi_card("Concluídos", r["concluido"], card_color="green")
        with c3:
            render_kpi_card("Não Iniciados", r["nao_iniciado"], card_color="red")
        with c4:
            render_kpi_card("Taxa Conclusão", f"{r['taxa_conclusao']}%", card_color="yellow")
        with c5:
            render_kpi_card("Dias Médios Conclusão", r["dias_medios_conclusao"], card_color="purple")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            render_grafico_status(dados["gupy"]["status_distribution"], "Status - Gupy")
        with col2:
            render_grafico_barras(dados["gupy"]["por_area"], "Conclusão por Área")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            render_grafico_barras(dados["gupy"]["por_unidade"], "Conclusão por Unidade")
        with col2:
            render_grafico_barras(dados["gupy"]["por_diretoria"], "Conclusão por Diretoria")

        if "gupy_df" in dados:
            st.divider()
            render_tabela(dados["gupy_df"])

    elif plataforma == "supplygo" and "supplygo" in dados:
        r = dados["supplygo"]["resumo"]
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_kpi_card("Total", r["total"], card_color="blue")
        with c2:
            render_kpi_card("Concluídos", r["concluido"], card_color="green")
        with c3:
            render_kpi_card("Cursando", r["cursando"], card_color="yellow")
        with c4:
            render_kpi_card("Taxa Conclusão", f"{r['taxa_conclusao']}%", card_color="yellow")
        with c5:
            render_kpi_card("Problemas", r["problema_plataforma"], card_color="red")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            render_grafico_status(dados["supplygo"]["status_distribution"], "Status - SupplyGo")
        with col2:
            render_grafico_barras(dados["supplygo"]["por_gerencia"], "Conclusão por Gerência")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            render_grafico_barras(dados["supplygo"]["por_unidade"], "Conclusão por Unidade")
        with col2:
            render_grafico_barras(dados["supplygo"]["por_familia_cargo"], "Conclusão por Família de Cargo")

        if "supplygo_df" in dados:
            st.divider()
            render_tabela(dados["supplygo_df"])


def pagina_por_regiao(dados):
    st.markdown('<h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">Por Região</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #64748b; margin: 0 0 32px 0;">Análise geográfica do desempenho</p>', unsafe_allow_html=True)

    fontes_disponiveis = []
    if "gupy" in dados:
        fontes_disponiveis.append("Gupy")
    if "supplygo" in dados:
        fontes_disponiveis.append("SupplyGo")

    if not fontes_disponiveis:
        st.warning("Nenhum dado disponível.")
        return

    fonte = st.selectbox("Plataforma", fontes_disponiveis)

    if fonte == "Gupy" and "gupy" in dados:
        estados = dados["gupy"].get("por_estado", [])
        render_grafico_barras(estados, "Gupy - Taxa de Conclusão por Estado")

        st.divider()

        render_grafico_progresso(dados["gupy"].get("progresso_por_estado", []), "Gupy - Progresso Médio por Estado")

        if estados:
            st.divider()
            st.markdown('<h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 32px 0 16px 0;">Detalhamento por Estado</h2>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(estados), use_container_width=True)

    elif fonte == "SupplyGo" and "supplygo" in dados:
        estados = dados["supplygo"].get("por_estado", [])
        render_grafico_barras(estados, "SupplyGo - Taxa de Conclusão por Estado")

        st.divider()

        render_grafico_progresso(dados["supplygo"].get("progresso_por_estado", []), "SupplyGo - Progresso Médio por Estado")

        if estados:
            st.divider()
            st.markdown('<h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 32px 0 16px 0;">Detalhamento por Estado</h2>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(estados), use_container_width=True)


def pagina_por_lideranca(dados):
    st.markdown('<h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">Por Liderança</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #64748b; margin: 0 0 32px 0;">Análise por liderança e chefia</p>', unsafe_allow_html=True)

    fontes_disponiveis = []
    if "gupy" in dados:
        fontes_disponiveis.append("Gupy")
    if "supplygo" in dados:
        fontes_disponiveis.append("SupplyGo")

    if not fontes_disponiveis:
        st.warning("Nenhum dado disponível.")
        return

    fonte = st.selectbox("Plataforma", fontes_disponiveis)

    if fonte == "Gupy" and "gupy" in dados:
        chefia = dados["gupy"].get("por_chefia", [])
        render_grafico_barras(chefia, "Gupy - Taxa de Conclusão por Chefia")

        if chefia:
            st.divider()
            st.markdown('<h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 32px 0 16px 0;">Detalhamento por Chefia</h2>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(chefia), use_container_width=True)

    elif fonte == "SupplyGo" and "supplygo" in dados:
        col1, col2 = st.columns(2)
        with col1:
            lideranca = dados["supplygo"].get("por_lideranca", [])
            render_grafico_barras(lideranca, "SupplyGo - Conclusão por Liderança Corporativa")
        with col2:
            lideranca_imediata = dados["supplygo"].get("por_lideranca_imediata", [])
            render_grafico_barras(lideranca_imediata, "SupplyGo - Conclusão por Liderança Imediata")

        if lideranca:
            st.divider()
            st.markdown('<h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 32px 0 16px 0;">Detalhamento por Liderança Corporativa</h2>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(lideranca), use_container_width=True)


def main():
    if "dados" not in st.session_state:
        st.session_state["dados"] = carregar_dados_locais()

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Resumo Geral"

    with st.sidebar:
        st.image("img/8f979e00-5fb5-4fe0-81dd-dbc6d0d3ac08.png", use_container_width=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 32px; padding-top: 16px;">
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; padding-left: 12px;">Navegação</div>', unsafe_allow_html=True)

        pagina_atual = st.session_state.get("pagina", "Resumo Geral")

        if st.button("📊 Resumo Geral", use_container_width=True, type="primary" if pagina_atual == "Resumo Geral" else "secondary"):
            st.session_state["pagina"] = "Resumo Geral"
        if st.button("💻 Plataformas", use_container_width=True, type="primary" if pagina_atual == "Plataformas" else "secondary"):
            st.session_state["pagina"] = "Plataformas"
        if st.button("🗺️ Regiões", use_container_width=True, type="primary" if pagina_atual == "Regiões" else "secondary"):
            st.session_state["pagina"] = "Regiões"
        if st.button("👥 Liderança", use_container_width=True, type="primary" if pagina_atual == "Liderança" else "secondary"):
            st.session_state["pagina"] = "Liderança"

        st.divider()

        st.markdown('<div style="font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; padding-left: 12px;">Dados</div>', unsafe_allow_html=True)

        with st.expander("📁 Upload Planilha", expanded=False):
            arquivo = st.file_uploader("Enviar Excel (.xlsx)", type=["xlsx"], key="upload_sidebar", label_visibility="collapsed")
            if arquivo:
                try:
                    conteudo = arquivo.read()
                    xl = pd.ExcelFile(io.BytesIO(conteudo))
                    if "Relatorio" in xl.sheet_names:
                        df = pd.read_excel(io.BytesIO(conteudo), header=6, sheet_name="Relatorio")
                    else:
                        df = pd.read_excel(io.BytesIO(conteudo))

                    fonte = detectar_fonte(df)
                    resultado = processar_excel(df)

                    if fonte == "gupy":
                        st.session_state["dados"]["gupy"] = resultado
                        st.session_state["dados"]["gupy_df"] = df
                        st.success("Planilha Gupy adicionada!")
                    elif fonte == "supplygo":
                        st.session_state["dados"]["supplygo"] = resultado
                        st.session_state["dados"]["supplygo_df"] = df
                        st.success("Planilha SupplyGo adicionada!")
                    else:
                        st.error("Fonte não identificada.")
                except Exception as e:
                    st.error(f"Erro: {e}")

        dados = st.session_state["dados"]
        if "gupy" in dados or "supplygo" in dados:
            excel_bytes = gerar_excel_export(dados)
            st.download_button(
                label="⬇ Exportar Relatório",
                data=excel_bytes,
                file_name="safra_relatorio.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary",
            )

    dados = st.session_state["dados"]
    pagina = st.session_state["pagina"]

    if pagina == "Resumo Geral":
        pagina_resumo_geral(dados)
    elif pagina == "Plataformas":
        pagina_por_plataforma(dados)
    elif pagina == "Regiões":
        pagina_por_regiao(dados)
    elif pagina == "Liderança":
        pagina_por_lideranca(dados)


if __name__ == "__main__":
    main()
