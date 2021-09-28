#!/bin/sh

quit(){
    if [ $# -gt 1 ];
    then
        echo "$1"
        shift
    fi
    exit $1
}

if [ ! -z "$VIRTUALENVWRAPPER_SCRIPT" ] && [ -f "$VIRTUALENVWRAPPER_SCRIPT" ];
then
    . "$VIRTUALENVWRAPPER_SCRIPT"
    mkvirtualenv -r ./dev-reqs.txt "ip-pool" || quit "Unable to make virtual environment." 1
else
    echo "Can't find virtualenvwrapper script"
    exit 1
fi
