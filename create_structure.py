import os

# Folder 
folders = [
    "app",
    "app/api",
    "app/core",
    "app/services",
    "app/workflows",
    "app/repository",
]

# File 
files = [
    # app root
    "app/__init__.py",
    "app/main.py",

    # config 
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/dependencies.py",

    # API layer
    "app/api/__init__.py",
    "app/api/routes.py",
    "app/api/schemas.py",

    # Services layer
    "app/services/__init__.py",
    "app/services/embedding.py",

    # Workflows layer
    "app/workflows/__init__.py",
    "app/workflows/rag_workflow.py",

    # Repository layer
    "app/repository/__init__.py",
    "app/repository/document_store.py",

    # Root files
    "notes.md",
    "requirements.txt",
]

# Buat folder
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Buat file kosong jika belum ada
for file in files:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            f.write("")

print("Struktur project berhasil dibuat.")
