# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.provider "docker" do |d|
    d.has_ssh = true
    d.image = "markzaslavskiy/mooc-lp-statistics:v1"
    config.vm.network "forwarded_port", guest: 80, host: 10000

    config.vm.provision "shell", inline: <<-EOC
      sudo /etc/init.d/apache2 start
      sudo LC_ALL="en_US.UTF-8" /etc/init.d/mongodb start
#      sudo echo "127.0.0.1 mooc-lp-statistics" >> /etc/hosts
    EOC
   
  end
end
