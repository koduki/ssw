# SSW - Simple Shell Wrapper
SSW is simple shell wrapper.
This wrapper give some generally functions your shell script.

* command line paramater check.
* override variable.
* help option.

## HowTo

### 1. loading ssw
    #!/bin/sh
    echo "$0"
    echo "$@"
    exec python bin/ssw.py "$@" < "$0"
    !#

### 2. define variable
Using "#define" annotation.
And If you write comment, this is gen option and help message.

    # define
    MSG=${1} # -m, --message, this is simple echo messsage.
    MSG2=${2}/hogehoge # -M, --message2, this is simple echo messsage2.
    INPUT_DIR=. # -t, --target, scan target direcotry.
    DIR_LIST_FILE=dir.list

### 3. running code
This is simple shell.
Using "# main" annotation.

    # main
    echo "hello $HOSTNAME `hostname` $MSG"
    echo $MSG2
    echo $INPUT_DIR 

### 4. execute
    sh simple.sh -m hello TEST1 TEST2 -target "hoge" --ssw.debug
