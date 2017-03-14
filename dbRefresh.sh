#!/bin/sh

if [ $# -eq 0 ] ; then
	echo "USAGE: ./dbRefresh.sh YYYY"
	exit 1
fi

cd db

mv stats_${1}.sqlite old

sqlite3 stats_${1}.sqlite < stats.sql

cd ..

