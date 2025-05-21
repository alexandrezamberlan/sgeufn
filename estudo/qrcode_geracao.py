import qrcode

# String que você quer transformar em QR code
data = "http://127.0.0.1:8000/frequencia/cad/"

# Criação do QR Code
qr = qrcode.QRCode(
    version=1,  # Tamanho do QR Code (1 é o menor)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nível de correção de erro
    box_size=10,  # Tamanho da caixa do QR code
    border=4,  # Largura da borda
)

qr.add_data(data)  # Adiciona os dados (string)
qr.make(fit=True)

# Criação da imagem
img = qr.make_image(fill='black', back_color='white')

# Salvar a imagem em um arquivo
#img.save("qrcode.png")

# Ou mostrar a imagem diretamente
img.show()
