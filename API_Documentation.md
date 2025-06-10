# Vonting System - API Documentation

## Endpoints

### Admin Endpoints

#### 1. Admin Login
- **URL**: `/api/admin/login`
- **Method**: POST
- **Description**: Authenticate an admin user and retrieve a token.
- **Request Body**:
  ```json
  {
    "email": "admin@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "email": "admin@example.com"
  }
  ```

#### 2. Create Activity
- **URL**: `/api/create-activity`
- **Method**: POST
- **Description**: Create a new activity (admin only).
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

#### 3. Update Activity
- **URL**: `/api/update-activity/<int:id>`
- **Method**: PUT
- **Description**: Update an existing activity by ID (admin only).
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

#### 4. Close Activity
- **URL**: `/api/admin/close-activity/<int:id>`
- **Method**: PATCH
- **Description**: Close an activity by ID (admin only).
- **Response**:
  ```json
  {
    "message": "Activity closed successfully"
  }
  ```

#### 5. Create Category
- **URL**: `/api/admin/create-category`
- **Method**: POST
- **Description**: Create a new category (admin only).
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

#### 6. Update Category
- **URL**: `/api/admin/update-category/<int:id>`
- **Method**: PUT
- **Description**: Update an existing category by ID (admin only).
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


#### 7. Create Project
- **URL**: `/api/admin/create-project`
- **Method**: POST
- **Description**: Create a new project (admin only).
- **Request Body**:
  ```json
  {
    "name": "New Project",
    "description": "Project description",
    "category": 1,
    "project_cover": "url_to_image",
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
      "project_cover": "url_to_image",
      "members": [
        {"id": 1, "name": "Member 1", "email": "member1@example.com"}
      ]
    }
  }
  ```

#### 8. Update Project
- **URL**: `/api/admin/update-project/<int:id>`
- **Method**: PUT
- **Description**: Update an existing project by ID (admin only).
- **Request Body**:
  ```json
  {
    "name": "Updated Project",
    "description": "Updated description",
    "category": 1,
    "project_cover": "url_to_image",
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
    "project_cover": "url_to_image",
    "members": [
      {"id": 1, "name": "Member 1", "email": "member1@example.com"}
    ]
  }
  ```

#### 9. Create Member
- **URL**: `/api/cretae-member`
- **Method**: POST
- **Description**: Create a new member.
- **Request Body**:
  ```json
  {
    "name": "Member Name",
    "email": "member@example.com",
    "classe": "Class 1",
    "turma": "IB",
    "profile_image": "url_to_image",
    "course": "Informatica"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Membro criado com sucesso!",
    "member": {
      "id": 1,
      "name": "Member Name",
      "email": "member@example.com",
      "classe": "Class 1",
      "turma": "IB",
      "profile_image": "url_to_image",
      "course": "Informatica"
    }
  }
  ```

#### 10. Category Autocomplete
- **URL**: `/category-autocomplete/`
- **Method**: GET
- **Description**: Autocomplete for categories (admin, used in forms).
- **Query Params**: `activity` (optional), `q` (search string)
- **Response**: Lista de categorias filtradas.

### Voter Endpoints

#### 1. Voter Login
- **URL**: `/api/login`
- **Method**: POST
- **Description**: Authenticate a voter and retrieve a token.
- **Request Body**:
  ```json
  {
    "email": "voter@example.com",
    "google_id": "google123"
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

#### 2. Vote for Project
- **URL**: `/api/vote-project`
- **Method**: POST
- **Description**: Submit a vote for a project.
- **Request Body**:
  ```json
  {
    "voter": 2,
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

#### 3. Vote for Expositor
- **URL**: `/api/vote-expositor`
- **Method**: POST
- **Description**: Submit a vote for an expositor.
- **Request Body**:
  ```json
  {
    "voter": 1,
    "category": 1,
    "member": 1
  }
  ```
- **Response**:
  ```json
  {
    "message": "Voted with sucess."
  }
  ```
### Retrieve Endpoints
#### 1. Get Members
- **URL**: `/api/get-members`
- **Method**: GET
- **Description**: Retrieve a list of members.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Member 1",
      "email": "example@gmail.com",
      "classe": "Class 1",
      "turma": "IB",
      "profile_image": "url_to_image",
      "course": "Informatica"
    }
  ]
  ```

#### 2. Get Categories
- **URL**: `/api/get-categorys`
- **Method**: GET
- **Description**: Retrieve a list of categories.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Category 1",
      "description": "Description 1",
      "projects": []
    }
  ]
  ```

#### 3. Get Category by ID
- **URL**: `/api/get-category/<int:id>`
- **Method**: GET
- **Description**: Retrieve details of a specific category by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Category 1",
    "description": "Description 1",
    "projects": []
  }
  ```

#### 4. Get Projects
- **URL**: `/api/get-projects`
- **Method**: GET
- **Description**: Retrieve a list of projects.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Project 1",
      "description": "Description 1",
      "category": 1,
      "project_cover": "url_to_image",
      "members": []
    }
  ]
  ```

#### 5. Get Project by ID
- **URL**: `/api/get-project/<int:id>`
- **Method**: GET
- **Description**: Retrieve details of a specific project by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Project 1",
    "description": "Description 1",
    "category": 1,
    "project_cover": "url_to_image",
    "members": []
  }
  ```

#### 6. Count Projects
- **URL**: `/api/count-project`
- **Method**: GET
- **Description**: Retrieve the total count of projects.
- **Response**:
  ```json
  {
    "total": 10
  }
  ```

#### 7. Count Categories
- **URL**: `/api/count-category`
- **Method**: GET
- **Description**: Retrieve the total count of categories.
- **Response**:
  ```json
  {
    "total": 5
  }
  ```

#### 8. Get Votes
- **URL**: `/api/get-votes`
- **Method**: GET
- **Description**: Retrieve all votes.
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

#### 9. Get Activities
- **URL**: `/api/get-activities`
- **Method**: GET
- **Description**: Retrieve all activities.
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

#### 10. Get Activity by ID
- **URL**: `/api/get-activity/<int:id>`
- **Method**: GET
- **Description**: Retrieve details of a specific activity by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Activity 1",
    "description": "Description 1",
    "categories": []
  }
  ```

### Ranking Endpoints

#### 1. Get Project Ranking
- **URL**: `/api/ranking/projects/<int:category_id>/`
- **Method**: GET
- **Description**: Retrieve the project ranking by number of votes (descending) for a category.
- **Response**:
  ```json
  [
    {
      "project_id": 1,
      "name": "Project 1",
      "description": "Description 1",
      "category": "Category 1",
      "votes": 3
    }
  ]
  ```

#### 2. Get Members Ranking
- **URL**: `/api/ranking/members/<int:category_id>/`
- **Method**: GET
- **Description**: Retrieve the members ranking by number of votes (descending) for a category.
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
