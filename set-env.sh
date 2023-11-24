# !/bin/bash
source bin/utils
function printUsage() {
    cat <<EOF

    Set the environment variables.

    Usage: set-env-local.sh [--env ENV]

	--env: Whether to run in dev or prod. Possible value are:  dev | prod. Default "dev"

EOF
}

ENV="dev"
DATA_DIR=""
CONDA_ENV_NAME=""
while [ $# -gt 0 ]; do
    ARG=$1
    case $ARG in
    -h | --help)
        printUsage
        exit 1
        ;;
    --env)
        shift
        ENV=$1
        shift
        ;;
    esac
done

# Read DATA_DIR and CONDA_ENV from file generated during install
while IFS= read -r line; do
    IFS='=' read -ra KEY_VALUE <<<"$line"
    printf -v "${KEY_VALUE[0]}" "%s" "${KEY_VALUE[1]}"
done <".env"

## DIRECTORIES ##
# The home directory
BASE_DIR=$(pwd -P)
export BASE_DIR=$BASE_DIR

# The front end directory
export FRONT_DIR=$BASE_DIR/front

# bash CLI directory
export PATH=$PATH:$BASE_DIR/bin

# SQLite directory
export SQLITE_DIR=$DATA_DIR/sqlite

## VARIABLES ##
# Add our python package to the pythonpath
export PYTHONPATH="${PYTHONPATH}:$BASE_DIR/src"

# Environment mode
export ENV="$ENV"

if [ -d $SQLITE_DIR ]; then
    # Set our sqlite alias
    alias sqlite3=$SQLITE_DIR/sqlite3
else
    error "Sqlite is not setup yet, please run the install script before"
    return 0
fi

if [ -z $CONDA_ENV_NAME ]; then

    error "CONDA_ENV_NAME is not setup yet, please run the install script before"
    return 0
else
    source ~/anaconda3/etc/profile.d/conda.sh
    conda activate $CONDA_ENV_NAME
fi

info "Environnement set with :
        BASE_DIR=$BASE_DIR
        ENV="$ENV"
        SQLITE="$SQLITE_DIR"
        CONDA_ENV_NAME=$CONDA_ENV_NAME"
