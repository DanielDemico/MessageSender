import requests

# Configurações da API
API_URL = "http://localhost:8080/message/sendText/teste"
API_KEY = "4F35CBC8FE66-41D5-B94C-2E2A3100442D"  # Substitua pela sua chave (gerada no servidor Evolution)

# Dados da mensagem
payload = {
    "number": "5514998629523",  # Número do destinatário (com DDI e DDD, sem "+")
    "text": "Mensagem enviada com python" 
}

# Headers da requisição
headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

# Envia a mensagem
response = requests.post(API_URL, json=payload, headers=headers)

# Verifica a resposta
if response.status_code in [200,201]:
    print("✅ Mensagem enviada com sucesso!")
    print("Resposta:", response.json())
else:
    print("❌ Erro ao enviar mensagem:")
    print("Status Code:", response.status_code)
    print("Detalhes:", response.text)