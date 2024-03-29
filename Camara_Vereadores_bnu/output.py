import os;
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

def printar_console(data_frame):
    # autor = 'Poder Executivo'
    # print('Totais: ' + autor)
    # print(df[df.Autores == autor].count())
    print('')
    print(data_frame)


def exportar_csv(data_frame):
    data_frame.to_csv('D:\TCC2\exportacao\projetos_camara_vereadores.csv', encoding='utf-8')

def apresentar_grafico_radar(data_frame):
    print('apresentar_grafico_radar')

def salvar_html_pagina(caminho_arquivo, soup):
    salvar_em_arquivos = False;
    if (salvar_em_arquivos):
        os.remove(caminho_arquivo);
        with open(caminho_arquivo, "x", encoding= 'utf-8') as file:
            file.write(str(soup.prettify()))

#salvar arquivo
def salvar_palavras_categoria_arquivo(palavras, caminho_arquivo):
    conteudo_arquivo = '';
    for palavra in palavras:
        conteudo_arquivo += palavra + ';'

    os.remove(caminho_arquivo);
    with open(caminho_arquivo, "x", encoding='utf-8') as file:
        file.write(conteudo_arquivo);

    return 0;

def carregar_palvaras_categoria_arquivo(caminho_arquivo):
    conteudo_arquivo = '';
    with open(caminho_arquivo, "r", encoding='utf-8') as file:
        conteudo_arquivo += file.readlines();

    return conteudo_arquivo.sprint(';');

################################################################################################

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def gerar_grafico_estrela2(autor, qtd_educacao, qtd_seguranca, qtd_saude, qtd_infra, qtd_economia, qtd_outros):
    # Set data
    df = pd.DataFrame({
        'group': [autor, 'Bruno Cunha', 'C', 'D'],
        'Educação': [qtd_educacao, 1.5, 30, 4],
        'Segurança': [qtd_seguranca, 10, 9, 34],
        'Saúde': [qtd_saude, 39, 23, 24],
        'Infra': [qtd_infra, 31, 33, 14],
        'Economia': [qtd_economia, 15, 32, 14],
        'Outros': [qtd_outros, 0,0,0]
    })

    # number of variable
    categories = list(df)[1:]
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = df.loc[0].drop(
        'group').values.flatten().tolist()  # Seleciona qual item do dataframe será apresentado (a,b,c ou d)
    values += values[:1]

    # values2 = df.loc[1].drop(
    #     'group').values.flatten().tolist()  # Seleciona qual item do dataframe será apresentado (a,b,c ou d)
    # values2 += values[:1]

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=8)  # Nome cada item

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([5, 10, 15], ["5", "10", "15"], color="grey", size=7)  # Escala interna
    plt.ylim(0, 40)

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')  # Linha
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)  # Preenchimento

    # # Plot data
    # ax.plot(angles, values2, linewidth=1, linestyle='solid')  # Linha
    # # Fill area
    # ax.fill(angles, values2, 'r', alpha=0.1)  # Preenchimento

    ax.set_title(autor, y=1.08)

    # Show the graph
    plt.show();

def gerar_grafico_estrela(autor, qtd_educacao, qtd_seguranca, qtd_saude, qtd_infra, qtd_economia, qtd_outros):
    N = 6
    theta = radar_factory(N, frame='polygon')

    data = [
        ['Educação', 'Segurança', 'Saúde', 'Infra', 'Economia', 'Outros'],
        (autor, [
            [qtd_educacao, qtd_seguranca, qtd_saude, qtd_infra, qtd_economia, qtd_outros]])

    ]
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b']
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([0, 2, 4, 6, 10, 14])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    #labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    labels = (autor, 'Teste')
    legend = axs[0, 0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')

    fig.text(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()