#!/bin/bash
#author zhodj/Dingjun Zhou

USE_ERR=355
usage()
{
    echo "Usage: $0 path" 
    exit $USE_ERR 
}

gen_lookup_tags()
{
    echo -e "!_TAG_FILE_SORTED\t2\t/2=foldcase/" > filenametags
    find . -not -regex '.*\.\(png\|gif\)' -type f -printf "%f\t%p\t1\n" | \
        sort -f >> filenametags
}

gen_cscope()
{
    DIR=$1
    echo "entering $DIR ..."
    echo "generating cscope and lookup tags..."
    cd $DIR
    find . -name "*.h" -o -name "*.c" -o -name "*.cpp" -o -name "*.m" -o -name "*.mm" -o -name "*.java" -o -name "*.py" > cscope.files
    cscope -bkqR -i cscope.files
    ctags -R
    gen_lookup_tags
    echo "done!"
}

if [ "$#" -ne "1" ]
then
    usage 
fi

gen_cscope

exit 0
