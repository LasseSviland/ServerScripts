FROM ubuntu:14.04
MAINTAINER Kyrre Begnum "kyrre.begnum@hioa.no" 
RUN apt-get update 
RUN apt-get -y install apache2 libapache2-mod-php5 php5-mysql git libwww-perl  
RUN rm -rf /var/www/html/*
RUN git clone  https://git.cs.hioa.no/kyrre.begnum/bookface.git 
RUN cp bookface/code/* /var/www/html/
RUN rm -rf bookface
ADD config.php /var/www/html
WORKDIR /var/www/html
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
RUN mkdir -p $APACHE_RUN_DIR $APACHE_LOCK_DIR $APACHE_LOG_DIR
ONBUILD ADD . /var/www/html/
EXPOSE 22 80
ENTRYPOINT ["/usr/sbin/apache2"]
CMD [ "-D","FOREGROUND"]



RUN apt-get update 
RUN apt-get -y install munin-node 
RUN apt-get -y install apache2 libapache2-mod-php5 php5-mysql git libwww-perl  
RUN echo -e "ExtendedStatus On  \n<Location /server-status> \n    SetHandler server-status \n    Order deny,allow \n    Deny from all \n    Allow from 127.0.0.1 \n</Location>\n" >  /etc/apache2/conf-enabled/status
RUN service apache2 restart
RUN rm -rf /var/www/html/*
RUN git clone  https://git.cs.hioa.no/kyrre.begnum/bookface.git 
RUN cp bookface/code/* /var/www/html/
RUN rm /var/www/html/index.html
RUN echo -e '<?php\n$dbhost = "172.16.1.16";\n$dbport = "3306";\n$db = "bookface";\n$dbuser = "bookface";\n$dbpassw = "fiftytrackstay";\n$webhost = "172.16.1.16";\n$weburl = "http://" . $webhost ;\n?>\n' >  /var/www/html/
RUN rm -rf bookface