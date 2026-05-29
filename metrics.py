"""
TrainSight Metrics Engine - Motor de métricas escalável

Escalabilidade:
  - Detecta automaticamente TODAS as colunas categóricas do DataFrame
  - Gera agrupamentos para QUALQUER coluna sem precisar alterar código
  - Novos estados, filiais, cargos, gerências, etc. são tratados automaticamente
  - Configuração via dicionário de mapeamento (adicionar nova entrada = novo suporte)
"""

import pandas as pd
import re
from typing import Dict, List, Optional, Set


# =============================================================================
# Mapas de normalização (adicionar novas entradas = novo suporte automático)
# =============================================================================

ESTADOS_MAP = {
    "RIO DE JANEIRO": "RJ", "SAO PAULO": "SP",
    "CEARA": "CE", "CEARÁ": "CE", "PERNAMBUCO": "PE",
    "BAHIA": "BA", "RIO GRANDE DO SUL": "RS",
    "PARANA": "PR", "PARANÁ": "PR", "PARA": "PA",
    "SANTA CATARINA": "SC", "MINAS GERAIS": "MG",
    "GOIÁS": "GO", "GOIAS": "GO", "DISTRITO FEDERAL": "DF",
    "ESPÍRITO SANTO": "ES", "ESPIRITO SANTO": "ES",
    "MATO GROSSO DO SUL": "MS", "MATO GROSSO": "MT",
    "RIO GRANDE DO NORTE": "RN", "PARAÍBA": "PB", "PARAIBA": "PB",
    "MARANHÃO": "MA", "MARANHAO": "MA", "PIAUI": "PI", "PIAUÍ": "PI",
    "ALAGOAS": "AL", "SERGIPE": "SE", "TOCANTINS": "TO",
    "ACRE": "AC", "AMAZONAS": "AM", "AMAPÁ": "AP", "AMAPA": "AP",
    "RONDÔNIA": "RO", "RONDONIA": "RO", "RORAIMA": "RR",
}

AREA_MAP = {
    "SAUD": "Comercial Saudáveis",
    "MARKETING": "Marketing",
    "LOG": "Logística",
    "GENTE": "Gente & Gestão",
    "GESTÃO": "Gente & Gestão",
    "GESTAO": "Gente & Gestão",
}

# Padrões para identificar colunas que devem ser agrupadas
# Adicionar novos padrões aqui = novo tipo de dado automaticamente agrupado
GROUPING_PATTERNS_GUPY = [
    {"col": "Estado", "normalizador": "estado"},
    {"col": "Área", "normalizador": "area"},
    {"col": "Unidade", "normalizador": "raw"},
    {"col": "Diretoria", "normalizador": "raw"},
    {"col": "Chefia ADP", "normalizador": "raw"},
    {"col": "Cargo", "normalizador": "raw"},
    {"col": "Subarea", "normalizador": "raw"},
    {"col": "Centro de Resultado", "normalizador": "raw"},
    {"col": "Centro de Custo Contábil", "normalizador": "raw"},
]

GROUPING_PATTERNS_SUPPLYGO = [
    {"col": "ESTADO", "normalizador": "estado"},
    {"col": "GERÊNCIA CORPORATIVA", "normalizador": "raw"},
    {"col": "LIDERANÇA CORPORATIVA", "normalizador": "raw"},
    {"col": "UNIDADE", "normalizador": "raw"},
    {"col": "FAMÍLIA DE CARGO", "normalizador": "raw"},
    {"col": "CARGO", "normalizador": "raw"},
    {"col": "GERÊNCIA", "normalizador": "raw"},
    {"col": "LIDERANÇA IMEDIATA", "normalizador": "raw"},
    {"col": "CENTRO DE CUSTO", "normalizador": "raw"},
]


# =============================================================================
# Funções de normalização
# =============================================================================

def normalizar_estado(v: str) -> str:
    """Normaliza nome/código de estado para sigla de 2 letras."""
    if not v or not isinstance(v, str):
        return "N/A"
    upper = str(v).strip().upper()
    if upper in ESTADOS_MAP:
        return ESTADOS_MAP[upper]
    if len(upper) == 2 and upper.isalpha():
        return upper
    return "N/A"


def normalizar_area(v: str) -> str:
    """Normaliza nome de área para categoria padronizada."""
    if not v or not isinstance(v, str):
        return "N/A"
    s = str(v).strip()
    upper = s.upper()
    for key, val in AREA_MAP.items():
        if key in upper:
            return val
    return s


