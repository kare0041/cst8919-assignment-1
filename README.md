# Flask Auth0 Authentication App

A simple Flask application that demonstrates authentication using Auth0. The app includes a home page, protected route, and login/logout functionality.

## Features

- Auth0 authentication integration
- Protected routes
- Login/Logout functionality
- Session management

## Prerequisites

- Python 3.x
- Auth0 account
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kare0041/my-app
cd my\ app/
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Auth0 Configuration

1. Log in to your [Auth0 Dashboard](https://manage.auth0.com/)
2. Create a new application:
3. Configure your application settings:
   - In your application settings, add the following URLs:
     - Allowed Callback URLs: `http://localhost:3000/callback`
     - Allowed Logout URLs: `http://localhost:3000`
     - Allowed Web Origins: `http://localhost:3000`

4. Copy your Auth0 credentials:
   - Domain
   - Client ID
   - Client Secret

### 4. Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
APP_SECRET_KEY=your-secret-key
```

Replace the values with your actual Auth0 credentials from your application settings.

### 5. Run the Application

```bash
python3 server.py
```

The application will be available at `http://localhost:3000`

## Routes

- `/` - Home page
- `/login` - Login page
- `/logout` - Logout
- `/protected` - Protected page (requires authentication)

## Dependencies

The application uses the following main dependencies:
- Flask
- Authlib
- python-dotenv

All dependencies are listed in `requirements.txt`

## Security Notes

- Never commit your `.env` file to version control
- Keep your Auth0 credentials secure
- Use a strong APP_SECRET_KEY
- Always use HTTPS in production
