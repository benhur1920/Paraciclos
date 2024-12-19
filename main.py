import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Paracicos",
    layout="wide"
)

def titulo(mensagem):
    st.markdown(
        f"""
        <h1 style="color: #12239E;">{mensagem}</h1>
        """,
        unsafe_allow_html=True
    )

def subheader(mensagem):
    # Usando HTML para alterar a cor do subheader
    st.markdown(
        f"""
        <h3 style="color: #12239E;">{mensagem}</h3>
        """,
        unsafe_allow_html=True
    )

def marcador_com_cor():
    st.markdown(
        """
    <hr style="border: 1px solid orange;">
    """,
        unsafe_allow_html=True
    )

def carregar_titulo(mensagem):
    col1, col2 = st.columns(2)
    with col1:
        titulo("Paraciclos")
        subheader('Prefeitura do Recife - Dados Abertos')
    with col2:
        st.image('paraciclos.png', width=250)  # Caminho relativo ajustado
    # URL do link
    link_url = "http://dados.recife.pe.gov.br/dataset/paraciclos-do-recife"

    # Exibe o texto com o link
    st.markdown(f'[Clique aqui e siga para os dados abertos]({link_url})')
    marcador_com_cor()


def carregar_dataframe():
    # Carregar o arquivo CSV com o separador correto
    df = pd.read_csv(
        r'C:\Users\Ben-Hur\OneDrive\Documentos\LucianoBorbaCurso\Aula01\paraciclos.csv', sep=';')
    return df


def calcular_total_paraciclos(df):
    totalpontos = df.shape[0]
    return totalpontos

def calcular_total_de_vagas(df):
    total_vagas = df['quantidade'].sum()
    return total_vagas

def substituir_rpa_por_zona(df):
    # Dicionário de mapeamento RPA -> Zona
    mapeamento_rpa_zona = {
        1: 'Centro',
        2: 'Norte',
        3: 'Noroeste',
        4: 'Oeste',
        5: 'Sudeste',
        6: 'Sul'
    }

    # Substituir valores na coluna 'rpa' pela coluna 'zona'
    df['zona'] = df['rpa'].map(mapeamento_rpa_zona)
    return df

def exibir_imagem_e_cartao_com_total_pontos_wifi(total_paraciclos, totalvagas):
    col1, col2 = st.columns(2)
    with col1:
        card_style = """
        <div style="
        border: 1px solid #fff; 
        border-radius: 8px; 
        padding: 10px; 
        background-color: #ff826a; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);
        text-align: center;
        width: 200px;
        margin: auto;
        ">
        <h4 style="color: #fff; margin: 5px 0;">Total de Paraciclos nos Bairros</h4>
        <p style="font-size: 40px; font-weight: bold; margin: 5px 0;">{}</p>
        </div>
        """.format(total_paraciclos)
        st.markdown(card_style, unsafe_allow_html=True)
    
    with col2:
        card_style = """
        <div style="
        border: 1px solid #fff; 
        border-radius: 8px; 
        padding: 10px; 
        background-color: #ff826a; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);
        text-align: center;
        width: 200px;
        margin: auto;
        ">
        <h4 style="color: #fff; margin: 5px 0;">Total de Vagas de Estacionamentos de Bikes</h4>
        <p style="font-size: 40px; font-weight: bold; margin: 5px 0;">{}</p>
        </div>
        """.format(totalvagas)
        st.markdown(card_style, unsafe_allow_html=True)
   
    marcador_com_cor()




def gerar_grafico_de_barras_Bairros(df):
    # Agrupar os dados por bairro e somar as quantidades
    df_bairros = df.groupby('bairro', as_index=False)['quantidade'].sum()

    # Ordenar os bairros pela quantidade em ordem decrescente
    df_bairros = df_bairros.sort_values(by='quantidade', ascending=False)

    subheader('Quantidade de vagas por Bairro')

    # Criar o gráfico com Plotly (grafico de barras horizontais)
    fig = px.bar(
        df_bairros,
        y='bairro',  # Usar o eixo Y para os bairros
        x='quantidade',
        hover_data={'bairro': True, 'quantidade': True},
        labels={'quantidade': 'Quantidade de Paraciclos'}
    )

    # Ajustar o layout do gráfico para permitir rolagem horizontal
    fig.update_layout(
        yaxis=dict(
            categoryorder='total descending',
            automargin=True
        ),
        xaxis=dict(
            title='Quantidade de Paraciclos',
            showgrid=True
        ),
        height=600,  # Altura do gráfico
        margin=dict(l=20, r=20, t=50, b=150),  # Margens ajustadas
        showlegend=False
        
    )

    # Exibir o gráfico com rolagem horizontal
    st.plotly_chart(fig, use_container_width=True )
    


def gerar_grafico_de_barras_Zona(df):

    # inserindo um titulo estilizado
    subheader('Quantidade de vagas por Zona')
    # Agrupar os dados por RPA e somar as quantidades
    df_Zona = df.groupby('zona', as_index=False)['quantidade'].sum()

    # Verificar se o DataFrame está vazio
    if df_Zona.empty:
        st.write("Nenhum dado para exibir no gráfico.")
        return

    # Criar o gráfico com plotly
    fig = px.bar(df_Zona, x='zona', y='quantidade',
                 hover_data={'zona': True, 'quantidade': True})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


