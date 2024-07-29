import pandas as pd
import plotly.express as px

def bar_plot(df: pd.DataFrame, x_axis: str, y_axis: str, titulo: str):
    """
    Recebe um dataframe para fazer a plotagem dos dados.
    
    Parâmetros:
    - df: dataframe com as informações
    - x_axis: nome da coluna do eixo X
    - y_axis: nome da coluna do eixo Y
    - titulo: título desejado

    Retorna:
    - Gráfico de barras
    """
    fig = px.bar(df[0:11], x=x_axis, y=y_axis)
    fig.update_xaxes(tickfont=dict(size=15))
    fig.update_traces(
        marker_color='#f5f5f5',
    )
    fig.update_layout(
        showlegend=True,
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=22, color='white'),
        ),
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=22, color='white')),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        height=600,
        yaxis=dict(
            title=dict(text='TERMO', font=dict(size=22, color='white')),  
            tickfont=dict(size=22, color='white') 
        ),
        xaxis=dict(
            title=dict(text='RELEVÂNCIA', font=dict(size=22, color='white')),  
            tickfont=dict(size=22, color='white') 
        )
    )

    # for trace in fig.data:
    #     trace.textposition = 'outside'
    #     trace.textfont = dict(size=18, color='white')
    #     if 'text' in trace:
    #         trace.text = [f'{t:.2f}' if t else '' for t in trace.y]
    #     trace.insidetextanchor = 'start'
    #     trace.textangle = 0
    
    return fig
