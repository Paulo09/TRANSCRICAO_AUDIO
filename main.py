import re
import os
import pandas as pd


def ler_transcricoes(diretorio):
    transcricoes = []
    for filename in os.listdir(diretorio):
        if filename.endswith(".txt"):
            with open(os.path.join(diretorio, filename), 'r', encoding='utf-8') as file:
                transcricoes.append(file.read())
    return transcricoes

def selecionar_transcricoes_com_protocolo(transcricoes):
    transcricoes_com_protocolo = []
    padrao_protocolo = r'\b\d{8}\d{5}\b'  # Padrão para número de protocolo (13 dígitos)
    
    for transcricao in transcricoes:
        if re.search(padrao_protocolo, transcricao):
            transcricoes_com_protocolo.append(transcricao)
            if len(transcricoes_com_protocolo) >= 5000:
                break
    
    return transcricoes_com_protocolo

def extrair_protocolos(transcricoes_com_protocolo):
    padrao_protocolo = r'\b\d{8}\d{5}\b'
    protocolos = []
    
    for transcricao in transcricoes_com_protocolo:
        match = re.search(padrao_protocolo, transcricao)
        if match:
            protocolos.append(match.group())
    
    return protocolos



def pesquisar_modelos_de_atendimento(protocolos, parquet_path):
    df_parquet = pd.read_parquet(parquet_path)
    modelos_de_atendimento = {}
    
    for protocolo in protocolos:
        resultado = df_parquet[df_parquet['protocolo'] == protocolo]
        if not resultado.empty:
            modelos_de_atendimento[protocolo] = resultado['modelo_atendimento'].values[0]
    
    return modelos_de_atendimento



def automatizar_processo(diretorio_transcricoes, parquet_path):
    transcricoes = ler_transcricoes(diretorio_transcricoes)
    transcricoes_com_protocolo = selecionar_transcricoes_com_protocolo(transcricoes)
    protocolos = extrair_protocolos(transcricoes_com_protocolo)
    modelos_de_atendimento = pesquisar_modelos_de_atendimento(protocolos, parquet_path)
    
    return modelos_de_atendimento

# Exemplo de uso
diretorio_transcricoes = 'caminho/para/diretorio/de/transcricoes'
parquet_path = 'caminho/para/arquivo/parquet.parquet'

resultados = automatizar_processo(diretorio_transcricoes, parquet_path)
print(resultados)