FROM resin/rpi-raspbian

#copy our files into the container
RUN mkdir -p /opt/pimometer
COPY ./bin/  /opt/pimometer/
COPY ./conf/ /opt/pimometer/
COPY ./webui/ /opt/pimometer/
RUN ln -s /opt/pimometer/webui/thermometer.html /opt/pimometer/webui/index.html

#install our required software
RUN apt-get -y install python-mongoengine mongodb-server lighttpd

#init our services
RUN service mongodb stop
RUN killall mongod
RUN service lighttpd stop
RUN cd /opt/pimometer/webui/ ; python -m SimpleHTTPServer 80 &
RUN mkdir -p /data/db
RUN mongod --rest &

EXPOSE 80 27017 28017

CMD /opt/pimometer/bin/daemon.py
