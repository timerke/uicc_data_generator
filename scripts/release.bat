cd ..
set PYTHON=python
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist release rd /S /Q release
if exist venv rd /S /Q venv

%PYTHON% -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python -m pip install pyinstaller
venv\Scripts\pyinstaller run.py --clean --onefile ^
--add-data "uiccgenerator\apdu.json;uiccgenerator" ^
--icon "img\icon.ico"

copy README.md dist
rename dist release
cd release
rename run.exe uicc_generator.exe
cd ..
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist venv rd /S /Q venv
if exist *.spec del *.spec
pause