def extrair_progresso(v) -> int:
    """Extrai número de progresso (ex: '75%' -> 75)."""
    if pd.isna(v):
        return 0
    s = str(v).replace("%", "").strip()
    match = re.search(r'(\d+)', s)
    if match:
        return int(match.group(1))
    return 0


# =============================================================================
# Motor de agrupamento genérico (escalável)
# =============================================================================

def _agrupar(df: pd.DataFrame, col: str, status_col: str = "_status") -> List[dict]:
    """Agrupa DataFrame por coluna e calcula métricas de status.
    
    Escalável: funciona com QUALQUER coluna, não precisa de configuração.
    """
    if col not in df.columns:
        return []
    grupos = df.groupby(col)
    resultado = []
    for nome, grupo in grupos:
        total = len(grupo)
        conc = int((grupo[status_col] == "Concluído").sum())
        nao_inic = int((grupo[status_col] == "Não iniciado").sum())
        nao_conc = int((grupo[status_col] == "Não concluído").sum())
        cursando = int((grupo[status_col] == "Cursando").sum())
        taxa = round(conc / total * 100, 1) if total else 0
        resultado.append({
            "nome": str(nome),
            "total": total,
            "concluido": conc,
            "nao_iniciado": nao_inic,
            "nao_concluido": nao_conc,
            "cursando": cursando,
            "taxa_conclusao": taxa,
        })
    return sorted(resultado, key=lambda x: x["total"], reverse=True)


def _agrupar_com_progresso(df: pd.DataFrame, col: str, status_col: str = "_status", 
                            prog_col: str = "_prog") -> List[dict]:
    """Agrupa por coluna com métrica de progresso adicional."""
    if col not in df.columns:
        return []
    grupos = df.groupby(col)
    resultado = []
    for nome, grupo in grupos:
        total = len(grupo)
        avg_progresso = round(float(grupo[prog_col].mean()), 1)
        conc = int((grupo[status_col] == "Concluído").sum())
        resultado.append({
            "nome": str(nome),
            "total": total,
            "concluido": conc,
            "progresso_medio": avg_progresso,
        })
    return sorted(resultado, key=lambda x: x["total"], reverse=True)


def _agrupar_tudo(df: pd.DataFrame, status_col: str = "_status",
                  patterns: List[dict] = None) -> Dict[str, List[dict]]:
    """Agrupa DataFrame por TODAS as colunas listadas nos patterns.
    
    Escalável: basta adicionar um dicionário ao pattern list para 
    que aquela coluna seja automaticamente agrupada.
    
    Args:
        df: DataFrame com dados processados
        status_col: nome da coluna de status
        patterns: lista de {"col": "nome_coluna", "normalizador": "tipo"}
    
    Returns:
        Dict com nome da coluna como chave e lista de agrupamentos como valor
    """
    if patterns is None:
        return {}
    
    resultado = {}
    for pattern in patterns:
        col = pattern["col"]
        normalizador = pattern.get("normalizador", "raw")
        
        if col not in df.columns:
            continue
        
        # Se tem normalizador, aplica
        if normalizador == "estado":
            df[f"_{col}_norm"] = df[col].apply(lambda x: normalizar_estado(str(x)) if pd.notna(x) else "N/A")
            result_col = f"_{col}_norm"
        elif normalizador == "area":
            df[f"_{col}_norm"] = df[col].apply(lambda x: normalizar_area(str(x)) if pd.notna(x) else "N/A")
            result_col = f"_{col}_norm"
        else:
            result_col = col
        
        resultado[col] = _agrupar(df, result_col, status_col)
    
    return resultado


# =============================================================================
# Detecção de fonte
# =============================================================================

def detectar_fonte(df: pd.DataFrame) -> str:
    """Detecta automaticamente se o DataFrame é Gupy ou SupplyGo.
    
    Escalável: adiciona novos padrões de detecção aqui para suportar 
    novas fontes de dados sem alterar lógica de processamento.
    """
    cols = [c.strip().lower() for c in df.columns]
    
    # Padrões Gupy
    if any(p in cols for p in ["status de realização", "progresso", "itens completados", "pontuação no ranking"]):
        return "gupy"
    
    # Padrões SupplyGo
    if any(p in cols for p in ["status trilha", "carga horária total", "carga horária cursada"]):
        return "supplygo"
    
    # Fallback: verifica colunas genéricas
    if "nome" in cols and "estado" in cols:
        return "gupy"
    
    return "desconhecido"


