# Voting System - API Documentation

## Sumário

- [Admin Endpoints](#admin-endpoints)
- [Voter Endpoints](#voter-endpoints)
- [Endpoints de Consulta](#endpoints-de-consulta)
- [Ranking Endpoints](#ranking-endpoints)

---

## Admin Endpoints

### 1. Create Activity
- **URL**: `/api/admin/create-activity`
- **Method**: POST
- **Descrição**: Cria uma nova atividade.
- **Request Body**:
  ```json
  {
    "name": "Activity Name",
    "description": "Activity description"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Atividade criada com sucesso!",
    "activity": {
      "id": 1,
      "name": "Activity Name",
      "description": "Activity description",
      "categories": []
    }
  }
  ```

### 2. Update Activity
- **URL**: `/api/update-activity/<int:id>`
- **Method**: PUT
- **Descrição**: Atualiza uma atividade existente.
- **Request Body**:
  ```json
  {
    "name": "Updated Activity",
    "description": "Updated description"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Activity",
    "description": "Updated description",
    "categories": []
  }
  ```

### 3. Close Activity
- **URL**: `/api/admin/close-activity/<int:id>`
- **Method**: PATCH
- **Descrição**: Fecha uma atividade.
- **Response**:
  ```json
  {
    "message": "Activity closed successfully"
  }
  ```

### 4. Create Category
- **URL**: `/api/admin/create-category`
- **Method**: POST
- **Descrição**: Cria uma nova categoria.
- **Request Body**:
  ```json
  {
    "name": "New Category",
    "description": "Description of the category"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Categoria criada com sucesso!",
    "category": {
      "id": 1,
      "name": "New Category",
      "description": "Description of the category",
      "projects": []
    }
  }
  ```

### 5. Update Category
- **URL**: `/api/admin/update-category/<int:id>`
- **Method**: PUT
- **Descrição**: Atualiza uma categoria existente.
- **Request Body**:
  ```json
  {
    "name": "Updated Category",
    "description": "Updated description"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Category",
    "description": "Updated description",
    "projects": []
  }
  ```

### 6. Create Project
- **URL**: `/api/admin/create-project`
- **Method**: POST
- **Descrição**: Cria um novo projeto.
- **Request Body**:
  ```json
  {
    "name": "New Project",
    "description": "Project description",
    "category": 1,
    "members": [
      {"name": "Member 1", "email": "member1@example.com"}
    ]
  }
  ```
- **Response**:
  ```json
  {
    "message": "Projeto criado com sucesso!",
    "project": {
      "id": 1,
      "name": "New Project",
      "description": "Project description",
      "category": 1,
      "members": [
        {"id": 1, "name": "Member 1", "email": "member1@example.com"}
      ]
    }
  }
  ```

### 7. Update Project
- **URL**: `/api/admin/update-project/<int:id>`
- **Method**: PUT
- **Descrição**: Atualiza um projeto existente.
- **Request Body**:
  ```json
  {
    "name": "Updated Project",
    "description": "Updated description",
    "category": 1,
    "members": [
      {"name": "Member 1", "email": "member1@example.com"}
    ]
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Project",
    "description": "Updated description",
    "category": 1,
    "members": [
      {"id": 1, "name": "Member 1", "email": "member1@example.com"}
    ]

  }
  ```

### 8. Category Autocomplete
- **URL**: `/category-autocomplete/`
- **Method**: GET
- **Descrição**: Autocomplete de categorias (admin, usado em formulários).
- **Query Params**: `activity` (opcional), `q` (busca)
- **Response**: Lista de categorias filtradas.

---

## Voter Endpoints

### 1. Register Voter
- **URL**: `/api/register-voter`
- **Method**: POST
- **Descrição**: Registra um novo votante.
- **Request Body**:
  ```json
  {
    "name": "Nome",
    "email": "voter@example.com",
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
      "email": "voter@example.com"
    }
  }
  ```

### 2. Voter Login
- **URL**: `/api/login`
- **Method**: POST
- **Descrição**: Autentica o votante e retorna o token JWT.
- **Request Body**:
  ```json
  {
    "email": "voter@example.com",
    "password": "senha"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "email": "voter@example.com"
  }
  ```

### 3. Vote for Project
- **URL**: `/api/vote-project`
- **Method**: POST
- **Descrição**: Votar em um projeto.
- **Request Body**:
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

### 4. Vote for Expositor
- **URL**: `/api/vote-expositor`
- **Method**: POST
- **Descrição**: Votar em um expositor.
- **Request Body**:
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

### 1. Get Members
- **URL**: `/api/get-members`
- **Method**: GET
- **Descrição**: Lista todos os membros.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Member 1",
      "email": "example@gmail.com"
    }
  ]
  ```

### 2. Get Categories
- **URL**: `/api/get-categorys`
- **Method**: GET
- **Descrição**: Lista todas as categorias.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Category 1",
      "projects": []
    }
  ]
  ```

### 3. Get Category by ID
- **URL**: `/api/get-category/<int:id>`
- **Method**: GET
- **Descrição**: Detalhes de uma categoria.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Category 1",
    "projects": []
  }
  ```

### 4. Get Projects
- **URL**: `/api/get-projects`
- **Method**: GET
- **Descrição**: Lista todos os projetos.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Project 1",
      "description": "Description 1",
      "category": 1,
      "members": []
    }
  ]
  ```

### 5. Get Project by ID
- **URL**: `/api/get-project/<int:id>`
- **Method**: GET
- **Descrição**: Detalhes de um projeto.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Project 1",
    "description": "Description 1",
    "category": 1,
    "members": []
  }
  ```

### 6. Count Projects
- **URL**: `/api/count-project`
- **Method**: GET
- **Descrição**: Total de projetos.
- **Response**:
  ```json
  {
    "total": 10
  }
  ```

### 7. Count Categories
- **URL**: `/api/count-category`
- **Method**: GET
- **Descrição**: Total de categorias.
- **Response**:
  ```json
  {
    "total": 5
  }
  ```

### 8. Get Votes
- **URL**: `/api/get-votes`
- **Method**: GET
- **Descrição**: Lista todos os votos.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "vote_type": "project",
      "created_at": "2025-04-27T23:06:32.907631Z",
      "voter": 1,
      "category": 1,
      "project": 1,
      "member": null
    }
  ]
  ```

