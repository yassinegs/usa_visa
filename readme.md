# Start venv
python3 -m venv venv

MAC & UNIX: source venv/bin/activate
Windows: venv\Scripts\activate

pip install -r requirements.txt

# Freeze the packages
pip freeze > requirements.txt

# Docker
docker build -t visa_usa .
docker run --name visa_usa_container -d --env-file .env -p 1000:1000 visa_usa