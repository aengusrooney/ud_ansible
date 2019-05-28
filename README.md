# Various Ansible Playbooks used in Unravel

## Following are few playbooks/roles available  
* provisioning/unravel_install.yml - Install the given version of Unravel 
* provisioning/unravel_jenkins.yml - Installs all the tools used with Jenkins and Jenkins itself
* provisioning/add_users_with_sudo_access_n_key.yml - Add the provided user & group and add sudo access
* provisioning/add_user_pub_key_to_remote.yml - Can add given users pub key on any remote host(s) 
* provisioning/docker.yml - Install & configure Docker 
* provisioning/docker_compose.yml - Install & configure docker-compose 
* utils/copy_dir_to_remote.yml - Copy/archive the given directory on host to any number of remote hosts (could be used to copy unravel-agent from server to all slaves)
* provisioning/install_virtualbox.yml - Installs VirtualBox and Its Extension Pack for RedHat Family 
* provisioning/install_vagrant.yml - Installs Vagrant for RedHat Family 
* provisioning/install_packer.yml - Installs Packer for RedHat Family 
* utils/copy_dir_to_remote.yml - Copy unravel-agent from master to all slaves

## How to use the Playbooks
For add_users_with_sudo_access_n_key.yml change the group & user values in the playbook (this needs to be externalised in vars:TBD)

Install Unravel & start services
edit unravel_server in inventory file or create your own inventory file with user , ip and ssh key info,
Also make sure to provide/update unravel version and clean inastall variables in the playbook 
* rpm_version: 4.5.0.4rc0012
* clean_install: 'YES'
```bash
ansible-playbook  -i inventory provisioning/install_unravel.yml  --limit=unravel_server 
```

There are tasks that can be run in unravel playbook, for example to get servcies 
```bash
ansible-playbook  -i inventory provisioning/install_unravel.yml  --limit=unravel_server   --tags get_services
```

Also make sure the inventory file has the sudo user and your ssh key path

```bash
ansible-playbook  -i inventory provisioning/add_users_with_sudo_access_n_key.yml
```

Install VirtualBox 
```bash
ansible-playbook -i inventory provisioning/install_virtualbox.yml
```

Install Vagrant
```bash
ansible-playbook -i inventory provisioning/install_vagrant.yml
```

Install Packer
```bash
ansible-playbook -i inventory provisioning/install_packer.yml
```

### How to copy unravel-agent from Master to all slaves
The playbook for this is in utils/copy_dir_to_remote.yml, make sure to check the inventory or create your own with master and slaves hosts , user and ssh key path. Once done execute the below command from the Master node.
```bash
ansible-playbook -i inventory copy_dir_to_remote.yml
```

### Ansible Vagrant profile for a Jenkins CI server


#### Deploying Jenkins
This Playbook deploys Jenkins Master with all software that mentioned [here](https://unraveldata.atlassian.net/wiki/spaces/DEVOPS/pages/641040541/Jenkins+Server)

Follow these steps for Jenkins Deployment:
* Run the following command to install the necessary Ansible roles for this profile: `$ ansible-galaxy install -r requirements.yml` 
* make sure the inventory file has the sudo user and your ssh key path
* Check the versions of Ruby, Python, Java, Jenkins, Node & tomcat in provisioning/vars/main.yml
* `$ ansible-playbook  -i inventory provisioning/unravel_jenkins.yml`
* Post Deployment , run the Compliance script to validate if Jenkins master has all software/packages and is up and running `$ inspec exec unravel_jenkins -i ~/.ssh/id_rsa  -t 'ssh://topcat@172.16.1.205'`

## Post deployment tests/compliance test
Execute below command to tests if all the required software is installed and Jenkins configured after using the unravel_jenkins.yml Playbook
```bash
inspec exec unravel_jenkins -t 'ssh://topcat:<password>@<host>'
```
## For Local Tests

### Background

Vagrant and VirtualBox (or some other VM provider) can be used to quickly build or rebuild virtual servers.

This Vagrant profile installs [Jenkins](http://jenkins-ci.org/) (running on Java) using the [Ansible](http://www.ansible.com/) provisioner.

### Getting Started


To use the vagrant file, you will need to have done the following:

  1. Download and Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  2. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html)
  3. Install [Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html)
  4. Open a shell prompt (Terminal app on a Mac) and cd into the folder containing the `Vagrantfile`
  5. Run the following command to install the necessary Ansible roles for this profile: `$ ansible-galaxy install -r requirements.yml`

Once all of that is done, you can simply type in `vagrant up`, and Vagrant will create a new VM, install the base box, and configure it.

Once the new VM is up and running (after `vagrant up` is complete and you're back at the command prompt), you can log into it via SSH if you'd like by typing in `vagrant ssh`. Otherwise, the next steps are below.

#### Setting up your hosts file

You need to modify your host machine's hosts file (Mac/Linux: `/etc/hosts`; Windows: `%systemroot%\system32\drivers\etc\hosts`), adding the line below:

    192.168.33.55  jenkins

(Where `jenkins`) is the hostname you have configured in the `Vagrantfile`).

After that is configured, you could visit http://jenkins:8080/ in a browser, and you'll see the Jenkins home page.

If you'd like additional assistance editing your hosts file, please read [How do I modify my hosts file?](http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file) from Rackspace.

## New Roles To be Developed
- [ ] add_users_with_sudo_access_n_key.yml
- [ ] ansible-dynamic-inventory-for-aws-ec2
- [ ] ansible_commands.txt
- [ ] copy_pub_key_to_n_machines.yml
- [ ] deploy_sudoer_file_and_stop_using_root.yml
- [ ] ec2_instance.yml
- [ ] get_http_zip_file.yml
- [ ] migrate_unravel_to_other_host.yml
- [ ] security_pathching.yml
- [ ] setup_logrotate_for_unravel.yml
- [ ] system_update_restart.yml
- [ ] update_centos_rhel.yml
- [ ] upgrade_unravel_on_test_cluster.yml
