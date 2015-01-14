#!/usr/bin/expect
#author zhodj/zhoudingjun

set timeout 60
set host 
set name 
set password 
set port 

set src_path ""
set des_path ""
set exculude_path ""

spawn bash
expect "$"
send "rsync  -a --delete --rsh=\"ssh -p $port\" $src_path $name@$host:$des_path --exclude .svn --exclude-from=$exculude_path\r"
expect {
    "Password:" {
        send "$password\n"
    }
}

spawn ssh $host -l $name -p $port
expect {
    "(yes/no)?" {
        send "yes\n"
        expect "Password:"
        send "$password\n"
    }       
    "Password:" {
        send "$password\n"
    }
}

expect ">"
send "echo\n"
interact
