from bs4 import BeautifulSoup
import requests
import pandas as pd

def MV(lista_times):

    teams_df = pd.read_csv("ScrapingBR/teams.csv")
    teams_df = teams_df.drop(["Unnamed: 0", "team_full_name", "team_logo"], axis = 1).set_index("team_name")
    teams_df = teams_df.drop(teams_df[~teams_df.index.isin(lista_times)].index)
                                                
    lista_times = list(teams_df.index)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    market_value = list()
    for time in lista_times:

        endereco_da_pagina = f"https://www.transfermarkt.com{teams_df.loc[time].url}"

        objeto_response = requests.get(endereco_da_pagina, headers=headers)

        pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')

        # times_nome = pagina_bs.find_all("h1", {"itemprop": "name"})
        # for i in times_nome:
        #     nome = i.text.replace("\n", "")
        #     times.append(nome)

        tags_time = pagina_bs.find_all("div", {"class": "dataMarktwert"})

        for i in tags_time:
            valor_mercado = i.text.replace("\n", "").replace("€", "").replace("m Total market value", "")
            market_value.append(valor_mercado)

    VM_df = pd.DataFrame({"Time": lista_times, "MV (Milhoes de Euros)": market_value})

    return VM_df


def MV_completo(lista_times):

    teams_df = pd.read_csv("ScrapingBR/teams.csv")
    teams_df = teams_df.drop(["Unnamed: 0", "team_full_name", "team_logo"], axis = 1).set_index("team_name")
    teams_df = teams_df.drop(teams_df[~teams_df.index.isin(lista_times)].index)
                                                
    lista_times = list(teams_df.index)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    market_value = dict()
    market_value["Time"] = lista_times

    for ano in range (2012, 2022):
        valor_anual = list()
        for time in lista_times:
            
            endereco_da_pagina = f"https://www.transfermarkt.com{teams_df.loc[time].url}/plus/0/galerie/0?saison_id={ano}"

            objeto_response = requests.get(endereco_da_pagina, headers=headers)

            pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')

            tags_time = pagina_bs.find_all("td", {"class": "rechts hauptlink"})
            total = 0
            custo_jog = list()
            for i in tags_time:
                valor_mercado = i.text.replace("\n", "").replace("€", "").replace("m Total market value", "").replace("Th", "").replace("m", "").replace("-", "").replace("\xa0", "")
                if valor_mercado != '':
                    valor_mercado = float(valor_mercado)
                    if valor_mercado < 30:
                        valor_mercado *= 1000
                    custo_jog.append(valor_mercado)
            for i in custo_jog:
                total += i
            total /= 1000
            valor_anual.append(total)
            market_value[f"{ano}"] = valor_anual

    VM_df = pd.DataFrame(market_value)

    return VM_df
