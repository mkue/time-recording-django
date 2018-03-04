### Docker


```
docker exec -it timerecording_web /bin/bash
python manage.py populate_db /files/timestamps.csv
python manage.py createsuperuser
```


### Frontend

Yarn is used to install frontend development packages. See: https://yarnpkg.com/en/docs/

To install all packages, use `yarn newinstall`

To add a package, use `yarn add moment  --modules-folder ./django_root/recorder/static/yarn/` from the root directory of this project.