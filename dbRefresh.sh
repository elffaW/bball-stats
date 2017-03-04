#!/bin/sh

cd db

mv stats.sqlite old

sqlite3 stats.sqlite < stats.sql

cd ..

