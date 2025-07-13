# Running the Python Flask Application

This document outlines how to run your Flask application in both development and production environments.

## Development Environment

For local development and testing, use the Flask built-in development server.

**Important:** For development, ensure the `FLASK_ENV` environment variable is set to `development` (not `production`). This enables debugging features and automatic code reloading.

To start the Flask backend server on the default port **5000**:

```bash
export FLASK_ENV=development 
flask --app flasker run --debug
```

This will launch the Python API, typically accessible at [http://localhost:5000](http://localhost:5000).

### Running on a Different Port (Development)

To start the Flask server on a different port (e.g., **5050**) during development:

```bash
export FLASK_ENV=development
flask --app flasker run --debug --port 5050
```

This will launch the API at [http://localhost:5050](http://localhost:5050).

-----

## Production Environment

For production deployments, it is highly recommended to use a robust WSGI server like Gunicorn.

**Important:** For production, ensure the `FLASK_ENV` environment variable is set to `production`. This disables debugging and enables performance optimizations. This variable should be set by your deployment environment (e.g., `systemd`, Docker, cloud provider's console), not in a `.env` file for security.

To start the Flask application with Gunicorn on port **5000** with 4 worker processes:

```bash
# Ensure FLASK_ENV=production is set in your environment (e.g., systemd service file)
gunicorn flasker:app -b 0.0.0.0:5000 -w 4
```

This command will run Gunicorn, binding it to all available network interfaces on port 5000 with 4 worker processes.

### Logging in Production

For better visibility and debugging in production, you can direct Gunicorn's access and error logs to standard output, which can then be captured by a process manager like `systemd` (and viewed with `journalctl`):

```bash
# Ensure FLASK_ENV=production is set in your environment
gunicorn flasker:app -b 0.0.0.0:5000 -w 4 --access-logfile - --error-logfile -
```

This ensures that all API calls and potential errors are logged, making monitoring and troubleshooting much easier.

-----

## Environmental Variables

The following Environmental variable are requirred to run the application either in a .env file during devleopment of system variables on production
```bash
USE_PINATA=true
PINATA_API_KEY=00000000000000000000
PINATA_API_SECRET=0000000000000000000000000000000000000000000000000000000000000000
PINATA_GATEWAY=emerald-added-flea-339.mypinata.cloud
PINATA_JWT=json.web.token

IPFS_HOST_IP=127.0.0.1
IPFS_API_PORT=5001
```