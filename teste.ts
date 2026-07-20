type LoginResposta = {
    access_token: string;
    token_type: string;
}

async function login(email: string, senha: string): Promise<LoginResposta | undefined>  {
    try {
            const resposta = await fetch("http://localhost:8000/usuario/login",{
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: new URLSearchParams({
                    username: email,
                    password: senha
                })
            });
            if (!resposta.ok) {
                throw new Error(`Falaha no login ${resposta.status}`)
            };
            const dados: LoginResposta = await resposta.json()
            console.log("Token:", dados.access_token);
            return dados
    } catch (error) {
        const msg = error instanceof Error ? error.message: String(error)
        console.log("Erro no login", msg);
        return undefined
    };
};