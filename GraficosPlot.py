import seaborn as sns
sns.set(style = "ticks", rc={'axes.facecolor':'white', 'figure.facecolor':'white'})
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def TimesPlot(ano_time_plot, time):
    ano = list()
    ponto_mandante = list()
    ponto_visitante = list()

    def plot_time(time_df, time):
        fig, axes = plt.subplots(figsize = (15, 10))
        sns.lineplot(x = "ano", y = "ponto_mandante", color = "green", data = time_df)
        sns.lineplot(x = "ano", y = "ponto_visitante", color = "red", data = time_df)
        axes.set(xlabel = "Ano", ylabel = "Pontos", title = f"Pontos Ganhos como Mandante dos principais times da Serie A do Brasileirão nos Últimos 10 Anos ({time})")
        plt.xticks(np.arange(min(time_df["ano"]), max(time_df["ano"])+1, 1.0))
        plt.yticks(np.arange(0, max(time_df["ponto_mandante"])+5, 5.0))
        plt.grid()
        plt.show()
        fig.savefig(f"Graficos/{time}.png")

    time_plot = ano_time_plot.drop(ano_time_plot[~ano_time_plot.Time.isin([time])].index)
    lista_anos = list(time_plot["ano"].unique())
    for i in range (2012, 2021):
        if i not in lista_anos:
            ano.append(i)
            ponto_mandante.append(0)
            ponto_visitante.append(0)
    if len(ano) > 0:
        anos_faltantes = {"Time": time, "ano": ano, "ponto_mandante": ponto_mandante, "ponto_visitante": ponto_visitante}
        df_fix = pd.DataFrame(anos_faltantes)
        time_plot = pd.concat([time_plot, df_fix])

    plot_time(time_plot, time)