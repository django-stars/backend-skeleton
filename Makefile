## Conf
TMPL_FILE_PREFIX='djangostars_project_template'



all: clean_all tmpl_django clean_builder tmpl_django_celery tmpl_django_drf tmpl_django_drf_celery
	echo -e '\033[1;95m..done..\033[0;36m'
	ls -lh builds/
	echo -e ${NC}
	cp startproject builds/

create_build_env:
	mkdir -p builds/
	mkdir builder/

clean_builder:
	rm -rf builder/

clean_all:
	rm -rf builds builder

add_django:
	echo  -e ${MSGSUBLABEL}create base Django project template...${NC}
	cd _base; cp -R ./ ../builder; cd ..

add_celery:
	echo  -e ${MSGSUBLABEL}add Celery to template...${NC}
	cd _celery; cp -R ./ ../builder; cd ..
	echo "from .celery import *  # noqa" >> builder/project_name/settings/__init__.py
	sed -i "/# end packages/i\Celery = \"*\"" builder/Pipfile
	echo -e "$$SRC_CELERY_INIT">> builder/project_name/__init__.py
	echo -e "$$SRC_CELERY_RUN">> builder/Makefile

add_drf:
	echo  -e ${MSGSUBLABEL}add DRF to template...${NC}
	cd _drf; cp -R ./ ../builder; cd ..
	echo "from .restapi import *  # noqa" >> builder/project_name/settings/__init__.py
	sed -i "/# end packages/i\djangorestframework = \"*\"" builder/Pipfile
	sed -i "/# 3rd party apps/a\    'rest_framework'," builder/project_name/settings/django.py

clean_build_files:
	find . -name "*~" -delete  # Emacs temp files

tmpl_django:
	echo  -e ${MSGLABEL}Django Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) add_django
	cd builder/; tar czf ../builds/${TMPL_FILE_PREFIX}__django.tar.gz .; cd ..
	$(MAKE) clean_builder

tmpl_django_celery:
	echo  -e ${MSGLABEL}Django + Celery Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) add_django
	$(MAKE) add_celery
	$(MAKE) clean_build_files
	cd builder/; tar czf ../builds/${TMPL_FILE_PREFIX}__django_celery.tar.gz .; cd ..
	$(MAKE) clean_builder

tmpl_django_drf:
	echo  -e ${MSGLABEL}Django + DRF Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) add_django
	$(MAKE) add_drf
	$(MAKE) clean_build_files
	cd builder/; tar czf ../builds/${TMPL_FILE_PREFIX}__django_drf.tar.gz .; cd ..
	$(MAKE) clean_builder

tmpl_django_drf_celery:
	echo  -e ${MSGLABEL}Django + DRF + Celery Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) add_django
	$(MAKE) add_drf
	$(MAKE) add_celery
	$(MAKE) clean_build_files
	cd builder/; tar czf ../builds/${TMPL_FILE_PREFIX}__django_drf_celery.tar.gz .; cd ..
	$(MAKE) clean_builder


ifndef VERBOSE
.SILENT:
endif

define SRC_CELERY_INIT
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app


__all__ = ('celery_app',)

endef
export SRC_CELERY_INIT

define SRC_CELERY_RUN

celery:
	pipenv run celery -A $${PROJECTNAME} worker -l info --beat
endef
export SRC_CELERY_RUN

## Colors
MSGLABEL='\033[1;33m'
MSGSUBLABEL='\033[0;33m'
MSGDONE='\033[0;32m'
NC='\033[0m'