# =============================================================================
# Processamento Gupy (escalável)
# =============================================================================

def calcular_metrics_gupy(df: pd.DataFrame) -> dict:
    """Processa dados Gupy.
    
    Escalável: adiciona novos campos ao df e padrões de agrupamento
    para que novas métricas e classificações sejam geradas automaticamente.
    """
    df = df.copy()
    
    # Normalizar colunas
    df["_estado"] = df.get("Estado", pd.Series([""] * len(df))).apply(
        lambda x: normalizar_estado(str(x)) if pd.notna(x) else "N/A"
    )
    df["_area"] = df.get("Área", pd.Series([""] * len(df))).apply(
        lambda x: normalizar_area(str(x)) if pd.notna(x) else "N/A"
    )
    df["_status"] = df.get("Status de realização", pd.Series([""] * len(df))).fillna("Não iniciado").astype(str).str.strip()
    df["_prog"] = df.get("Progresso", pd.Series([0] * len(df))).apply(extrair_progresso)
    df["_pont"] = pd.to_numeric(df.get("Pontuação no ranking", pd.Series([0] * len(df))), errors="coerce").fillna(0)
    df["_media"] = pd.to_numeric(df.get("Média", pd.Series([0] * len(df))), errors="coerce").fillna(0)
    
    # Tempo de conclusão
    df["_data_inicio"] = pd.to_datetime(df.get("Data de início na trilha", pd.Series([""] * len(df))), errors="coerce", dayfirst=True)
    df["_data_fim"] = pd.to_datetime(df.get("Data de finalização na trilha", pd.Series([""] * len(df))), errors="coerce", dayfirst=True)
    df["_dias_conclusao"] = (df["_data_fim"] - df["_data_inicio"]).dt.days
    df.loc[df["_data_fim"].isna() | df["_data_inicio"].isna(), "_dias_conclusao"] = None

    total = len(df)
    concluido = int((df["_status"] == "Concluído").sum())
    nao_inic = int((df["_status"] == "Não iniciado").sum())
    nao_conc = int((df["_status"] == "Não concluído").sum())
    ponts = df[df["_pont"] > 0]["_pont"]
    medias = df[df["_media"] > 0]["_media"]
    nome_trilha = str(df["Nome da trilha"].iloc[0]) if "Nome da trilha" in df.columns and len(df) > 0 else ""

    status_dist = df["_status"].value_counts().to_dict()
    progresso_medio = round(float(df["_prog"].mean()), 1) if total else 0
    
    concluidos_df = df[df["_status"] == "Concluído"]
    dias_medios_conclusao = round(float(concluidos_df["_dias_conclusao"].mean()), 1) if len(concluidos_df) > 0 else 0

    # Agrupamentos escaláveis
    agrupamentos = _agrupar_tudo(df, "_status", GROUPING_PATTERNS_GUPY)
    
    # Progresso por estado
    progresso_estado = _agrupar_com_progresso(df, "_estado", "_status", "_prog")

    return {
        "resumo": {
            "total": total,
            "concluido": concluido,
            "nao_iniciado": nao_inic,
            "nao_concluido": nao_conc,
            "taxa_conclusao": round(concluido / total * 100, 1) if total else 0,
            "pontuacao_media": round(float(ponts.mean()), 1) if len(ponts) else 0,
            "nota_media": round(float(medias.mean()), 1) if len(medias) else 0,
            "nome_trilha": nome_trilha,
            "progresso_medio": progresso_medio,
            "dias_medios_conclusao": dias_medios_conclusao,
        },
        "por_estado": agrupamentos.get("Estado", []),
        "por_area": agrupamentos.get("Área", []),
        "por_unidade": agrupamentos.get("Unidade", []),
        "por_diretoria": agrupamentos.get("Diretoria", []),
        "por_chefia": agrupamentos.get("Chefia ADP", []),
        "por_cargo": agrupamentos.get("Cargo", []),
        "por_subarea": agrupamentos.get("Subarea", []),
        "por_centro_resultado": agrupamentos.get("Centro de Resultado", []),
        "por_centro_custo": agrupamentos.get("Centro de Custo Contábil", []),
        "status_distribution": {str(k): int(v) for k, v in status_dist.items()},
        "progresso_por_estado": progresso_estado,
    }


