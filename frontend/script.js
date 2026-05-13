const API_URL = "http://127.0.0.1:8000";
let isLogin = true;

function toggleMode() {
    isLogin = !isLogin;
    const title = document.getElementById('form-title')
    const btn = document.getElementById('auth-btn')
    const toggleText = document.getElementById('toggle-text')
    const prefInput = document.getElementById('preferences');

    if (isLogin) {
        title.innerText = "Login";
        btn.innerText = 'Entrar';
        toggleText.innerText = "Não tem conta? Cadastre-se";
        prefInput.style.display = "None";
    } else {
        title.innerText = "Cadastro";
        btn.innerText = "Criar conta";
        toggleText.innerText = "Já tem uma conta? Faça login.";
        prefInput.style.display = "block";
    }
}

async function handleAuth() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const preferences = document.getElementById('preferences').value;

    if(!email || !password) {
        alert("Por favor, preencha todos os campos");
        return;
    }

    try {
        if (isLogin) {
            // LÓGICA DE LOGIN (POST /Token)
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email:email,
                    password:password
                })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token || data.access_token);
                alert("Login realizado com sucesso!");
            } else {
                const errorData = await response.json();
                alert("Erro no login: " + (errorData.detail || "Verifique seus dados"));
            }
        } else {
            // LÓGICA DE CADASTRO (POST /users/)
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: email,
                    password: password,
                    preferences: preferences || "tecnologia"
                })
            });

            if (response.ok) {
                alert("Cadastro realizado! Agora faça o login.");
                toggleMode(); //Volta para a tela de login automaticamente
            } else {
                const errorData = await response.json();
                alert("Erro no cadastro: " + (errorData.detail || "Tente outro e-mail"));
            }
        }
    } catch (error) {
        console.error("Erro na requisição", error);
        alert("Não foi possível conectar ao servidor.");
    }
} 
