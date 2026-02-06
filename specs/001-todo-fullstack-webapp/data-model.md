# Data Model: Todo Full-Stack Web Application

## Entity: User

### Fields
- **id**: UUID (Primary Key, Auto-generated)
- **email**: String (Unique, Required, Validated)
- **password_hash**: String (Required, Encrypted)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

### Relationships
- **tasks**: One-to-Many (User has many Tasks)

### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum security requirements
- All required fields must be present

## Entity: Task

### Fields
- **id**: UUID (Primary Key, Auto-generated)
- **title**: String (Required, Max 255 chars)
- **description**: Text (Optional)
- **completed**: Boolean (Default: False)
- **user_id**: UUID (Foreign Key to User.id, Required)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

### Relationships
- **user**: Many-to-One (Task belongs to one User)

### Validation Rules
- Title must be present and non-empty
- Title length must not exceed 255 characters
- User_id must reference an existing User
- Completed status must be boolean value

## Database Schema

### Tables
```
users
├── id (UUID, PK)
├── email (VARCHAR UNIQUE)
├── password_hash (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

tasks
├── id (UUID, PK)
├── title (VARCHAR)
├── description (TEXT)
├── completed (BOOLEAN)
├── user_id (UUID, FK -> users.id)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

### Indexes
- **users.email**: Unique index for fast login lookup
- **tasks.user_id**: Index for efficient ownership queries
- **tasks.completed**: Index for filtering operations
- **tasks.created_at**: Index for sorting operations

## State Transitions

### Task State Transitions
- **Incomplete** ↔ **Complete**: Toggle via PATCH /api/tasks/{id}
- Transition requires valid JWT with matching user_id

## Access Control Rules

### Ownership Requirements
- Users can only access tasks where user_id matches their authenticated user ID
- Unauthorized access attempts return 403 Forbidden
- Invalid JWT tokens return 401 Unauthorized