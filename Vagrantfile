# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$verify_webui = <<EOS
  if [ -d /vagrant/webui/ ]; then
    webui_installed=1
    apt-get -y -qq install lighttpd
    rm -rf /var/www/
    ln -s /vagrant/webui /var/www
    ln -s /var/www/thermometer.html /var/www/index.html
    sed -i 's/index.html/thermometer.html/' /etc/lighttpd/lighttpd.conf
    /etc/init.d/lighttpd restart
  else
    webui_installed=0
  fi

  if [ $webui_installed != 1 ]; then
    echo ""
    echo "In order to have a working web interface (beyond the mongo API), please ensure to checkout the git submodules as well..."
    sleep 4
    echo "Continuing setup without a webui..."
  fi
EOS

$welcome_script = <<EOS
  ip=$(ip addr show eth0 | grep eth0 | grep inet | cut -d/ -f1| awk '{print $2}')
  database=$(grep database /vagrant/conf/pimometer.conf | awk '{print $3}')
  collection=$(grep collection /vagrant/conf/pimometer.conf | awk '{print $3}')
  echo "You can view the mongodb data at http://$ip:28017/$database/$collection/"
  if [ -d /vagrant/webui/ ]; then
      echo "The userfriendly web interface can be accessed at http://$ip/"
  fi
EOS

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "baremettle/debian-7.5"

  config.vm.synced_folder ".", "/vagrant", type: "rsync",
    rsync__auto: true

  config.vm.provision "shell", inline: $verify_webui

  config.vm.provision "shell",
    inline: "apt-get -yqqq install python-django python-mongoengine python-pip mongodb-server git"

  config.vm.provision "shell",
    inline: "pip -q install djangorestframework django-rest-framework-mongoengine markdown django-filter"

  config.vm.provision "shell",
    inline: "/etc/init.d/mongodb stop && sleep 5 && mongod --quiet --rest --jsonp --dbpath=/var/lib/mongodb --fork --logpath=/var/log/mongodb/mongodb.log"

  config.vm.provision "shell",
    inline: "mkdir -p /etc/pimometer && cp /vagrant/conf/pimometer.conf /etc/pimometer/pimometer.conf && chmod a+r /etc/pimometer/pimometer.conf"

  config.vm.provision "shell",
    inline: "/vagrant/bin/daemon.py demo=True &"

  config.vm.provision "shell", inline: $welcome_script

end
