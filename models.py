from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ResumoGupy(BaseModel):
    total: int = 0
    concluido: int = 0
    nao_iniciado: int = 0
    nao_concluido: int = 0
    taxa_conclusao: float = 0.0
    pontuacao_media: float = 0.0
    nota_media: float = 0.0
    nome_trilha: str = ""
    progresso_medio: float = 0.0
    dias_medios_conclusao: float = 0.0


class ResumoSupplyGo(BaseModel):
    total: int = 0
    concluido: int = 0
    cursando: int = 0
    nao_iniciado: int = 0
    taxa_conclusao: float = 0.0
    carga_horaria_media: float = 0.0
    carga_horaria_total_media: float = 0.0
    problema_plataforma: int = 0
    progresso_medio: float = 0.0


class Agrupamento(BaseModel):
    nome: str = ""
    total: int = 0
    concluido: int = 0
    nao_iniciado: int = 0
    nao_concluido: int = 0
    cursando: int = 0
    taxa_conclusao: float = 0.0


class AgrupamentoProgresso(BaseModel):
    nome: str = ""
    total: int = 0
    concluido: int = 0
    progresso_medio: float = 0.0


class RespostaGupy(BaseModel):
    resumo: ResumoGupy = Field(default_factory=ResumoGupy)
    por_estado: List[Agrupamento] = Field(default_factory=list)
    por_area: List[Agrupamento] = Field(default_factory=list)
    por_unidade: List[Agrupamento] = Field(default_factory=list)
    por_diretoria: List[Agrupamento] = Field(default_factory=list)
    por_chefia: List[Agrupamento] = Field(default_factory=list)
    por_cargo: List[Agrupamento] = Field(default_factory=list)
    status_distribution: Dict[str, int] = Field(default_factory=dict)
    progresso_por_estado: List[AgrupamentoProgresso] = Field(default_factory=list)


class RespostaSupplyGo(BaseModel):
    resumo: ResumoSupplyGo = Field(default_factory=ResumoSupplyGo)
    por_estado: List[Agrupamento] = Field(default_factory=list)
    por_gerencia: List[Agrupamento] = Field(default_factory=list)
    por_lideranca: List[Agrupamento] = Field(default_factory=list)
    por_unidade: List[Agrupamento] = Field(default_factory=list)
    por_familia_cargo: List[Agrupamento] = Field(default_factory=list)
    por_cargo: List[Agrupamento] = Field(default_factory=list)
    por_gerencia_operacional: List[Agrupamento] = Field(default_factory=list)
    status_distribution: Dict[str, int] = Field(default_factory=dict)
    progresso_por_estado: List[AgrupamentoProgresso] = Field(default_factory=list)


class RespostaCombinada(BaseModel):
    gupy: RespostaGupy = Field(default_factory=RespostaGupy)
    supplygo: RespostaSupplyGo = Field(default_factory=RespostaSupplyGo)


class UploadUrlRequest(BaseModel):
    url: str
