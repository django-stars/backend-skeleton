## Conf
TMPL_PROJECT_FILE_PREFIX='djangostars_project_template'
TMPL_APPLICATION_FILE_PREFIX='djangostars_app_template'
TMP="/tmp/tmp.be_skeleton_builder"
CURRENTDIR := $(shell pwd)


all: greeting clean_all create_build_env
	$(MAKE) tmpl_proj__django
	$(MAKE) tmpl_proj__django_celery
	$(MAKE) tmpl_proj__django_drf
	$(MAKE) tmpl_proj__django_drf_celery
	$(MAKE) tmpl_app__django
	$(MAKE) tmpl_app__django_drf
	echo -e '\033[1;95m..done..\033[0;36m'
	ls -lh builds/
	echo -e ${NC}
	cp startproject builds/
	rm -rf ${TMP}
	${MAKE} web_index

greeting:
	echo -e "\033[1;91m"
	echo "                                                                                                                                                       "
	echo "    _/_/_/                        _/                                  _/        _/_/_/  _/                  _/              _/                         "
	echo "   _/    _/    _/_/_/    _/_/_/  _/  _/      _/_/    _/_/_/      _/_/_/      _/        _/  _/      _/_/    _/    _/_/    _/_/_/_/    _/_/    _/_/_/    "
	echo "  _/_/_/    _/    _/  _/        _/_/      _/_/_/_/  _/    _/  _/    _/        _/_/    _/_/      _/_/_/_/  _/  _/_/_/_/    _/      _/    _/  _/    _/   "
	echo " _/    _/  _/    _/  _/        _/  _/    _/        _/    _/  _/    _/            _/  _/  _/    _/        _/  _/          _/      _/    _/  _/    _/    "
	echo "_/_/_/      _/_/_/    _/_/_/  _/    _/    _/_/_/  _/    _/    _/_/_/      _/_/_/    _/    _/    _/_/_/  _/    _/_/_/      _/_/    _/_/    _/    _/   "
	echo -e "\033[0;32m"
	echo "                                                                                                                         by Django Stars"
	echo -e ${NC}
	echo ""

create_build_env:
	mkdir -p builds/
	mkdir -p ${TMP}

clean_builder:
	rm -rf ${TMP}/*

clean_all:
	rm -rf builds ${TMP}/*

clean_build_files:
	find ${TMP}/ -name "*~" -delete  # Emacs temp files


### Project Template ###########################################################

tmpl_proj__add_django:
	echo  -e ${MSGSUBLABEL}create base Django project template...${NC}
	cd project_template/_base/; cp -R ./ ${TMP}/; cd ../../

tmpl_proj__add_celery:
	echo  -e ${MSGSUBLABEL}add Celery to template...${NC}
	cd project_template/_celery/; cp -R ./ ${TMP}; cd ../../
	sed -i "/# end packages/i\Celery = \"*\"" ${TMP}/Pipfile
	echo "$$SRC_CELERY_INIT" >> ${TMP}/project_name/__init__.py
	echo "$$SRC_CELERY_RUN" >> ${TMP}/Makefile

tmpl_proj__add_drf:
	echo  -e ${MSGSUBLABEL}add DRF to template...${NC}
	cd project_template/_drf/; cp -R ./ ${TMP}/; cd ../../
	sed -i "/# end packages/i\djangorestframework = \"*\"" ${TMP}/Pipfile
	sed -i "/# 3rd party apps/a\    'rest_framework'," ${TMP}/project_name/settings/django.py

tmpl_proj__django: clean_builder
	echo  -e ${MSGLABEL}Django Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_proj__add_django
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_PROJECT_FILE_PREFIX}__django.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder

tmpl_proj__django_celery: clean_builder
	echo  -e ${MSGLABEL}Django + Celery Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_proj__add_django
	$(MAKE) tmpl_proj__add_celery
	$(MAKE) clean_build_files
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_PROJECT_FILE_PREFIX}__django_celery.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder

tmpl_proj__django_drf: clean_builder
	echo  -e ${MSGLABEL}Django + DRF Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_proj__add_django
	$(MAKE) tmpl_proj__add_drf
	$(MAKE) clean_build_files
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_PROJECT_FILE_PREFIX}__django_drf.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder

tmpl_proj__django_drf_celery: clean_builder
	echo  -e ${MSGLABEL}Django + DRF + Celery Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_proj__add_django
	$(MAKE) tmpl_proj__add_drf
	$(MAKE) tmpl_proj__add_celery
	$(MAKE) clean_build_files
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_PROJECT_FILE_PREFIX}__django_drf_celery.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder


### Application Template #######################################################

tmpl_app__add_django:
	echo  -e ${MSGSUBLABEL}create base Django application template...${NC}
	cd app_template/_base/; cp -R ./ ${TMP}/; cd ..

tmpl_app__add_drf:
	echo  -e ${MSGSUBLABEL}add DRF to application template...${NC}
	cd app_template/_drf/; cp -R ./ ${TMP}/; cd ..

tmpl_app__django: clean_builder
	echo  -e ${MSGLABEL}Django Application Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_app__add_django
	$(MAKE) clean_build_files
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_APPLICATION_FILE_PREFIX}__django.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder

tmpl_app__django_drf: clean_builder
	echo  -e ${MSGLABEL}Django Application + DRF Template...${NC}
	$(MAKE) create_build_env
	$(MAKE) tmpl_app__add_django
	$(MAKE) tmpl_app__add_drf
	$(MAKE) clean_build_files
	cd ${TMP}/; tar czf ${CURRENTDIR}/builds/${TMPL_APPLICATION_FILE_PREFIX}__django_drf.tar.gz .; cd ${CURRENTDIR}
	$(MAKE) clean_builder


### Web pages ##################################################################
WEB_INDEX_CONTENT := $(shell pandoc README.md)

web_index:
	echo -e "$$SRC_WEB_INDEX"  > builds/index.html


### Variables ##################################################################


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

define SRC_WEB_INDEX
<html>
<head>
  <title>Django Stars Backend Skeleton</title>
  <link href="https://fonts.googleapis.com/css?family=Cuprum" rel="stylesheet">
  <style>
	* {
	  font-family: 'Cuprum', sans-serif;
	}
	html, body {
	  background-color: #3F3024;
	}
	#content {
	  position: absolute;
	  top: 50%;
	  left: 50%;
	  -moz-transform: translateX(-50%) translateY(-50%);
	  -webkit-transform: translateX(-50%) translateY(-50%);
	  transform: translateX(-50%) translateY(-50%);
	  color: #CCC9A1;
	}
	h1 {
	  text-align: center;
	}
	code {
	  color: #CCC9A1 !important;
	  border: 1px solid #333;
	  border-radius: 3px;
	  background-color: #00494C;
	  padding: 1px 4px;
	}
	a {
	  color: #A53F2B;
	}
  </style>
</head>
<body>

  <div id="content">${WEB_INDEX_CONTENT}</div>

</body>
</html>
endef
export SRC_WEB_INDEX

## Colors
MSGLABEL='\033[1;33m'
MSGSUBLABEL='\033[0;33m'
MSGDONE='\033[0;32m'
NC='\033[0m'
