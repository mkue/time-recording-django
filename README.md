### Docker


```
docker exec -it timerecording_web /bin/bash
python manage.py populate_db /files/timestamps.csv
python manage.py createsuperuser
```


### Frontend

Yarn is used to install frontend development packages. See: https://yarnpkg.com/en/docs/

