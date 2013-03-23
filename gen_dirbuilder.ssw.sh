#!/bin/sh
echo "$0"
echo "$@"
exec python bin/ssw.py "$@" < "$0"
!#

# define
MSG=${1} # -m, --message, this is simple echo messsage.
MSG2=${2}/hogehoge # -M, --message2, this is simple echo messsage2.
INPUT_DIR=. # -t, --target, scan target direcotry.
DIR_LIST_FILE=dir.list

# main
echo "hello $HOSTNAME `hostname` $MSG"
echo $MSG2
find $INPUT_DIR -type d|awk '{print "echo \"`stat --format=_q_%a %U:%G_q_ "$1"` "$1"\""}'|sed "s/_q_/'/g"|sh > $DIR_LIST_FILE

cat ${DIR_LIST_FILE} |awk 'BEGIN{print "#/bin/sh"};{print "mkdir -p \""$3"\""}' > 01_mkdir.sh
cat ${DIR_LIST_FILE} |awk 'BEGIN{print "#/bin/sh"};{print "chown "$2" \""$3"\""}'  > 02_chown.sh 
cat ${DIR_LIST_FILE} |awk 'BEGIN{print "#/bin/sh"};{print "chmod "$1" \""$3"\""}' > 03_chmod.sh 
