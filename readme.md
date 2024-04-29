# Start venv
python3 -m venv venv

MAC & UNIX: source venv/bin/activate
Windows: venv\Scripts\activate

pip install -r requirements.txt

# Freeze the packages
pip freeze > requirements.txt