### 9. Get Activities
- **URL**: `/api/get-activities`
- **Method**: GET
- **Descrição**: Lista todas as atividades.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Activity 1",
      "description": "Description 1",
      "categories": []
    }
  ]
  ```

### 10. Get Activity by ID
- **URL**: `/api/get-activity/<int:id>`
- **Method**: GET
- **Descrição**: Detalhes de uma atividade.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Activity 1",
    "description": "Description 1",
    "categories": []
  }
  ```

---

## Ranking Endpoints

### 1. Get Project Ranking
- **URL**: `/api/ranking/projects/<int:category_id>/`
- **Method**: GET
- **Descrição**: Ranking de projetos por votos na categoria.
- **Response**:
  ```json
  [
    {
      "project_id": 1,
      "name": "Project 1",
      "description": "Description 1",
      "category_name": "Category 1",
      "votes": 3
    }
  ]
  ```

### 2. Get Members Ranking
- **URL**: `/api/ranking/members/<int:category_id>/`
- **Method**: GET
- **Descrição**: Ranking de membros por votos na categoria.
- **Response**:
  ```json
  [
    {
      "member_id": 5,
      "name": "Name 2",
      "category_name": "Category 1",
      "votes": 3
    }
  ]
  ```

---

**Observações:**
- Para endpoints protegidos, envie o token JWT no header `Authorization: Bearer <access_token>`.
- Em caso de erro, a resposta conterá um campo `"error"`