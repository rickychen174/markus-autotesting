#!/usr/bin/env bash

set -e

get_method_names() {
python3 - <<EOPY
import json
with open('${ENVSETTINGS}') as f:
	settings = json.load(f)
solution_group = settings['solution_group']
names = set()
for group in solution_group:
	name = group['java_method_name']
	if 'CONNECTION' not in name and name not in names:
		print(name)
	names.add(name)
EOPY
}

get_datasets_from_method_name() {
python3 - <<EOPY
import json
with open('${ENVSETTINGS}') as f:
	settings = json.load(f)
solution_group = settings['solution_group']
for group in solution_group:
	if group['java_method_name'] == '$1'
		print(group['dataset_file_path'])
EOPY
}

remove_schemas() {
	local method_names=$(get_method_names)
	local schemas=""
	local dbstring=""
	local oracledb=$(get_install_setting oracle_database)
	local oracleuser=${oracledb}
	for testname in "${method_names[@]}"; do
		local datasets=$(get_datasets_from_method_name ${testname})
    	for datafile in "${datasets[@]}"; do
    		local schemaname="${TESTERNAME}_$(basename -s .sql ${datafile})"
    		if [[ "${schemas}" != *" ${schemaname} "* ]]; then
    			dbstring="${dbstring}
    			DROP SCHEMA IF EXISTS ${schemaname} CASCADE;"
    			schemas="${schemas} ${schemaname} "
    		fi
    	done
	done
	psql -U ${oracleuser} -d ${oracledb} -h localhost -f <(echo ${dbstring})
}

get_setting() {
    cat ${ENVSETTINGS} | python3 -c "import sys, json; print(json.load(sys.stdin)['$1'])"
}

get_install_setting() {
	cat ${INSTALLSETTINGS} | python3 -c "import sys, json; print(json.load(sys.stdin)['$1'])"
}

# script starts here
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 environment_dir"
    exit 1
fi

ENVDIR=$(readlink -f $1)
TESTERNAME=$(basename ${ENVDIR})
ENVSETTINGS=${ENVDIR}/environment_settings.json

THISSCRIPT=$(readlink -f ${BASH_SOURCE})
BINDIR=$(dirname ${THISSCRIPT})
SPECSDIR=$(dirname ${BINDIR})/specs
INSTALLSETTINGS=${SPECSDIR}/install_settings.json

remove_schemas
