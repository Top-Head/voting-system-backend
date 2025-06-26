# Voting System - API Documentation

## Sumário

- [Admin Endpoints](#admin-endpoints)
- [Voter Endpoints](#voter-endpoints)
- [Endpoints de Consulta](#endpoints-de-consulta)
- [Ranking Endpoints](#ranking-endpoints)
- [Observações Gerais](#observações-gerais)

---

## Admin Endpoints

### 1. Criar Atividade
- **URL**: `/api/admin/create-activity`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "Nome da Atividade",
    "description": "Descrição"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Atividade criada com sucesso!",
    "activity": {
      "id": 1,
      "name": "Nome da Atividade",
      "description": "Descrição",
      "categories": []
    }
  }
  ```

### 2. Fechar Atividade
- **URL**: `/api/admin/close-activity/<int:id>`
- **Method**: PATCH
- **Response**:
  ```json
  {
    "message": "Activity closed successfully"
  }
  ```

### 3. Criar Projeto
- **URL**: `/api/admin/create-project`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "Nome do Projeto",
    "description": "Descrição",
    "activity": 1,
    "category": 1,
    "subcategory": 1,
    "members": [
      {
        "name": "Membro 1",
        "email": "membro1@email.com",
        "classe": "1ª",
        "turma": "A",
        "course": "Informática"
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "message": "Projeto criado com sucesso!",
    "project": {
      "id": 1,
      "name": "Nome do Projeto",
      "description": "Descrição",
      "subcategory": 1,
      "members": [
        {
          "id": 1,
          "name": "Membro 1",
          "email": "membro1@email.com",
          "classe": "1ª",
          "turma": "A",
          "course": "Informática"
        }
      ]
    }
  }
  ```

### 4. Atualizar Projeto
- **URL**: `/api/admin/update-project/<int:id>`
- **Method**: PUT
- **Body**: Igual ao de criação
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Nome Atualizado",
    "description": "Descrição Atualizada",
    "subcategory": 1,
    "members": [
      {
        "id": 1,
        "name": "Membro 1",
        "email": "membro1@email.com"
      }
    ]
  }
  ```

### 5. Autocomplete de Categorias/Subcategorias/Atividades
- **URL**: `/category-autocomplete/`, `/subcategory-autocomplete/`, `/activity-autocomplete/`
- **Method**: GET
- **Query Params**: `q` (busca), `activity` ou `category` (filtro)
- **Response**: Lista filtrada para autocomplete.

---

## Voter Endpoints

### 1. Registrar Votante
- **URL**: `/api/register-voter`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "Nome",
    "email": "voter@email.com",
    "password": "senha"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Voter registered successfully!",
    "voter": {
      "id": 1,
      "name": "Nome",
      "email": "voter@email.com"
    }
  }
  ```

### 2. Login Votante
- **URL**: `/api/login`
- **Method**: POST
- **Body**:
  ```json
  {
    "email": "voter@email.com",
    "password": "senha"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "email": "voter@email.com"
  }
  ```

### 3. Votar em Projeto
- **URL**: `/api/vote-project`
- **Method**: POST
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**:
  ```json
  {
    "category": 1,
    "project": 1
  }
  ```
- **Response**:
  ```json
  {
    "message": "Voted with success!"
  }
  ```

### 4. Votar em Expositor
- **URL**: `/api/vote-expositor`
- **Method**: POST
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**:
  ```json
  {
    "category": 1,
    "member": 1
  }
  ```
- **Response**:
  ```json
  {
    "message": "Voted with success."
  }
  ```

---

## Endpoints de Consulta

### 1. Listar Membros
- **URL**: `/api/get-members`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Membro 1",
      "email": "membro@email.com",
      "classe": "1ª",
      "turma": "A",
      "course": "Informática"
    }
  ]
  ```

### 2. Listar Categorias
- **URL**: `/api/get-categorys`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Categoria 1",
      "is_global": false,
      "subcategory": []
    }
  ]
  ```

### 3. Detalhar Categoria
- **URL**: `/api/get-category/<int:id>`
- **Method**: GET
- **Response**:
  - Se for global:
    ```json
    {
      "id": 1,
      "name": "Categoria Global",
      "is_global": true,
      "stand": {
        "id": 1,
        "name": "Stand",
        "stand_cover": "url"
      }
    }
    ```
  - Se não for global:
    ```json
    {
      "id": 1,
      "name": "Categoria 1",
      "is_global": false,
      "subcategory": []
    }
    ```

### 4. Listar Projetos
- **URL**: `/api/get-projects`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Projeto 1",
      "description": "Descrição",
      "subcategory": 1,
      "members": []
    }
  ]
  ```

### 5. Detalhar Projeto
- **URL**: `/api/get-project/<int:id>`
- **Method**: GET
- **Response**: Igual ao de listagem, mas apenas um objeto.

### 6. Contar Projetos
- **URL**: `/api/count-project`
- **Method**: GET
- **Response**:
  ```json
  {
    "total": 10
  }
  ```

### 7. Contar Categorias
- **URL**: `/api/count-category`
- **Method**: GET
- **Response**:
  ```json
  {
    "total": 5
  }
  ```

### 8. Listar Votos
- **URL**: `/api/get-votes`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "voter": 1,
      "subcategory": 1,
      "project": 1,
      "member": null,
      "created_at": "2025-06-26T23:06:32.907631Z"
    }
  ]
  ```

### 9. Listar Atividades
- **URL**: `/api/get-activities`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Atividade 1",
      "description": "Descrição",
      "categories": []
    }
  ]
  ```

### 10. Detalhar Atividade
- **URL**: `/api/get-activity/<int:id>`
- **Method**: GET
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Atividade 1",
    "description": "Descrição",
    "finished": true,
    "categories": []
  }
  ```

### 11. Listar Subcategorias
- **URL**: `/api/get-subcategories`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Subcategoria",
      "projects": []
    }
  ]
  ```

### 12. Detalhar Subcategoria
- **URL**: `/api/get-subcategory/<int:id>`
- **Method**: GET
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Subcategoria",
    "projects": []
  }
  ```

### 13. Listar membros por categoria
- **URL**: `/api/get-members-by-category/<int:category_id>`
- **Method**: GET
- **Response**: Lista de membros daquela categoria.

---

## Ranking Endpoints

### 1. Ranking de Membros por Categoria
- **URL**: `/api/get-ranking-category/<int:category_id>`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "member_id": 1,
      "name": "Nome do Membro",
      "category_name": "Categoria",
      "votes": 5
    }
  ]
  ```

---

## Observações Gerais

- **Autenticação**: Endpoints de voto exigem JWT no header:  
  `Authorization: Bearer <access_token>`
- **Erros**: Sempre retornam um campo `"error"` com mensagem.
- **Uploads**: Imagens são URLs absolutas.
- **Campos obrigatórios**: Veja exemplos de body.
- **Autocomplete**: Use para selects dinâmicos no admin.
- **Atualize sempre os tokens após login.**

Se precisar de exemplos de erro ou detalhes de