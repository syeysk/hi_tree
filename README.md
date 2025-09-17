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

Соберите статику:
```sh
python manage.py collectstatic
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

## На Windows

### Установка GDAL

1. Скачать `GDAL-3.4.3-cp311-cp311-win_amd64.whl` из https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal (https://www.cgohlke.com/#gdal)
2. Установить: `pip install GDAL-3.4.3-cp311-cp311-win_amd64.whl`
3. В `.env` добавить:
    - `GDAL_LIBRARY_PATH=venv/Lib/site-packages/osgeo/gdal304.dll`
    - `GEOS_LIBRARY_PATH=venv/Lib/site-packages/osgeo/geos_c.dll`

Источники:
- https://opensourceoptions.com/how-to-install-gdal-for-python-with-pip-on-windows/

### Установка Spatialite

1. Скачать `mod_spatialite-5.1.0-win-amd64.7z` из http://www.gaia-gis.it/gaia-sins/windows-bin-amd64/
2. Извлечь все *.dll в `venv/Scripts`
3. В `.env` добавить: `SPATIALITE_LIBRARY_PATH=mod_spatialite`

Источники:
- https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/spatialite/
- https://stackoverflow.com/questions/39787700/unable-to-locate-the-spatialite-library-django


## Интерфейс командной строки

## Интерфейс API

## Обсуждение

Задать вопрос или обсудить проект можно в Телеграм-канале:
- https://t.me/hi_tree_group
