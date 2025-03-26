@echo off
echo Creating Virtual Environment...
python -m venv venv

echo Activating Virtual Environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete! You can now run your project.
pause
