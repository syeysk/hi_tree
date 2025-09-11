# База исторических наименований административно-территориальных единиц

## Подготовка к работе

Находясь в директории репозитория, перейдите в рабочую директорию:
```sh
cd server
```

Установите зависимости:
```sh
pip install -r requirements.txt
```

Примените миграции:
```sh
python manage.py migrate
```

Импортируйте базу:
```sh
python -Xutf8 manage.py yaml2csv -r
python -Xutf8 manage.py loaddata data.yaml
```

Экспортируйте базу:
```sh
python -Xutf8 manage.py dumpdata adminutils --format yaml -o data.yaml
python -Xutf8 manage.py yaml2csv
```

## Интерфейс командной строи
