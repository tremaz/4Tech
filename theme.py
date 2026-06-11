import plotly.io as pio
import plotly.graph_objects as go

SAFRA_COLORS = {
    "blue": "#3b82f6",
    "green": "#22c55e",
    "yellow": "#f59e0b",
    "purple": "#a855f7",
    "pink": "#ec4899",
    "teal": "#14b8a6",
    "red": "#ef4444",
    "orange": "#f97316",
}

SAFRA_PALETTE = [SAFRA_COLORS[k] for k in ("blue", "green", "yellow", "purple", "pink", "teal", "orange")]

def create_safra_template():
    template = go.layout.Template()
    
    template.layout = go.Layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#0f172a"),
        title=dict(font=dict(family="Inter:wght@700, -apple-system, sans-serif", size=14, color="#0f172a"), x=0, xanchor="left"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        colorway=SAFRA_PALETTE,
        xaxis=dict(
            gridcolor="#e2e8f0",
            gridwidth=1,
            zeroline=False,
            showline=False,
            ticks="",
        ),
        yaxis=dict(
            gridcolor="#e2e8f0",
            gridwidth=1,
            zeroline=False,
            showline=False,
            ticks="",
        ),
        margin=dict(t=40, b=20, l=20, r=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
    )
    
    return template

pio.templates["safra"] = create_safra_template()
pio.templates.default = "safra"
