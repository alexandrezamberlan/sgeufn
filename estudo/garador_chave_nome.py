import hashlib
import secrets

def gerar_chave(nome):
    # Gera um valor aleatório seguro
    aleatorio = secrets.token_hex(8)  # 16 caracteres hex (8 bytes)
    
    # Concatena o nome com o valor aleatório
    base = nome + aleatorio
    
    # Cria um hash SHA-256 da base
    hash_resultado = hashlib.sha256(base.encode()).hexdigest()
    
    # Retorna os primeiros 16 caracteres do hash
    return hash_resultado[:16]

# Exemplo de uso
email = "silva@ufn.edu.br" #437036245df38780
evento = "1a semana da informática ufn"
chave = gerar_chave(email + evento) #328d057eb769da8c
print(chave)