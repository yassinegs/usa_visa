# Utiliser une image de base officielle Python
FROM python:3.9-slim

# Installer les dépendances pour Chrome
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Commande pour exécuter l'application
CMD ["python", "main.py"]