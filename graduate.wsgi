[uwsgi]
chdir=/home/lastone817/graduate
module=graduate.wsgi:application
master=true
processes=10
vacuum=true
max-requests = 5000
socket = /tmp/graduate.sock
chmod-socket = 666
daemonize=/home/lastone817/graduate/graduate.log
pidfile=/home/lastone817/graduate/graduate.pid
