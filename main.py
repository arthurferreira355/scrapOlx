import pandas as pd
import requests
from bs4 import BeautifulSoup

listaJson = []

def BuscarDadosOlx(pages):
    
    for x in range(0, pages):
        print("LOOP NUMERO" +str(x))
        url = "https://ma.olx.com.br/regiao-de-sao-luis/sao-luis/imoveis/venda"
        if x == 0:
            print("somente primeira página")
        else:
            url = "https://ma.olx.com.br/regiao-de-sao-luis/sao-luis/imoveis/venda"+str(x)

        PARAMS = {
            "authority":"ma.olx.com.br",
            "method":"GET",
            "path":"/regiao-de-sao-luis/sao-luis/imoveis/venda",
            "scheme":"https",
            "referer":"https://ma.olx.com.br/regiao-de-sao-luis/sao-luis/imoveis/venda",
            "sec-fetch-mode":"navigate",
            "sec-fetch-site":"same-origin",
         "sec-fetch-user":"?1",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

        page = requests.get(url=url, headers = PARAMS)
        soup = BeautifulSoup(page.content, 'lxml')
        itens = soup.find_all("li", {"class":"sc-1fcmfeb-2 juiJqh"})
        
        for a in itens:
            try:
                tituloImovel = a.find_all("h2")[0].contents[0]
                precoImovel = a.find_all("p",class_="sc-1iuc9a2-8 bTklot sc-ifAKCX eoKYee")[0].contents[0]
                precoImovel = precoImovel.split("R$")[1]
                precoImovel = float(precoImovel.replace(".",""))
                infoImovel = a.find_all("span", class_="sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb")[0].contents[0]
                locImovel = a.find_all("span", class_="sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf")[0].contents[0]
                cidadeImovel = locImovel.split(",")[0]
                bairroImovel = locImovel.split(",")[1]
                diaPostagem = a.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[0].contents[0]
                horaPostagem = a.find_all("span", class_="wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb")[1].contents[0]
                urlImovel = a.find("a")["href"]

                json = {"dia_postagem":diaPostagem,
                        "hora_postagem":horaPostagem,
                        "titulo_anuncio":tituloImovel,
                        "preco":precoImovel,
                        "infos_imovel":infoImovel,
                        "cidade":cidadeImovel,
                        "bairro":bairroImovel,
                        "url":urlImovel}
                        
                listaJson.append(json)

            except:
                print("erro")

BuscarDadosOlx(100)

df = pd.DataFrame(listaJson)
df.to_excel("imoveisSLZ.xlsx", index=False)