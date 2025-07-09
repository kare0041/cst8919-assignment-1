# Flask Auth0 Authentication App

A simple Flask application that demonstrates authentication using Auth0. The app includes a home page, protected route, and login/logout functionality.

## Features

- Auth0 authentication integration
- Protected routes
- Login/Logout functionality
- Session management
- Enhanced logging for security monitoring

## Prerequisites

- Python 3.x
- Auth0 account
- pip (Python package manager)
- Azure account (for deployment to Azure App Service)

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
     - Allowed Callback URLs: `http://localhost:3000/callback` (and your Azure App Service URL, e.g., `https://<your-app-name>.azurewebsites.net/callback`)
     - Allowed Logout URLs: `http://localhost:3000` (and your Azure App Service URL, e.g., `https://<your-app-name>.azurewebsites.net`)
     - Allowed Web Origins: `http://localhost:3000` (and your Azure App Service URL, e.g., `https://<your-app-name>.azurewebsites.net`)

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
PORT=3000 # Or your desired port
```

Replace the values with your actual Auth0 credentials from your application settings.

### 5. Azure App Service Deployment

1.  **Create an Azure App Service**:
    *   Navigate to the Azure Portal and create a new Web App.
    *   Choose your desired runtime (Python 3.x).
2.  **Deployment Method**:
    *   You can deploy via Git, local Git repository, GitHub Actions, or other methods.
    *   Ensure your `requirements.txt` is in the root directory for Azure to automatically install dependencies.
3.  **Configure Application Settings**:
    *   In your App Service, go to "Configuration" -> "Application settings".
    *   Add the environment variables from your `.env` file (e.g., `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `APP_SECRET_KEY`). Azure App Service uses these as environment variables.
4.  **Startup Command**:
    *   For Python Flask applications, set the startup command under "Configuration" -> "General settings". A common command is `gunicorn --bind 0.0.0.0 --timeout 600 server:app`.

### 6. Run the Application Locally

```bash
python3 server.py
```

The application will be available at `http://localhost:3000`

## Routes

- `/` - Home page
- `/login` - Login page
- `/logout` - Logout
- `/protected` - Protected page (requires authentication)

## Logging and Monitoring

This application includes enhanced logging to monitor user activity and detect potential security incidents. Logs are emitted using Flask's `app.logger` and, when deployed to Azure App Service with `AppServiceConsoleLogs` enabled and configured to send logs to Log Analytics, these logs can be queried and used for alerting.

### Logging Details

-   **User Login**: When a user successfully logs in, the `user_id`, `email`, and a `timestamp` are recorded using `app.logger.info()`.
    *   Detection Logic: This log helps in auditing successful authentication events.
-   **Protected Route Access**: Every time a logged-in user accesses the `/protected` route, their `user_id`, `email`, and a `timestamp` are logged with `app.logger.info()`.
    *   Detection Logic: This is crucial for monitoring access to sensitive areas of the application.
-   **Unauthorized Access Attempts**: If an unauthenticated user tries to access a `@login_required` route (like `/protected`), a warning is logged via `app.logger.warning()` with a `timestamp`.
    *   Detection Logic: This log helps identify attempts to bypass authentication.

### Azure Log Analytics KQL Query for Excessive Access

An Azure Alert has been configured to trigger when any user exceeds 10 accesses to the `/protected` route within a 15-minute window. This helps in detecting suspicious activity, such as brute-force attempts or automated access.

**KQL Query:**

```kusto
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription has "Protected route accessed by user"
| extend 
    user_id = extract(@"user_id=(.*?),", 1, ResultDescription),
    timestamp = extract(@"timestamp=([0-9T:.-]+)", 1, ResultDescription)
| summarize access_count = count(), latest_access = max(TimeGenerated) by user_id
| where access_count > 10
| project user_id, timestamp=latest_access, access_count
```

**Alert Logic:**

This KQL query identifies users who have accessed the protected route more than 10 times in the last 15 minutes. An Azure Monitor Alert can be configured with this query to trigger notifications (e.g., email, SMS, webhook) when the condition is met, enabling proactive security response.

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

## 5-minute YouTube video demo

https://youtu.be/ymvX3PRDJLA