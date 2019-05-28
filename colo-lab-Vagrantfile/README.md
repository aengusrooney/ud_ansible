This vagrant file will create vm with FQDN in unraveldata.com domain. Update the followings variables before using this vagrant file.
This vagrant file is designed to use in unraveldata's colo or lab networks.

The hosting machine requirement

1. Vagrant 2.2.2
2. VirtualBox-6.0
3. Vagrant plugins: vagrant-hostmanager, vagrant-auto_network, vagrant-disksize
4. sudo yum install -y sshpass
5. sudo pip install -r requirements.txt

NOTE: We have Ansible Plabooks to install Virtualbox, Vagrant and its plugins

https://github.com/unraveldata-org/unravel_ansible/blob/master/provisioning/install_virtualbox.yml

https://github.com/unraveldata-org/unravel_ansible/blob/master/provisioning/install_vagrant.yml

Variables need to be updated for the Vagrantfile

1. NODENAME, the hostname of the vm, and the FQDN will <entered_node_name>.unraveldata.com
   (example = tnode1)

2. NODEIP, the IP address of the vm on bridged interface eth1.
   (example = 172.36.2.101 )

3. GATEWAY, the IP address of the default gateway used in this vm. 
   (example in colo = 172.36.0.254)

4. DNSSERVER, the IP address of the DNS server.
   (example in colo = 172.36.1.213)

5. FIRSTOCTET, the first octet of the network address.
   (example in colo or lab = 172)

6. DISK2SIZE, the 2nd disk size, only required for Vagrant file with 2nd disk
   (example = 100 or 200)

Additionally, you also need to update the vagrantconfig.yml file which has the details for:

1. MEMSIZE, memory size default for small vm is 55296  (54GB), you can make it 110592  (108GB) for single vm purpose
2. CPU, number of cpu core and default for small vm is 8, and you can increate it to 16 for single vm purpose
3. OSTYPE, the OS provider and its distributuion name (e.g. cosm/centos7 )
4. NODEIP, the IP address of the vm on bridged interface eth1
5. NODENAME, the hostname of the vm  (e.g.  tnode1)
6. eth, the network interface e.g "eno4" for congo55-74 and "enp3s0f0" for all other colo machines

This Vagrantfile will is required to run the basic vm ansible playbook and that is the file named "unravel_vm_provision.yml"

The unravel_vm_provision.yml" playbook will install needed dependency and join the node to the Windows AD environment.


## Setup a VM cluster:

### Stage 1. Provision the VM
Update `inventory`, `vagrantconfig.yml` all needed field mentioned above then run the command:
```bash
vagrant up
```

### Stage 2. Preparing Hadoop Environment
Update `inventory` file [all:vars] section to proper value then run the command:<br>
```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -v -i inventory singleNode-HDP-playbook.yml
```

### Stage 3. Create the cluster
<br>Note: CDH Template / HDP blueprint might need to be updated based on host and platform version
```bash
git clone https://<Username>@github.com/unraveldata-org/devops.git
cd devops/cloudformation/<hortonwork|cloudera>/

# HDP example
python cluster.py --host tnode12.unraveldata.com --blueprint blueprints/singleNode-blueprint.json --host-mapping blueprints/singleNode-cluster.json -v 2.6.5.0 --version-definition blueprints/version_definition.json

# CDH example
python cluster.py --host tnode12.unraveldata.com --template template/cloudera-singleNode.json -v 5.15.1 -a deploy-template
python cluster.py --host tnode12.unraveldata.com -a deploy-cms --cms-host tnode12.unraveldata.com
```


<br>
<br>

## TO-DO:
1. Update `Vagrantfile-with-2nd-disk` with the new changes
2. Get VM status for automatic VM provisioning <br>
We can call the following commands remotely from Jenkins or Rundeck to get current allocated resource and base on that information we can make VM provisioning automatic.
- Get running vms command: `vboxmanage list runningvms`
- Get VM allocated resource: `vboxmanage showvminfo vms_tnode11_1553108716623_70326|grep 'Memory size\|Number of CPUs:'`
- Available physical memory: `free`
- Available vcores and physical cores(CPU/thread per core) : `lscpu | grep -m 2 'CPU(s):\|Thread(s) per core:'`
3. Change all configuration files to jinja2 template which can be use/update easier by ansible
4. 