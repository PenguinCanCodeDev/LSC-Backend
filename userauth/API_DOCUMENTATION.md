# API Documentation - Django JWT Authentication System

## Base URL
```
http://localhost:8000
```

---

## 1. Home Endpoint

**Endpoint:** `GET /`

**Description:** Test endpoint to verify the server is running.

**Authentication:** Not required

**Request:**
```bash
curl -X GET http://localhost:8000/
```

**Response:**
```json
"Hello world"
```

**Status Code:** `200 OK`

---

## 2. User Registration

**Endpoint:** `POST /api/register/`

**Description:** Create a new user account with campus, faculty, department, and matriculation details.

**Authentication:** Not required (Public endpoint)

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "campus": "Main",
  "faculty": "Engineering",
  "department": "CS",
  "matriculation_number": "MAT123",
  "session": "2024"
}
```

**Field Constraints:**
- `username`: Required, unique, max 150 characters
- `email`: Required, valid email format
- `password`: Required, at least 8 characters recommended
- `campus`: Optional, max 20 characters
- `faculty`: Optional, max 20 characters
- `department`: Optional, max 20 characters
- `matriculation_number`: Optional, max 14 characters
- `session`: Optional, max 5 characters

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "campus": "Main",
  "faculty": "Engineering",
  "department": "CS",
  "matriculation_number": "MAT123",
  "session": "2024"
}
```

**Error Response (400 Bad Request):**
```json
{
  "username": ["A user with that username already exists."],
  "email": ["This field may not be blank."]
}
```

**PowerShell Example:**
```powershell
$body = @{
    username="johndoe"
    email="john@example.com"
    password="securepass123"
    campus="Main"
    faculty="Engineering"
    department="CS"
    matriculation_number="MAT123"
    session="2024"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/register/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response | ConvertTo-Json
```

---

## 3. Obtain JWT Tokens (Login)

**Endpoint:** `POST /api/token/`

**Description:** Authenticate user and obtain access & refresh tokens. Accepts **either username or email** with password.

**Authentication:** Not required (Public endpoint)

**Request Headers:**
```
Content-Type: application/json
```

**Request Body (Option 1 - Username):**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Request Body (Option 2 - Email):**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Unable to log in with provided credentials."
}
```

**PowerShell Example (Login with Email):**
```powershell
$body = @{
    email="john@example.com"
    password="securepass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/token/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$access_token = $response.access
$refresh_token = $response.refresh

Write-Host "Access Token: $access_token"
Write-Host "Refresh Token: $refresh_token"
```

**PowerShell Example (Login with Username):**
```powershell
$body = @{
    username="johndoe"
    password="securepass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/token/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$access_token = $response.access
$refresh_token = $response.refresh
```

**Token Lifetime:**
- **Access Token:** 1 day (24 hours)
- **Refresh Token:** 30 days

---

## 4. Refresh Access Token

**Endpoint:** `POST /api/token/refresh/`

**Description:** Get a new access token using your refresh token.

**Authentication:** Not required

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**PowerShell Example:**
```powershell
$body = @{
    refresh="your_refresh_token_here"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/token/refresh/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$new_access_token = $response.access
Write-Host "New Access Token: $new_access_token"
```

---

## 5. Get Current User Info

**Endpoint:** `GET /my-user-info/`

**Description:** Retrieve information about the currently authenticated user.

**Authentication:** ✓ Required (Bearer Token)

**Request Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "campus": "Main",
  "faculty": "Engineering",
  "department": "CS",
  "matriculation_number": "MAT123",
  "session": "2024"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**PowerShell Example:**
```powershell
$headers = @{
    "Authorization" = "Bearer $access_token"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/my-user-info/" `
    -Method GET `
    -Headers $headers

$response | ConvertTo-Json
```

---

## 6. Protected Route Test

**Endpoint:** `GET /my-protected-endpoint/`

**Description:** Test endpoint that requires authentication.

**Authentication:** ✓ Required (Bearer Token)

**Request Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
"You have been granted access to my protected route"
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**PowerShell Example:**
```powershell
$headers = @{
    "Authorization" = "Bearer $access_token"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/my-protected-endpoint/" `
    -Method GET `
    -Headers $headers

Write-Host $response
```

---

## Authentication Flow

### Step 1: Register a New User
```powershell
POST /api/register/
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  ...
}
```

### Step 2: Authenticate & Get Tokens
You can use either **username** or **email**:

**Option A - With Username:**
```powershell
POST /api/token/
{
  "username": "newuser",
  "password": "password123"
}
```

**Option B - With Email:**
```powershell
POST /api/token/
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Step 3: Use Access Token for Protected Endpoints
```powershell
GET /my-user-info/
Headers: Authorization: Bearer <access_token>
```

### Step 4: Refresh Token When Expired
```powershell
POST /api/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

---

## Error Handling

### Common HTTP Status Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Authenticated but not permitted |
| 404 | Not Found - Endpoint does not exist |
| 500 | Internal Server Error - Server error |

### Example Error Response
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Security Notes

1. **Never share your tokens** - Keep access and refresh tokens private
2. **Use HTTPS in production** - Always use HTTPS instead of HTTP in production
3. **Token expiration** - Access tokens expire after 1 day; use refresh token to get a new one
4. **Password security** - Use strong passwords (at least 12 characters recommended)
5. **Authorization header format** - Always use `Bearer <token>` format

---

## Testing with cURL

### Register User:
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"testpass123",
    "campus":"Main",
    "faculty":"Eng",
    "department":"CS",
    "matriculation_number":"MAT001",
    "session":"2024"
  }'
```

### Get Tokens (with Username):
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "password":"testpass123"
  }'
```

### Get Tokens (with Email):
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"testpass123"
  }'
```

### Use Protected Endpoint:
```bash
curl -X GET http://localhost:8000/my-user-info/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

## Testing with Postman

1. **Set up environment variables:**
   - `base_url`: `http://localhost:8000`
   - `access_token`: (leave blank, will be set by script)
   - `refresh_token`: (leave blank, will be set by script)

2. **Create requests:**
   - POST Register: `{{base_url}}/api/register/`
   - POST Token: `{{base_url}}/api/token/`
   - GET User Info: `{{base_url}}/my-user-info/`
   - Authorization header: `Bearer {{access_token}}`

