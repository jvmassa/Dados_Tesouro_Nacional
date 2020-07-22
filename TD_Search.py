# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:55:37 2020

@author: massa
"""

import pandas as pd
import Stats_pack as sp
import plotly.graph_objects as go
import plotly.express as px
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def Base_PT_TD():
    """
    Retona dataframe com os preços de compra/venda e suas respectivas taxas para
    todos dos títulos emitidos pelo Tesouro Nacional
    """
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
    df = pd.read_csv(url, sep = ';', decimal = ',')
    df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], dayfirst = True)
    df['Data Base'] = pd.to_datetime(df['Data Base'], dayfirst = True)
    mult_ind = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(mult_ind).iloc[:,3:]
    
    return df

def Busca_Titulo(titulo, vcto):
    """
    Retona dataframe com os preços de compra/venda e suas respectivas taxas para
    todos dos títulos emitidos pelo Tesouro Nacional
    """
    base = Base_PT_TD()
    base.sort_index(inplace = True)
    titulo = base.loc[(titulo, vcto)]
    titulo['Taxa Compra Manha'] = titulo['Taxa Compra Manha']/100
    titulo['Taxa Venda Manha'] = titulo['Taxa Venda Manha']/100
    return titulo

def Base_Vendas_TD():
    """
    Retorna dataframe com dados relativos às vendas dos títulos emitidos 
    pelo TN
    """
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv'
    df = pd.read_csv(url, sep = ';', decimal = ',')
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], 
      dayfirst = True)
    df['Data Venda'] = pd.to_datetime(df['Data Venda'], dayfirst = True)
    mult_ind = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(mult_ind).iloc[:,3:]
    
    return df

def Busca_Venda_Titulo(titulo, vcto):
    """
    Retorna dataframe com os dados relativos às venas de um determinado titulo 
    """
    base = Base_Vendas_TD()
    base.sort_index(inplace = True)
    titulo = base.loc[(titulo, vcto)]
    return titulo

def Base_Recompra_TD():
    """
    Retorna dataframe com os dados relativos aos títulos entregues pelo
    investidores ao tesouro
    """
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv'
    df = pd.read_csv(url, sep = ';', decimal = ',')
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'],
      dayfirst = True)
    df['Data Resgate'] = pd.to_datetime(df['Data Resgate'],
      dayfirst = True)
    mult_ind = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(mult_ind).iloc[:,3:]
    
    return df

def Busca_Recompra_Titulo(titulo, vcto):
    
    """
    Retorna dataframe com dados relativos a um determinado titulo emitido 
    pelo TN 
    """
    base = Base_Recompra_TD()
    base.sort_index(inplace = True)
    titulo = base.loc[(titulo, vcto)]
    
    return titulo

def Base_Cupom_TD():
    """
    Retorna dataframe que contem infos relativas aos pgtos de juros dos titulos
    emitidos pelo TN
    """
    
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/de2af5cf-9dbd-4566-b933-da6871cce030/download/CupomJurosTesouroDireto.csv'
    df = pd.read_csv(url, sep = ';', decimal = ',')
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'],
      dayfirst = True)
    df['Data Resgate'] = pd.to_datetime(df['Data Resgate'], dayfirst = True)
    mult_ind = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(mult_ind).iloc[:,3:]
    
    return df

def Busca_Cupom_Titulo(titulo, vcto):
    """
    Retorna dataframe com dados relativos a um determinado titulo emitido 
    pelo TN 
    """
    base = Base_Cupom_TD()
    base.sort_index(inplace = True)
    titulo = base.loc[(titulo, vcto)]
    return titulo

def Base_TM_TD():
    """
    Retorna dataframe com infos sobre titulos emitidos pelo TN que foram 
    carregados até o vcto
    """
    url = 'https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/9180ec46-5d73-49ab-bd26-f16e2b323f74/download/VencimentosTesouroDireto.csv'
    df = pd.read_csv(url, sep = ';', decimal = ',')
    df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], 
      dayfirst = True)
    df['Data Resgate'] = pd.to_datetime(df['Data Resgate'], dayfirst = True)
    mult_ind = pd.MultiIndex.from_frame(df.iloc[:,:3])
    df = df.set_index(mult_ind).iloc[:,3:]
    
    return df

def Spread_Titulo(titulo, vcto):
    """
    Retorna um dataframe com o spread, em bps, praticado pelo TN para um determi
    nado titulo
    """
    
    titulo = Busca_Titulo(titulo, vcto)
    #Taxa de captação do título
    cap = titulo['Taxa Compra Manha']
    #Taxa de 'aplicação' do título
    ap = titulo['Taxa Venda Manha']
    spread = ((1+ap)/(1+cap)-1)*100
    spread = spread.dropna()
    return spread

def Painel_NegS_Titulo(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com os totais semanais de vendas, recompras e saldo rea
    lizados pelo TN
    """
    vendas = Busca_Venda_Titulo(titulo,vcto)['Valor']
    recompras = Busca_Recompra_Titulo(titulo, vcto)['Valor']*(-1)
    #bloco das séries semanais:
    vendas_semanais = vendas.resample('1W').sum()
    recompras_semanais = recompras.resample('1W').sum()
    saldo_semanal = vendas_semanais + recompras_semanais    
    df_semanal = pd.DataFrame({'Vendas': vendas_semanais,
                               'Recompras': recompras_semanais,
                               'Saldo': saldo_semanal})
    df_semanal = df_semanal.dropna()
    
    #gráfico semanal
    fig = go.Figure(data = [
            go.Bar(name = 'Vendas', x = df_semanal.index, y = df_semanal['Vendas']),
            go.Bar(name = 'Recompras', x = df_semanal.index, 
                   y = df_semanal['Recompras']),
           go.Bar(name = 'Saldo', x = df_semanal.index, y = df_semanal['Saldo'])],
            layout= dict(title =dict(text = 'Histórico de Negociação Semanal' + 
                        ' ' +str(titulo) + ' ' + str(vcto))))
    fig.update_layout(barmode = 'group')
    
    fig.show()
    
