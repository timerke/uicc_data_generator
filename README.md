# uicc_data_generator
Генератор данных для стандарта UICC-Terminal interface.

## Запуск

1. На компьютере должен быть установлен Python, путь к которому должен быть прописан в переменной среды PATH (на *Windows*).

2. Перейдите в папку **scripts** и установите необходимые зависимости, запустив:

   - скрипт **install.bat**, если вы работаете в *Windows*;
   - скрипт **install.sh**, если вы работаете в *Linux*.

3. Перейдите в корень репозитория.

4. В командной строке выполните команду:

   - если Вы работаете в *Windows*:

     ```batch
     venv\Scripts\python run.py -i INPUT_FILE --csv
     ```

   - если Вы работаете в *Linux*:

     ```bash
     venv/bin/python run.py -i INPUT_FILE --csv --t0
     ```

   В указанных командах используются флаги:

   - *-i*, *--input_file* - *INPUT_FILE* путь до JSON-файла с параметрами команды;
   - *--csv* - выходные данные будут выведены в CSV-формате. Это опциональный флаг, в данный момент не функционирует;
   - *--t0* - будет использоваться символьный вариант (character based protocol T=0) протокола передачи данных. Это опциональный флаг, по умолчанию используется блочный вариант (block based protocol T=1) протокола передачи данных.

