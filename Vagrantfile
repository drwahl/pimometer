# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$welcome_script = <<EOS
  ip=$(ip addr show eth0 | grep eth0 | grep inet | cut -d/ -f1| awk '{print $2}')
  echo "You can now access your instance at http://$ip/"
EOS

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "baremettle/debian-7.5"

  config.vm.synced_folder ".", "/vagrant", type: "rsync",
    rsync__auto: true

  config.vm.provision "shell",
    inline: "apt-get -yqq install python-django python-mongoengine python-pip mongodb-server"

  config.vm.provision "shell",
    inline: "pip install djangorestframework markdown django-filter"

  config.vm.provision "shell",
    inline: "sed -i 's/bind_ip = 127.0.0.1/bind_ip = 0.0.0.0/' /etc/mongodb.conf && /etc/init.d/mongodb restart"

  config.vm.provision "shell",
    inline: "/usr/bin/python /vagrant/pimometer/manage.py runserver 0.0.0.0:80 &"

  config.vm.provision "shell", inline: $welcome_script

end
