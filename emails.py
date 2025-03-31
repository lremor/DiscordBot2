import requests, os
from dotenv import load_dotenv

# Sua chave de API da Abstract
load_dotenv()
API_KEY = os.getenv('EMAILS_KEY')

def validar_email(email):
    url = f'https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}'
    response = requests.get(url)
    return response.json()

def validar_lista_emails(arquivo):
    try:
        with open(arquivo, 'r') as f:
            emails = f.readlines()

        emails_validos = []  # Lista para armazenar os e-mails válidos

        for email in emails:
            email = email.strip()  # Remove espaços em branco
            resultado = validar_email(email)
            
            if resultado.get('is_valid_format', {}).get('value'):
                print(f'{email} - Válido')
                emails_validos.append(email)  # Adiciona o e-mail válido à lista
            else:
                print(f'{email} - Inválido')
        
        # Salvar e-mails válidos em emails_validos.txt
        with open('emails_validos.txt', 'w') as f_validos:
            for email_valido in emails_validos:
                f_validos.write(email_valido + '\n')
    
    except FileNotFoundError:
        print('Arquivo não encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Chame a função com o nome do arquivo .txt
validar_lista_emails('emails.txt')

