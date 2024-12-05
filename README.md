# Cinema FastAPI 2.0.0

## Sobre o Projeto

Esta API foi desenvolvida para gerenciar operações de cinema de forma simples e eficiente. Ela inclui funcionalidades para gerenciar clientes, administradores, filmes, salas, sessões e ingressos. É ideal para aplicações de gestão de cinemas de pequeno e médio porte.

---

## Funcionalidades Principais
- **Gerenciamento de Clientes**: Registro, autenticação, atualização e exclusão.
- **Administração**: Registro, autenticação e gerenciamento de administradores.
- **Filmes**: Adição, edição e exclusão de filmes.
- **Salas**: Gerenciamento de salas de cinema.
- **Sessões**: Criação e gerenciamento de sessões de filmes.
- **Ingressos**: Compra, atualização e consulta de ingressos.

---

## Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior
- Gerenciador de pacotes `pip`
- Docker

### Passos para Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/Wesley00s/cinema-fastapi.git
    cd cinema-fastapi
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate     # Para Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
    
4. Exexute o arquivo `docker-compose.yaml` para criar o container do PostgreSQL:
   ```bash
   docker compose up -d --build
   ```

5. Execute a aplicação:
    ```bash
    uvicorn app.main:app --reload
    ```

A API estará disponível em [http://localhost:8000](http://localhost:8000). Ao acessar esse endereço se você ver essa mensagem, deu tudo certo:
```json
{
    'status': 'success',
    'message': 'Cinema API say hello 👋'
}
```

---

## Testando as Rotas com Postman

### Importando a Coleção

1. Abra o Postman.
2. Acesse esse link [postman](https://www.postman.com/material-meteorologist-76512622/academic/collection/yu9wawr/cinema-fastapi?action=share&creator=32579915) para acessar a coleção no postman.
3. Após acessar, você verá as rotas organizadas por categoria: Clientes, Administradores, Filmes, Salas, Sessões e Ingressos.

### Configurando o Ambiente

Certifique-se de configurar a variável `url` no Postman para `http://localhost:8000`.

---

## Exemplos de Requisições

### Autenticar Cliente
**Endpoint**: `POST /customer/auth`

**Exemplo de corpo da requisição**:
```json
{
  "email": "jane.smith@example.co.uk",
  "password": "mypassword456"
}
```

### Registrar Filme
**Endpoint**: `POST /movie`

**Exemplo de corpo da requisição**:
```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "synopsis": "Um ladrão é contratado para plantar uma ideia no subconsciente de um alvo.",
  "duration": 148,
  "age_rating": "PG-13",
  "director": "Christopher Nolan",
  "release_date": "2010-07-26"
}
```
> Para mais detalhes sobre as rotas, use a coleção no Postman ou acesse a documentação interativa disponível em http://localhost:8000/docs.
