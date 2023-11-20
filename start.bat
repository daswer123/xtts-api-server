@echo off

:: Init virtual venv
python -m venv venv
call venv/Scripts/activate

:: Install requerments
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requerments.txt

python server.py -p 8020