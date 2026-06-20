def test_resposta_server(cliente):
    reposta = cliente.get("/usuario/perfil")
    assert reposta.status_code == 401

def test_cadastro(cliente):
    resposta = cliente.post("/usuario/cadastro", json={
        "nome": "Gustavo",
        "email": "gustavo@gmail.com",
        "senha": "gustavo3010"
    })
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados['email'] == "gustavo@gmail.com"
    assert "senha" not in dados

def test_login_sucesso(cliente):
    cliente.post("/usuario/cadastro", json={
        "nome": "Gustavo", "email": "gustavo@gmail.com", "senha": "gustavo3010"})
    resposta = cliente.post("/usuario/login", data={
        "username": "gustavo@gmail.com",
        "password": "gustavo3010"
    })
    assert resposta.status_code == 200
    assert "access_token" in resposta.json()
def test_login_erro(cliente):
    cliente.post("/usuario/cadastro", json={
        "nome": "Gustavo", "email": "gustavo@gmail.com", "senha": "gustavo3010"})
    resposta = cliente.post("/usuario/login", data = {
        "username": "gustavo@gmail.com",
        "password": "senha_errada"
    })
    assert resposta.status_code == 401
def test_login_inexistente(cliente):
    resposta = cliente.post("/usuario/login", data = {
        "username": "pedro@naoexiste.com",
        "password": "naoexitse"
    })
    assert resposta.status_code == 401