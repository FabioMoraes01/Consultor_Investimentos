import pandas as pd
import requests
import json
import openai

# Configurar sua chave de API do OpenAI
openai.api_key = 'openaikey'

# Função para gerar mensagens generativas com base nos gostos e saldos
def generate_ai_tips(user):
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um consultor investimentos e dá as melhores sugestões para investir o dinehiro com base nos dólares e euros."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['Nome']} sobre os melhores negócios para investir (máximo de 100 caracteres)"
      }
    ]
  )
    
    return completion.choices[0].message.content.strip('\"')


# Caminho para o arquivo JSON
json_file_path = 'D:\Projetos\Python\Consultor de compras\dados.json'

# Extração dos dados do arquivo JSON usando pandas
data = pd.read_json(json_file_path)
                    
# Obter a lista de IDs dos usuários
user_ids = data['id'].tolist()

# Função para obter um usuário por ID
def get_user(user_id):
    user = data[data['id'] == user_id].iloc[0] if user_id in user_ids else None
    return user

# Obter os usuários usando a função get_user
users = [get_user(user_id) for user_id in user_ids]

# Caminho para os arquivos JSON transformados
transformed_json_file_path = 'dados_transformados.json'

# Itera pelos IDs dos usuários e obtém os dados transformados
users = [get_user(user_id) for user_id in data['id']]


# Atualiza os dados dos usuários com saldos convertidos
for user in users:
    user['Saldo_USD'] = user['Saldo'] * 0.202  # Taxa de conversão de RUB para USD
    user['Saldo_EUR'] = user['Saldo'] * 0.187  # Taxa de conversão de RUB para EUR


# Gera e exibe dicas de comprasinvestimento para cada usuário
for user in users:
    if user is not None and 'Saldo' in user:
        user['Saldo_USD'] = user['Saldo'] * 0.202  # Taxa de conversão de RUB para USD
        user['Saldo_EUR'] = user['Saldo'] * 0.187  # Taxa de conversão de RUB para EUR


for user in users:
    name = user['Nome']
    balance_usd = user['Saldo_USD']
    balance_eur = user['Saldo_EUR']
    

    ai_tips = generate_ai_tips(user)

    print(f"Dados do usuário {name}:\n{user}\n")
    print(f"Dicas de investimentos para {name}:\n{ai_tips}\n")

# Salva os dados transformados em um novo arquivo JSON
pd.DataFrame(users).to_json(transformed_json_file_path, orient='records', indent=4)