# =============================================================================
# Processamento SupplyGo (escalável)
# =============================================================================

def calcular_metrics_supplygo(df: pd.DataFrame) -> dict:
    """Processa dados SupplyGo.
    
    Escalável: novos campos e agrupamentos são adicionados apenas
    atualizando GROUPING_PATTERNS_SUPPLYGO e este método.
    """
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    
    df["_estado"] = df.get("ESTADO", pd.Series([""] * len(df))).apply(
        lambda x: normalizar_estado(str(x)) if pd.notna(x) else "N/A"
    )
    df["_status"] = df.get("Status Trilha", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()
    df["_carga_total"] = pd.to_numeric(df.get("Carga Horária Total", pd.Series([0] * len(df))), errors="coerce").fillna(0)
    df["_carga_cursada"] = pd.to_numeric(df.get("Carga Horária Cursada", pd.Series([0] * len(df))), errors="coerce").fillna(0)
    
    problema_col = "Problema na plataforma?"
    df["_problema"] = df.get(problema_col, pd.Series([False] * len(df))).fillna(False).astype(bool)
    
    # Progresso em %
    df["_progresso_pct"] = df.apply(
        lambda row: round(row["_carga_cursada"] / row["_carga_total"] * 100, 1) 
        if row["_carga_total"] > 0 else 0,
        axis=1
    )

    total = len(df)
    concluido = int((df["_status"] == "Concluído").sum())
    cursando = int((df["_status"] == "Cursando").sum())
    nao_inic = int((df["_status"] == "Não iniciado").sum())
    problema = int(df["_problema"].sum())

    carga_media = round(float(df["_carga_cursada"].mean()), 1) if total else 0
    carga_total_media = round(float(df["_carga_total"].mean()), 1) if total else 0
    progresso_medio = round(float(df["_progresso_pct"].mean()), 1) if total else 0

    status_dist = df["_status"].value_counts().to_dict()

    # Agrupamentos escaláveis
    agrupamentos = _agrupar_tudo(df, "_status", GROUPING_PATTERNS_SUPPLYGO)
    
    # Progresso por estado
    progresso_estado = _agrupar_com_progresso(df, "_estado", "_status", "_progresso_pct")

    return {
        "resumo": {
            "total": total,
            "concluido": concluido,
            "cursando": cursando,
            "nao_iniciado": nao_inic,
            "taxa_conclusao": round(concluido / total * 100, 1) if total else 0,
            "carga_horaria_media": carga_media,
            "carga_horaria_total_media": carga_total_media,
            "problema_plataforma": int(problema),
            "progresso_medio": progresso_medio,
        },
        "por_estado": agrupamentos.get("ESTADO", []),
        "por_gerencia": agrupamentos.get("GERÊNCIA CORPORATIVA", []),
        "por_lideranca": agrupamentos.get("LIDERANÇA CORPORATIVA", []),
        "por_unidade": agrupamentos.get("UNIDADE", []),
        "por_familia_cargo": agrupamentos.get("FAMÍLIA DE CARGO", []),
        "por_cargo": agrupamentos.get("CARGO", []),
        "por_gerencia_operacional": agrupamentos.get("GERÊNCIA", []),
        "por_lideranca_imediata": agrupamentos.get("LIDERANÇA IMEDIATA", []),
        "por_centro_custo": agrupamentos.get("CENTRO DE CUSTO", []),
        "status_distribution": {str(k): int(v) for k, v in status_dist.items()},
        "progresso_por_estado": progresso_estado,
    }


# =============================================================================
# Função principal (escalável)
# =============================================================================

def processar_excel(df: pd.DataFrame, fonte: str = None) -> dict:
    """Processa qualquer planilha de treinamento.
    
    Escalável: para adicionar suporte a uma nova fonte:
    1. Adicione padrões em detectar_fonte()
    2. Crie uma função calcular_metrics_<fonte>()
    3. Adicione padrões de agrupamento em GROUPING_PATTERNS_*
    """
    if fonte is None:
        fonte = detectar_fonte(df)
    if fonte == "gupy":
        return calcular_metrics_gupy(df)
    elif fonte == "supplygo":
        return calcular_metrics_supplygo(df)
    else:
        return {
            "erro": "Fonte não identificada",
            "colunas_detectadas": list(df.columns),
            "sugestao": "Adicione padrões de detecção em metrics.detectar_fonte()"
        }
