# Dev Container for Verbroken-Verbinding-Test

This folder configures VS Code to open the workspace inside your existing Docker Compose `streamlit` service so the editor and language servers (Pylance / IntelliSense / Intellicode) can see installed packages (Streamlit, Transformers, etc.).

What it does
- Uses the repository `docker-compose.yml` service `streamlit` to run the dev container.
- Installs VS Code extensions: Python, Pylance, Intellicode.
- Runs `pip install -r requirements.txt` after the container is created so imports are visible to the language server.

How to use (VS Code)
1. In VS Code, open this folder.
2. Open the Command Palette (Ctrl+Shift+P) and choose: **Remote-Containers: Reopen in Container** (or **Dev Containers: Reopen in Container**).
3. Wait while the container is built and extensions installed. After the container is ready, VS Code will reopen inside it.

Quick terminal steps (PowerShell)
Note: these are optional. Reopening in container from VS Code is recommended.

```powershell
# Build the image with docker-compose (optional, VS Code will build automatically):
docker compose build streamlit

# Start the service in detached mode (if you want the app to be running outside VS Code):
docker compose up -d streamlit

# To open a shell inside the running service (for quick checks):
docker compose exec streamlit bash
```

Verify inside container
1. Once inside the container shell or the VS Code terminal (which will run in-container), run:

```powershell
python -c "import streamlit, transformers; print('streamlit', streamlit.__version__, 'transformers', transformers.__version__)"
```

If that prints versions without ImportError, Pylance/IntelliSense inside the container should also work and provide completions for `streamlit` and `transformers`.

Notes
- If you want a non-root user, or a different Python path, edit `devcontainer.json` accordingly.
- The devcontainer uses the project bind-mount so changes you make in VS Code are reflected immediately in the container.
