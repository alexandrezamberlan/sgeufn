// Função que cria o email a partir do sobrenome
function criarEmail(nomeCompleto) {
    var partes = nomeCompleto.split(" ");
    var sobrenome = partes[partes.length - 1];  // Pega o sobrenome
    var email = sobrenome.toLowerCase() + "@ufn.edu.br";  // Concatena com o domínio
    return email;
}

// Função para exibir o email gerado
function gerarEmail() {
    var nomeCompleto = document.getElementById('nomeCompleto').value;
    var email = criarEmail(nomeCompleto); // A função que está em funcoes.js
    document.getElementById('resultadoEmail').textContent = "Email gerado: " + email;
}