def Painel_NegM_Titulo(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com os totais mensais de vendas, recompras e saldo rea
    lizados pelo TN
    """
    vendas = Busca_Venda_Titulo(titulo,vcto)['Valor']
    recompras = Busca_Recompra_Titulo(titulo, vcto)['Valor']*(-1)
 
    #bloco das séries mensais:
    vendas_mensais = vendas.resample('1M').sum()
    recompras_mensais = recompras.resample('1M').sum()
    saldo_mensal = vendas_mensais + recompras_mensais
    df_mensal = pd.DataFrame({'Vendas': vendas_mensais,
                              'Recompras': recompras_mensais,
                              'Saldo': saldo_mensal})      
        
    #gráfico mensal
    fig = go.Figure(data = [
            go.Bar(name = 'Vendas', x = df_mensal.index[:-1], y = df_mensal['Vendas'][:-1]),
            go.Bar(name = 'Recompras', x = df_mensal.index[:-1],
                   y = df_mensal['Recompras'][:-1]),
           go.Bar(name = 'Saldo', x = df_mensal.index[:-1], y = df_mensal['Saldo'][:-1])],
            layout= dict(title =dict(text = 'Histórico de Negociação Mensal' + 
                                     ' ' +str(titulo) + ' ' + str(vcto))))
    fig.update_layout(barmode = 'group')
    
    fig.show()

def Painel_NegD_Titulo(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com os totais diários de vendas, recompras e saldo rea
    lizados pelo TN
    """
    vendas = Busca_Venda_Titulo(titulo,vcto)['Valor']
    recompras = Busca_Recompra_Titulo(titulo, vcto)['Valor']*(-1)
    saldo = vendas + recompras
    df = pd.DataFrame({'Vendas': vendas,
                       'Recompras': recompras,
                       'Saldo': saldo})
    df = df.dropna()
    fig = go.Figure(data=[
            go.Bar(name = 'Vendas', x = df.index, y = df['Vendas']),
            go.Bar(name = 'Recompras', x = df.index, y = df['Recompras']),
            go.Bar(name = 'Saldo', x = df.index, y = df['Saldo'])],
            layout= dict(title =dict(text = 'Histórico de Negociação Diária' + 
                                     ' ' + str(titulo) + ' ' + str(vcto))))
    fig.update_layout(barmode = 'group')
    
    return fig.show()

def Historico_PU(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com as séries históricas dos preços de compra e venda.
    """
    df = Busca_Titulo(titulo,vcto)[['PU Venda Manha', 'PU Compra Manha']]
    df = df.dropna()
    fig = go.Figure(data = [
            go.Scatter(name = 'PU Compra Manhã', x = df.index,
                       y = df['PU Compra Manha']),
            go.Scatter(name = 'PU Venda Manhã', x = df.index,
                       y = df['PU Venda Manha'])],
                       layout= dict(title =dict(text = 'Histórico de Preços' + ' ' +
                                    str(titulo) + ' ' + str(vcto))))
    fig.show()
    
def Historico_Txs(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com as séries históricas das taxas de compra e venda.
    """
    df = Busca_Titulo(titulo,vcto)[['Taxa Venda Manha', 'Taxa Compra Manha']]
    df = df.dropna()
    fig = go.Figure(data = [
            go.Scatter(name = 'Taxa Compra Manhã', x = df.index,
                       y = df['Taxa Compra Manha']),
            go.Scatter(name = 'Taxa Venda Manhã', x = df.index,
                       y = df['Taxa Venda Manha'])],
                       layout= dict(title =dict(text = 'Histórico de Taxas' + ' ' +
                                    str(titulo) + ' ' + str(vcto))))    
    fig.show()

def Historico_Spread(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com a série histórica do spread.
    """
    df = Spread_Titulo(titulo,vcto)
    fig = go.Figure(data = [
            go.Scatter(x = df.index, y = df)],
            layout= dict(title =dict(text = 'Histórico Spread' + ' ' +
                                    str(titulo) + ' ' + str(vcto))))
    fig.show()
    
def Historico_Vol(titulo, vcto, fator,window = 21):
    """
    Inputs:
    Titulo e data de vencimento
    Window: janela de volatilidade
    Recebe os dados básicos do título e a janela a ser empregada no cálculo da
    volatilidade realizada do ativo e retorna grafico interativo com a série his
    tórica de volatilidade do papel.
    """
    asset = Busca_Titulo(titulo, vcto)[fator]
    rolling = sp.Rolling_Vol(asset, window)
    fig = go.Figure(data = [
            go.Scatter(name = str(window) + 'du', x = rolling.index, y = rolling)],
            layout= dict(title =dict(text = 'Vol. Realizada Yield' + ' ' +
                                    str(titulo) + ' ' + str(vcto))))
    fig.show()
    
def Historico_DD(titulo, vcto):
    """
    Recebe o código e a data de vencimento de um determinado título e retorna 
    gráfico interativo com drawdown do ativo.
    """
    titulo = Busca_Titulo(titulo, vcto)['PU Venda Manha']
    dd = sp.Drawdown(titulo)
    fig = go.Figure(data = [
            go.Scatter(x = dd.index, y = dd)],
            layout = dict(title = dict(text = 'Drawdown' + ' ' + str(titulo) + 
                                       ' ' + str(vcto)
                                       )
        )
    )
    fig.show()