def criando_filtros_segmentacao(df):
    # Adicionando estilo CSS personalizado para alterar a cor de fundo da sidebar
    st.markdown(
        """
        <style>
        /* Alterando a cor de fundo da sidebar inteira */
        .css-1d391kg {
            background-color: orange !important;
        }
        .sidebar .sidebar-content {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Filtros")

    # Limpar espaços extras e padronizar os nomes dos bairros
    df['bairro'] = df['bairro'].str.strip().str.upper()

    # Filtro de RPA (Seleção múltipla com pesquisa e "Selecionar todos")
    rpas_disponiveis = sorted(df['rpa'].unique())
    # Adiciona a opção "Selecionar todos"
    rpas_disponiveis_com_todos = ['Selecionar todos'] + rpas_disponiveis

    selected_rpa = st.sidebar.multiselect(
        'Selecione as RPAs:',
        options=rpas_disponiveis_com_todos,
        default=rpas_disponiveis_com_todos,  # Por padrão, seleciona todos
        help="Pesquise e selecione as RPAs desejadas.",
        key="rpa_filter",
    )

    # Se "Selecionar todos" for selecionado, incluir todas as RPAs
    if 'Selecionar todos' in selected_rpa or len(selected_rpa) == 0:
        selected_rpa = rpas_disponiveis

    # Filtrar o DataFrame com base no RPA selecionado
    df_filtrado_por_rpa = df[df['rpa'].isin(selected_rpa)]

    # Filtro de Bairro (Seleção múltipla com pesquisa e "Selecionar todos")
    bairros_disponiveis = sorted(df_filtrado_por_rpa['bairro'].unique())
    # Adiciona a opção "Selecionar todos"
    bairros_disponiveis_com_todos = ['Selecionar todos'] + bairros_disponiveis

    selected_bairro = st.sidebar.multiselect(
        'Selecione os Bairros:',
        options=bairros_disponiveis_com_todos,
        default=bairros_disponiveis_com_todos,  # Por padrão, seleciona todos
        help="Pesquise e selecione os bairros desejados.",
        key="bairro_filter"
    )

    # Se "Selecionar todos" for selecionado, incluir todos os bairros
    if 'Selecionar todos' in selected_bairro or len(selected_bairro) == 0:
        selected_bairro = bairros_disponiveis

    # Aplicar o filtro de Bairro ao DataFrame já filtrado pelas RPAs
    df_filtrado_final = df_filtrado_por_rpa[df_filtrado_por_rpa['bairro'].isin(
        selected_bairro)]

    return df_filtrado_final

def mostra_df(df):
    subheader("Listagem de Paraciclos no Recife")
    st.dataframe(data=df, use_container_width=False, hide_index=None, 
                 column_order=None, column_config=None, key=None, on_select="ignore", selection_mode="multi-row")
    marcador_com_cor()


def exibir_mapas(df):
    subheader("Localização")
    # Remover espaços extras das colunas
    df.columns = df.columns.str.strip()

    # Verificar se as colunas de latitude e longitude estão presentes
    if 'latitude' in df.columns and 'longitude' in df.columns:
        # Criar o mapa com Plotly
        fig = px.scatter_mapbox(df,
                                lat='latitude',
                                lon='longitude',
                                hover_name='local',  # Substitua 'endereco' por 'local' ou a coluna correta
                                # Dados adicionais no tooltip
                                hover_data={'bairro': True,
                                            'rpa': True, 'quantidade': True, 'zona': True},
                                color='quantidade',  # Cor baseada na quantidade de vagas
                                size='quantidade',  # Tamanho dos pontos baseado na quantidade de vagas
                                size_max=15,  # Tamanho máximo dos pontos
                                color_continuous_scale='Viridis'  # Escala de cores
                                
                                )

        # Definir o estilo do mapa e o tamanho
        fig.update_layout(mapbox_style="carto-positron",  # Estilo do mapa
                          mapbox_zoom=12,  # Nível de zoom inicial
                          mapbox_center={"lat": df['latitude'].mean(
                              # Centralizar o mapa
                          ), "lon": df['longitude'].mean()},
                          # Definir a altura do mapa (ajuste conforme necessário)
                          height=800,
                          # Definir a largura do mapa (ajuste conforme necessário)
                          width=1200
                          )
        st.plotly_chart(fig)  # Exibir o gráfico no Streamlit
    else:
        st.write(
            "As colunas de latitude e longitude não estão presentes ou estão incorretas.")

    marcador_com_cor()

    
def main():
    carregar_titulo('Paraciclos')
    df = carregar_dataframe()
    df = substituir_rpa_por_zona(df)

    # Aplicar os filtros interdependentes (RPA → Bairro)
    df_filtered = criando_filtros_segmentacao(df)

    # Calcular total com base no DataFrame filtrado
    totalpontos = calcular_total_paraciclos(df_filtered)
    totalvagas = calcular_total_de_vagas(
        df_filtered)  # Corrigido para usar df_filtered

    # Exibir o cartão e o gráfico com os dados filtrados
    exibir_imagem_e_cartao_com_total_pontos_wifi(totalpontos, totalvagas)
    col1, col2 = st.columns(2)
    with col1:
        gerar_grafico_de_barras_Bairros(df_filtered)
    with col2:
        gerar_grafico_de_barras_Zona(df_filtered)
    marcador_com_cor()
    mostra_df(df_filtered)  # Exibir o DataFrame filtrado
    exibir_mapas(df_filtered)  # Passar o DataFrame filtrado para o mapa e encerrar




if __name__ == "__main__":
    main()
