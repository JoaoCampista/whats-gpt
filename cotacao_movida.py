import json
import requests
import pandas as pd
from datetime import datetime, timedelta

def requisicao(data):

    data_retirada = data['data_retirada']
    data_devolucao = data['data_devolucao']
    parceiro = data['parceiro']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'portal': 'parcerias',
        'parceiro': parceiro,
        'Content-Type': 'application/json',
        'sentry-trace': 'c47a517034c344518b450a632f66695c-8ceae92341fd5ae4-0',
        'Origin': 'https://parcerias.movida.com.br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://parcerias.movida.com.br/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }

    data = {
        "cnpjparceiro": False,
        "cupom": None,
        "data_retirada": data_retirada,
        "data_devolucao": data_devolucao,
        "local_retirada": "MOVLSSZ",
        "local_devolucao": "MOVLSSZ",
        "simplificado": False,
        "tarifa": None,
        "force-rate-qualifier": True
    }

    response = requests.post('https://apisite.movida.com.br/api/reserva/parceiros/cotacao', headers=headers, json=data)

#    with open('response.json', 'w') as f:
#        json.dump(response.json(), f)
#
#    with open('response.json', encoding='utf-8') as f:
#        dados_json = json.load(f)

    dados_json = response.json()

    return dados_json

def cotacao(dados_json, data):

    cotacao = []

    veiculos = dados_json['VehAvailRSCore']['VehVendorAvails']['VehVendorAvail']['VehAvails']

    for n in range(len(veiculos)):
        grupo = veiculos[n]['VehAvail']['VehAvailCore']['Vehicle']['Description']
        modelos = veiculos[n]['VehAvail']['VehAvailCore']['Vehicle']['VehMakeModel']['Name']
        status = veiculos[n]['VehAvail']['VehAvailCore']['Status']
        taxas = veiculos[n]['VehAvail']['VehAvailCore']['RentalRate']['VehicleCharges']
        coberturas = veiculos[n]['VehAvail']['VehAvailCore']['VehAvailInfo']['PricedCoverages']
        
        for i in range(len(taxas)):

            # SE A TAXA FOR REFERENTE A DIÁRIA
            if taxas[i]['VehicleCharge']['Purpose'] == '1':
                diaria = float(taxas[i]['VehicleCharge']['Calculation']['UnitCharge'])
            
            # SE FOR REFERENTE A TAXA ADMINISTRATIVA
            if taxas[i]['VehicleCharge']['Purpose'] == '83':
                tad = float(taxas[i]['VehicleCharge']['Amount'])

        for j in range(len(coberturas)):

            # SE A COBERTURA FOR DO TIPO BÁSICA
            if coberturas[j]['PricedCoverage']['Coverage']['CoverageType'] == 79:

                cobertura = float(coberturas[j]['PricedCoverage']['Charge']['Amount'])

        total = float(veiculos[n]['VehAvail']['VehAvailCore']['TotalCharge']['PrePagamento']['TotalComDesconto'])

        output = {
            'grupo':grupo,
            'diaria':diaria,
            'taxa':tad,
            'cobertura':cobertura,
            'total':total,
            'data':data
        }

        cotacao.append(output)

    return cotacao 

def cotacao_movida(start, end):
    
    data_inicial = datetime.strptime(start, '%d/%m/%Y %H:%M')
    data_final = datetime.strptime(end, '%d/%m/%Y %H:%M')
    diferenca = data_final - data_inicial
    lista_datas = [data_inicial + timedelta(days=i) for i in range(diferenca.days + 1)]

    cotacoes = []
    
    #for dia in lista_datas:

    #data_inicial = dia.strftime('%d/%m/%Y %H:%M')

    #delta = timedelta(days=1)

    #data_final = dia + delta
    #data_final = data_final.strftime('%d/%m/%Y %H:%M')

    print(data_inicial)

    inputs = {
        'parceiro':'visa',
        'data_retirada': start,
        'data_devolucao': end
    }

    response = requisicao(inputs)
    cotado = pd.DataFrame(cotacao(response, f"{data_inicial} - {data_final}"))

    cotacoes.append(cotado)

    df = pd.concat(cotacoes)
    dados_pivot = df.pivot(index='grupo', columns='data', values='total').reset_index()

    return dados_pivot