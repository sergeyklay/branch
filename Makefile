# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

include default.mk

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ] ; then \
		echo $(ROOT_DIR) > $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PKG_NAME) -a ! -L $(WORKON_HOME)/$(PKG_NAME) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PKG_NAME); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use \"workon $(PKG_NAME)\" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PKG_NAME)" -a -f "$(WORKON_HOME)/$(PKG_NAME)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PKG_NAME); \
		fi; \
	fi
endef

requirements/%.txt: requirements/%.in $(VENV_BIN)
	$(VENV_BIN)/pip-compile --output-file=$@ $<

build.py: $(VENV_PYTHON)
	@echo $(CS)"Generate project's build ids"$(CE)
	$(VENV_PYTHON) manage.py create_build_id

## Public targets

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(PYTHON) -m venv --prompt $(PKG_NAME) $(VENV_ROOT)
	@echo
	@echo Done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo See https://docs.python.org/3/library/venv.html for more.
	@echo
	$(call mk-venv-link)

.PHONY: init
init: $(VENV_PYTHON)
	@echo $(CS)Set up virtualenv$(CE)
	$(VENV_PIP) install --upgrade pip pip-tools setuptools wheel
	@echo

.PHONY: install
install: $(REQUIREMENTS)
	@echo $(CS)Installing $(PKG_NAME) and all its dependencies$(CE)
	$(VENV_BIN)/pip-sync $(REQUIREMENTS)
	$(VENV_PIP) install -e .
	$(VENV_PIP) install --upgrade twine check-manifest check-wheel-contents
	$(NPM) install
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./build ./dist ./*.egg-info
	$(RM) -r ./node_modules
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./storage/coverage/htmlcov
	$(RM) ./storage/coverage/coverage.*
	$(RM) ./storage/logs/*.log
	$(RM) ./storage/pids/*.pid
	@echo

.PHONY: maintainer-clean
maintainer-clean: clean
	@echo $(CS)Performing full clean$(CE)
	-$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	$(RM) ./build.py
	$(RM) requirements/*.txt
	@echo

.PHONY: lint
lint: $(VENV_PYTHON)
	@echo $(CS)Running linters$(CE)
	-$(VENV_BIN)/flake8 $(FLAKE8_FLAGS) ./
	$(VENV_BIN)/pylint $(PYLINT_FLAGS) ./$(PKG_NAME) ./apps
	@echo

.PHONY: build
build: build.py
	@echo $(CS)Compress static assets$(CE)
	$(VENV_PYTHON) manage.py compress

.PHONY: serve
serve: $(VENV_PYTHON)
	@echo $(CS)Starting web server on $(LOCAL_PORT) port$(CE)
	$(VENV_PYTHON) manage.py runserver $(LOCAL_PORT)

.PHONY: static
static: $(VENV_PYTHON)
	@echo $(CS)Collect static files$(CE)
	$(VENV_PYTHON) manage.py collectstatic --noinput --clear --ignore *.scss

# See: https://sass-lang.com/install
.PHONY: css
css:
	sass -I $(include) --no-source-map $(infile) $(outfile)

.PHONY: migrations
migrations: $(VENV_PYTHON)
	$(VENV_PYTHON) manage.py makemigrations

.PHONY: migrate
migrate: $(VENV_PYTHON)
	$(VENV_PYTHON) manage.py migrate

.PHONY: ccov
ccov: $(VENV_PYTHON)
	@echo $(CS)Combine coverage reports$(CE)
	$(VENV_BIN)/coverage combine
	$(VENV_BIN)/coverage report
	$(VENV_BIN)/coverage html
	$(VENV_BIN)/coverage xml
	@echo

.PHONY: manifest
manifest:
	@echo $(CS)Check MANIFEST.in for completeness$(CE)
	$(VENV_BIN)/check-manifest -v
	@echo

.PHONY: test
test: export EMAIL_BACKEND=django.core.mail.backends.dummy.EmailBackend
test: export CACHE_BACKEND=django.core.cache.backends.dummy.DummyCache
test: export DJANGO_SETTINGS_MODULE=$(PKG_NAME).settings
test: export SECRET_KEY='Naive and not very secret key used for tests'
test: export RECAPTCHA_PUBLIC_KEY='Naive and not very secret key used for tests'
test: export RECAPTCHA_PRIVATE_KEY='Naive and not very secret key used for tests'
test: export DATABASE_URL=sqlite://:memory:
test: export DEBUG=False
test: export USE_SSL=False
test: export WORKER_LOGLEVEL=info
test: build.py $(VENV_PYTHON)
	@echo $(CS)Running tests$(CE)
	$(VENV_BIN)/coverage erase
	$(VENV_BIN)/coverage run -m pytest $(PYTEST_FLAGS)
	@echo

.PHONY: help
help:
	@echo $(PKG_NAME)
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  init:         Set up virtualenv (has to be launched first)'
	@echo '  install:      Install project and all its dependencies'
	@echo '  serve:        Run development server'
	@echo '  static:       Collect static files'
	@echo '  css:          Build CSS files from SCSS source'
	@echo '  migrations:   Create database migrations'
	@echo '  migrate:      Run all database migrations'
	@echo '  build:        Prepare project to use'
	@echo '  test:         Run unit tests'
	@echo '  ccov:         Combine coverage reports'
	@echo '  lint:         Lint the code'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  maintainer-clean:'
	@echo '                Delete almost everything that can be reconstructed'
	@echo '                with this Makefile'
	@echo
	@echo 'Nodejs:'
	@echo
	@echo '  npm:          $(HAVE_NPM)'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Flags:'
	@echo
	@echo '  FLAKE8_FLAGS: $(FLAKE8_FLAGS)'
	@echo '  PYTEST_FLAGS: $(PYTEST_FLAGS)'
	@echo '  PYLINT_FLAGS: $(PYLINT_FLAGS)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  NPM:          $(NPM)'
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
	@echo
