cd ..
echo -e "\n===== https://$C9_HOSTNAME =====\n"
F:/PyCharm/Anaconda/python.exe gunicorn app.main:application --access-logfile - --worker-class gevent --bind 192.168.0.10:4000