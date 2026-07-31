# Archivos que NO deben ser subidos a Git

# Archivos de entorno con claves secretas
.env
.env.local
.env.*.local

# Datos sensibles
data/
logs/
*.log
*.sqlite
*.db

# Dependencias del proyecto
venv/
env/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE y editor
.vscode/
.idea/
*.swp
*.swo
*~

# Sistema operativo
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
.dockerignore

# Build
build/
dist/
*.egg-info/

# Documentación generada
docs/_build/

# Archivos temporales
tmp/
temp/
*.tmp
*.temp