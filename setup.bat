@echo off
echo Please wait. This may take several minutes...
c:\Python35\python -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
deactivate