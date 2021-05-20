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

# Run “make build” by default
.DEFAULT_GOAL = build

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PKG_NAME = branch

ifneq (,$(findstring xterm,${TERM}))
	GREEN := $(shell tput -Txterm setaf 2)
	RESET := $(shell tput -Txterm sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"
else
	CS = "~~~ "
	CE = " ~~~"
endif

COV          =
HEADER_EXTRA =

REQUIREMENTS = requirements/requirements-dev.txt

PYLINT_FLAGS ?= --load-plugins=pylint_django --django-settings-module=$(PKG_NAME).settings.test
PYTEST_FLAGS ?= --color=yes -v --fail-on-template-vars
FLAKE8_FLAGS ?=

VENV_ROOT = .venv

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
    NPM     ?= npm.exe
	PYTHON  ?= python.exe
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	NPM     ?= npm
	PYTHON  ?= python3
	VENV_BIN = $(VENV_ROOT)/bin
endif

VENV_PIP    = $(VENV_BIN)/pip
VENV_PYTHON = $(VENV_BIN)/python

export PATH := $(VENV_BIN):$(PATH)

LOCAL_PORT = 8001

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
ifneq ($(OS),Windows_NT)
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
HAVE_NPM := $(shell sh -c "command -v $(NPM)")
ifndef HAVE_PYTHON
$(error "Python is not available. Please install Python.")
endif
ifndef HAVE_NPM
$(error "npm is not available. Please install npm.")
endif
endif
endif
