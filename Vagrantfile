# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  #config.vm.box = "geerlingguy/ubuntu1604"
  config.vm.box = "geerlingguy/centos7"
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider :virtualbox do |v|
    v.name = "jenkins"
    v.memory = 512
    v.cpus = 2
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.hostname = "jenkins"
  config.vm.network :private_network, ip: "192.168.33.55"

  # Set the name of the VM. See: http://stackoverflow.com/a/17864388/100134
  config.vm.define :jenkins do |jenkins|
  end

  # Ansible provisioner.
  config.vm.provision "ansible" do |ansible|
    ansible.compatibility_mode = "2.0"
    ansible.playbook = "provisioning/install_packer.yml"
    #ansible.playbook = "provisioning/install_vagrant.yml"
    #ansible.playbook = "provisioning/install_virtualbox.yml"
    #ansible.playbook = "provisioning/unravel_jenkins.yml"
    #ansible.playbook = "provisioning/samp.yml"
    #ansible.playbook = "provisioning/docker.yml"
    ansible.inventory_path = "provisioning/inventory"
    ansible.become = true
    ansible.verbose = true
  end

end
