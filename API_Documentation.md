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
- **URL**: `/api/create-activity`
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
    "activity": 1,
    "category": 1,
    "subcategory": 1,
    "members": [
      {
        "name": "Membro 1",
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
      "subcategory": 1,
      "members": [
        {
          "id": 1,
          "name": "Membro 1",
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
    "subcategory": 1,
    "members": [
      {
        "id": 1,
        "name": "Membro 1"
      }
    ]
  }
  ```

### 5. Criar Subcategoria
- **URL**: `/api/create-subcategory`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "Subcategoria",
    "category": 1,
    "activity": 1
  }
  ```
- **Response**:
  ```json
  {
    "message": "Subcategoria criada com sucesso!",
    "subcategory": {
      "id": 1,
      "name": "Subcategoria",
      "projects": []
    }
  }
  ```

### 6. Autocomplete de Categorias/Subcategorias/Atividades
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

### 3. Votar
- **URL**: `/api/vote`
- **Method**: POST
- **Headers**: `Authorization: Bearer <access_token>`
- **Body** (exemplo para projeto):
  ```json
  {
    "category_id": 1,
    "category_type": "project",
    "subcategory_id": 1,
    "activity_id": 1,
    "item_id": 1
  }
  ```
- **Response**:
  ```json
  {
    "msg": "Voted with sucess"
  }
  ```
- **Obs:** Para votar em membro ou stand, altere `category_type` e `item_id` conforme o tipo.

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
      "classe": "1ª",
      "turma": "A",
      "course": "Informática"
    }
  ]
  ```

### 2. Detalhar Membro
- **URL**: `/api/get-member/<int:id>`
- **Method**: GET
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Membro 1",
    "classe": "1ª",
    "turma": "A",
    "course": "Informática"
  }
  ```

### 3. Listar Categorias
- **URL**: `/api/get-categorys`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Categoria 1",
      "category_type": "project",
      "subcategories": []
    }
  ]
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
      "description": "Descrição"
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
    "finished": true
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

### 14. Listar itens de categoria para votação
- **URL**: `/api/get-category-items`
- **Method**: GET
- **Query Params**: `cat_id`, `subcat_id`, `cat_tp`, `act_id`
- **Response**: Lista de itens (projetos, membros ou stands) para votação, com status se o usuário já votou.

---

## Ranking Endpoints

### 1. Ranking Geral por Atividade
- **URL**: `/api/get-rankings/<int:activity_id>`
- **Method**: GET
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  [
    {
      "category": "Categoria",
      "subcategory": "Subcategoria",
      "category_type": "project",
      "ranking": [
        {
          "id": 1,
          "name": "Projeto 1",
          "total_votes": 5
        }
      ]
    }
  ]
  ```

### 2. Ranking Público por Atividade
- **URL**: `/api/public-rankings/<int:activity_id>`
- **Method**: GET
- **Response**: Igual ao ranking geral, mas sem autenticação.

### 3. Ranking de Projetos por Subcategoria
- **URL**: `/api/subcategoryProjectsRanking/<int:subcategory_id>/`
- **Method**: GET
- **Response**:
  ```json
  [
    {
      "project_id": 1,
      "name": "Projeto 1",
      "description": "Descrição",
      "subcategory_name": "Subcategoria",
      "category_name": "Categoria",
      "votes": 10,
      "members": [
        {
          "name": "Membro 1",
          "classe": "1ª",
          "turma": "A"
        }
      ]
    }
  ]
  ```

---

## Observações Gerais

- **Autenticação**: Endpoints de voto e rankings privados exigem JWT no header:  
  `Authorization: Bearer <access_token>`
- **Erros**: Sempre retornam um campo `"error"` com mensagem.
- **Uploads**: Imagens são URLs absolutas.
- **Campos obrigatórios**: Veja exemplos de body.
- **Autocomplete**: Use para selects dinâmicos no admin.
- **Atualize sempre os tokens após login.**

---