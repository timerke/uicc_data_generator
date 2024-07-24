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
venv\Scripts\pyinstaller run_server.py --clean --onefile ^
--add-data "gcodebin\gcodebin.json;gcodebin" ^
--add-data "http_server\static\css\*;http_server\static\css" ^
--add-data "http_server\static\img\*;http_server\static\img" ^
--add-data "http_server\static\js\*;http_server\static\js" ^
--add-data "http_server\views\*;http_server\views" ^
--icon "http_server\static\img\favicon.ico"

copy config.ini dist
copy README_RELEASE.md dist\README.md
rename dist release
cd release
rename run_server.exe gcodebin_server.exe
cd ..
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist venv rd /S /Q venv
if exist *.spec del *.spec
pause