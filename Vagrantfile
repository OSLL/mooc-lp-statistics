# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.provider "docker" do |d|
    d.has_ssh = true
    d.image = "markzaslavskiy/mooc-lp-statistics:v1"
    config.vm.network "forwarded_port", guest: 80, host: 10000

    config.vm.provision "shell", inline: <<-EOC
      sudo apt-get -y install vim # for debug
      # HACK - transfer to Dockerfile and rebuild image
      # Enabling config as a default host
      sudo rm /etc/apache2/sites-enabled/000-default.conf
      sudo rm /etc/apache2/sites-available/000-default.conf
      sudo sed -i 's/ServerName/#/g' /etc/apache2/sites-available/mooc-lp-statistics.conf
      # /HACK
      sudo /etc/init.d/apache2 start

      # HACK - transfer to Dockerfile and rebuild image
      sudo mkdir -p /data/db
      sudo chown -R mongodb:mongodb /data
      sudo sed -i 's/journal=true/journal=false/g' /etc/mongodb.conf
      # /HACK
      sudo LC_ALL="en_US.UTF-8" /etc/init.d/mongodb start
#      sudo echo "127.0.0.1 mooc-lp-statistics" >> /etc/hosts
    EOC
   
  end
end
