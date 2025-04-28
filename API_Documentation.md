# API Documentation

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
    "password": "password123",
    "secret_code": "CODE"
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

#### 2. Create Category
- **URL**: `/api/admin/create-category`
- **Method**: POST
- **Description**: Create a new category.
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
      "description": "Description of the category"
    }
  }
  ```

#### 3. Update Category
- **URL**: `/api/admin/update-category/<int:id>`
- **Method**: PUT
- **Description**: Update an existing category by ID.
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
    "description": "Updated description"
  }
  ```

#### 4. Close Category
- **URL**: `/api/admin/close-category/<int:id>`
- **Method**: DELETE
- **Description**: Close a category by ID.
- **Response**:
  ```json
  {
    "message": "Category closed successfully"
  }
  ```

#### 5. Create Project
- **URL**: `/api/admin/create-project`
- **Method**: POST
- **Description**: Create a new project.
- **Request Body**:
  ```json
  {
    "name": "New Project",
    "description": "Project description",
    "category_id": 1
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
      "category_id": 1
    }
  }
  ```

#### 6. Update Project
- **URL**: `/api/admin/update-project/<int:id>`
- **Method**: PUT
- **Description**: Update an existing project by ID.
- **Request Body**:
  ```json
  {
    "name": "Updated Project",
    "description": "Updated description"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Project",
    "description": "Updated description"
  }
  ```

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
    "voter_id": 2,
    "category": 1,
    "project": 1
  }
  ```
- **Response**:
  ```json
  {
    "message": "Voted with sucess!"
  }
  ```

#### 3. Vote for Expositor
- **URL**: `/api/vote-expositor`
- **Method**: POST
- **Description**: Submit a vote for an expositor.
- **Request Body**:
  ```json
  {
    "voter_id": 1,
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

#### 4. Get Members
- **URL**: `/api/get-members`
- **Method**: GET
- **Description**: Retrieve a list of members.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Member 1",
      "profile_image": "url_to_image"
    },
    {
      "id": 2,
      "name": "Member 2",
      "profile_image": "url_to_image"
    }
  ]
  ```

#### 5. Get Categories
- **URL**: `/api/get-categorys`
- **Method**: GET
- **Description**: Retrieve a list of categories.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Category 1",
      "description": "Description 1"
    },
    {
      "id": 2,
      "name": "Category 2",
      "description": "Description 2"
    }
  ]
  ```

#### 6. Get Category by ID
- **URL**: `/api/get-category/<int:id>`
- **Method**: GET
- **Description**: Retrieve details of a specific category by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Category 1",
    "description": "Description 1"
  }
  ```

#### 7. Get Projects
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
      "category_id": 1
    },
    {
      "id": 2,
      "name": "Project 2",
      "description": "Description 2",
      "category_id": 2
    }
  ]
  ```

#### 8. Get Project by ID
- **URL**: `/api/get-project/<int:id>`
- **Method**: GET
- **Description**: Retrieve details of a specific project by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Project 1",
    "description": "Description 1",
    "category_id": 1
  }
  ```

#### 9. Count Projects
- **URL**: `/api/count-project`
- **Method**: GET
- **Description**: Retrieve the total count of projects.
- **Response**:
  ```json
  {
    "total": 10
  }
  ```

#### 10. Count Categories
- **URL**: `/api/count-category`
- **Method**: GET
- **Description**: Retrieve the total count of categories.
- **Response**:
  ```json
  {
    "total": 5
  }
  ```

#### 11. Get Votes
- **URL**: `/api/get-votes`
- **Method**: GET
- **Description**: Retrieve all votes
- **Response**:
  ```json
  {
    "id": 1,
    "vote_type": "project",
    "created_at": "2025-04-27T23:06:32.907631Z",
    "voter": 1,
    "category": 1,
    "project": 1,
    "member": null
  }