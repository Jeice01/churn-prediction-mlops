
"""Orbis Intelligence — Dashboard de observabilidade MLOps."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
LOGO = Path(__file__).resolve().parent / "assets" / "orbis-logo.png"

if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from api.database.dashboard_queries import consultar_metricas_diarias


st.set_page_config(
    page_title="Orbis Intelligence | MLOps",
    page_icon=str(LOGO) if LOGO.exists() else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Identidade visual Orbis Conect
st.markdown(
    """
    <style>
    .stApp {
        background: #0B1120;
        color: #F1F5F9;
    }

    [data-testid="stSidebar"] {
        background: #111B30;
        border-right: 1px solid #263650;
    }

    [data-testid="stMetric"] {
        background: #152139;
        padding: 22px;
        border: 1px solid #283B59;
        border-radius: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC;
        font-size: 2rem;
    }

    h1, h2, h3 {
        color: #F8FAFC;
    }

    .orbis-subtitle {
        color: #94A3B8;
        margin-top: -10px;
        margin-bottom: 24px;
    }

    .orbis-label {
        display: inline-block;
        background: #17365B;
        color: #93C5FD;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-bottom: 12px;
    }

    div[data-testid="stPlotlyChart"] {
        background: #152139;
        border-radius: 16px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Navegação lateral
with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    else:
        st.title("ORBIS CONECT")

    st.divider()

    pagina = st.radio(
        "Navegação",
        [
            "Visão Geral",
            "Monitoramento da API",
            "Inteligência de Churn",
        ],
    )

    st.divider()
    st.caption("Orbis Intelligence")
    st.caption("MLOps Dashboard | v0.3")


# Cabeçalho
st.markdown(
    '<span class="orbis-label">DADOS REAIS • SUPABASE</span>',
    unsafe_allow_html=True,
)

st.title("Orbis Intelligence")

st.markdown(
    '<p class="orbis-subtitle">'
    'Monitoramento inteligente de modelos de Machine Learning'
    '</p>',
    unsafe_allow_html=True,
)


# Filtro interativo
opcoes_periodo = {
    "Últimos 7 dias": 7,
    "Últimos 15 dias": 15,
    "Últimos 30 dias": 30,
    "Todo o histórico": None,
}

coluna_filtro, coluna_info = st.columns([1, 3])

with coluna_filtro:
    periodo_selecionado = st.selectbox(
        "Período de análise",
        options=list(opcoes_periodo.keys()),
        index=3,
    )

dias = opcoes_periodo[periodo_selecionado]

with coluna_info:
    st.write("")
    st.caption(
        f"Exibindo: {periodo_selecionado} | "
        "Dados agrupados no horário de Brasília"
    )


# Consulta filtrada ao Supabase
@st.cache_data(ttl=60, show_spinner=False)
def carregar_metricas_diarias(periodo):
    return pd.DataFrame(consultar_metricas_diarias(periodo))


try:
    dados = carregar_metricas_diarias(dias)

    if not dados.empty:
        dados["dia"] = pd.to_datetime(dados["dia"])
        dados["data_label"] = dados["dia"].dt.strftime("%d/%m/%Y")

except Exception:
    st.error(
        "Não foi possível consultar os dados do Supabase. "
        "Verifique a conexão com o banco."
    )
    st.stop()


# Indicadores calculados sobre o período selecionado
if dados.empty:
    indicadores = {
        "total_requisicoes": 0,
        "total_erros_http": 0,
        "tempo_medio_ms": 0.0,
        "total_previsoes": 0,
        "total_churn_previsto": 0,
    }
else:
    total_requisicoes = int(dados["requisicoes"].sum())

    # Média ponderada pelo volume de requisições de cada dia.
    tempo_medio = (
        (dados["latencia_ms"] * dados["requisicoes"]).sum()
        / total_requisicoes
        if total_requisicoes > 0
        else 0.0
    )

    indicadores = {
        "total_requisicoes": total_requisicoes,
        "total_erros_http": int(dados["erros"].sum()),
        "tempo_medio_ms": float(tempo_medio),
        "total_previsoes": int(dados["previsoes"].sum()),
        "total_churn_previsto": int(dados["churn"].sum()),
    }


def formatar_inteiro(valor):
    return f"{valor:,}".replace(",", ".")


def formatar_decimal(valor):
    return (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


CORES = {
    "azul": "#4A90D9",
    "laranja": "#F58220",
    "vermelho": "#EF4444",
    "fundo": "#152139",
    "texto": "#E2E8F0",
}


def estilizar_grafico(figura):
    figura.update_layout(
        paper_bgcolor=CORES["fundo"],
        plot_bgcolor=CORES["fundo"],
        font_color=CORES["texto"],
        margin=dict(l=15, r=15, t=50, b=15),
        xaxis=dict(
            showgrid=False,
            title_text="Data",
            type="category",
        ),
        yaxis=dict(
            gridcolor="#283B59",
            rangemode="tozero",
        ),
        showlegend=False,
    )
    return figura


def exibir_grafico(coluna, titulo, cor, eixo_y):
    if dados.empty:
        st.info("Não existem registros no período selecionado.")
        return

    figura = px.bar(
        dados,
        x="data_label",
        y=coluna,
        title=titulo,
        color_discrete_sequence=[cor],
    )

    figura.update_yaxes(title_text=eixo_y)

    st.plotly_chart(
        estilizar_grafico(figura),
        use_container_width=True,
    )


# Página 1 — Visão Geral
if pagina == "Visão Geral":
    st.subheader("Visão geral da operação")

    coluna1, coluna2, coluna3, coluna4 = st.columns(4)

    coluna1.metric(
        "Requisições",
        formatar_inteiro(indicadores["total_requisicoes"]),
    )

    coluna2.metric(
        "Erros HTTP",
        formatar_inteiro(indicadores["total_erros_http"]),
    )

    coluna3.metric(
        "Latência média",
        f'{formatar_decimal(indicadores["tempo_medio_ms"])} ms',
    )

    coluna4.metric(
        "Previsões de churn",
        formatar_inteiro(indicadores["total_churn_previsto"]),
    )

    st.write("")

    esquerda, direita = st.columns(2)

    with esquerda:
        exibir_grafico(
            "requisicoes",
            "Volume diário de requisições",
            CORES["azul"],
            "Requisições",
        )

    with direita:
        exibir_grafico(
            "churn",
            "Previsões diárias de churn",
            CORES["laranja"],
            "Previsões",
        )


# Página 2 — Monitoramento da API
elif pagina == "Monitoramento da API":
    st.subheader("Monitoramento da API")

    coluna1, coluna2, coluna3 = st.columns(3)

    coluna1.metric(
        "Requisições",
        formatar_inteiro(indicadores["total_requisicoes"]),
    )

    coluna2.metric(
        "Erros HTTP",
        formatar_inteiro(indicadores["total_erros_http"]),
    )

    coluna3.metric(
        "Latência média",
        f'{formatar_decimal(indicadores["tempo_medio_ms"])} ms',
    )

    esquerda, direita = st.columns(2)

    with esquerda:
        exibir_grafico(
            "requisicoes",
            "Requisições por dia",
            CORES["azul"],
            "Requisições",
        )

    with direita:
        exibir_grafico(
            "erros",
            "Erros HTTP por dia",
            CORES["vermelho"],
            "Erros",
        )

    exibir_grafico(
        "latencia_ms",
        "Latência média diária",
        CORES["laranja"],
        "Milissegundos",
    )


# Página 3 — Inteligência de Churn
else:
    st.subheader("Inteligência de Churn")

    coluna1, coluna2 = st.columns(2)

    coluna1.metric(
        "Previsões realizadas",
        formatar_inteiro(indicadores["total_previsoes"]),
    )

    coluna2.metric(
        "Churn previsto",
        formatar_inteiro(indicadores["total_churn_previsto"]),
    )

    esquerda, direita = st.columns(2)

    with esquerda:
        exibir_grafico(
            "previsoes",
            "Total diário de previsões",
            CORES["azul"],
            "Previsões",
        )

    with direita:
        exibir_grafico(
            "churn",
            "Previsões positivas de churn",
            CORES["laranja"],
            "Churn previsto",
        )


# Rodapé
st.divider()

st.caption(
    f"Período: {periodo_selecionado} • "
    "Fonte: Supabase PostgreSQL • "
    "Cache: 60 segundos"
)

st.caption(
    "© 2026 Orbis Conect — Automatize. Conecte. Evolua."
)
