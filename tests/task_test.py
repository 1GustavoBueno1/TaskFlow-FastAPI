def test_tentar_acessar_tarefa_de_outro_user(cliente):
    cliente.post("/usuario/cadastro", json= {
        "nome": "Gustavo",
        "email": "gustavo@gmail.com",
        "senha": "gustavo3010"
    })
    login_1 = cliente.post("/usuario/login", data= {
        "username": "gustavo@gmail.com",
        "password": "gustavo3010"
    })
    token_1 = login_1.json()['access_token']
    header = {"Authorization": f"Bearer {token_1}"}
    tarefa_user_1 = cliente.post("/tarefas/criar", json = {
        "nome": "estudar",
        "descricao": "estudar todo dia"
    }, headers=header)
    id_tarefa_user_1 = tarefa_user_1.json()['id']
    cliente.post("/usuario/cadastro", json= {
        "nome": "pedro",
        "email": "pedro@gmail.com",
        "senha": "pedro3010"
    })
    login_2 = cliente.post("/usuario/login", data={
        "username": "pedro@gmail.com",
        "password": "pedro3010"
    })
    token_2 = login_2.json()["access_token"]
    resposta = cliente.delete(f"/tarefas/deletar_tarefa/{id_tarefa_user_1}", headers={"Authorization": f"Bearer {token_2}"})
    assert resposta.status_code == 404

def test_tentar_acessar_tarefa(cliente):
    cliente.post("/usuario/cadastro", json= {
        "nome": "Gustavo",
        "email": "gustavo@gmail.com",
        "senha": "gustavo3010"
    })
    login_1 = cliente.post("/usuario/login", data= {
        "username": "gustavo@gmail.com",
        "password": "gustavo3010"
    })
    token_1 = login_1.json()['access_token']
    header = {"Authorization": f"Bearer {token_1}"}
    tarefa_user_1 = cliente.post("/tarefas/criar", json = {
        "nome": "estudar",
        "descricao": "estudar todo dia"
    }, headers=header)
    id_tarefa_user_1 = tarefa_user_1.json()['id']
    resposta = cliente.delete(f"/tarefas/deletar_tarefa/{id_tarefa_user_1}", headers=header)
    assert resposta.status_code == 200

def test_marcar_task_concluida(cliente):
    cliente.post(("/usuario/cadastro"), json={
        "nome": "gustavo",
        "email": "gustavo@gmail.com",
        "senha": "gustavo3010"
    })
    user = cliente.post("/usuario/login", data={
        "username": "gustavo@gmail.com",
        "password": "gustavo3010"
    })
    token = user.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    tarefa = cliente.post("/tarefas/criar", json={
        "nome": "estudar",
        "descricao": "todo dia",
    }, headers=header)
    id_tarefa = tarefa.json()['id']
    resposta = cliente.put(f"/tarefas/editar_tarefa/{id_tarefa}", json={
        "status": "concluida"
    }, headers=header)
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "concluida"

