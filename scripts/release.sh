cd ..
rm -rf build
rm -rf dist
rm -rf release
rm -rf venv

python3 -m venv venv
./venv/bin/python3 -m pip install --upgrade pip
./venv/bin/python3 -m pip install -r requirements.txt
./venv/bin/python3 -m pip install pyinstaller
./venv/bin/pyinstaller run_server.py --clean --onefile \
--add-data "./gcodebin/gcodebin.json:gcodebin" \
--add-data "./http_server/static/css/*:http_server/static/css" \
--add-data "./http_server/static/img/*:http_server/static/img" \
--add-data "./http_server/static/js/*:http_server/static/js" \
--add-data "./http_server/views/*:http_server/views" \
--icon "./http_server/static/img/favicon.ico"

cp ./config.ini ./dist/config.ini
cp ./README.md ./dist/README.md
mv dist release
mv ./release/run_server ./release/gcodebin_server
rm -rf build
rm -rf dist
rm -rf venv
rm -rf *.spec