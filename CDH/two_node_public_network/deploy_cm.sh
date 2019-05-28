#!/usr/bin/env bash

source ../../../vagrant_examples/local_ansible/bin/activate

echo "Deploying Cloudera Manager"

NODE1=$(grep 'master:' node1/vagrantconfig.yml | cut -d'"' -f2)
NODE1_IP=$(grep 'master_ip:' node1/vagrantconfig.yml | cut -d'"' -f2)
NODE1_CDH_VER=$(grep 'cdh_version' node1/vagrantconfig.yml | cut -d':' -f2)
NODE2=$(grep 'master:' node2/vagrantconfig.yml | cut -d'"' -f2)
echo Node1 host name $NODE1 and Node1 is $NODE2
#sed -i "s/=key1/=node1\/${NODE1}_key/" multi_node_hosts
#sed -i "s/=key2/=node2\/${NODE2}_key/" multi_node_hosts
#sed -i "s/^node1 /${NODE1}.unraveldata.com/g" multi_node_hosts
#sed -i "s/^node2 /${NODE2}.unraveldata.com/g" multi_node_hosts
HOSTS_REACHABLE=$(ansible all -i multi_node_hosts -m ping)
if [ $?  -ne 0 ]; then
    echo "One of the hosts in multi_node_hosts in not rechable"
fi

echo "Installing Cloudera Manager"
#ansible-playbook -i multi_node_hosts ../../../devops/cloudera_install/cloudera_install/cloudera.yml --become --become-method=sudo

#sed -i "s/tnode2.unraveldata.com/${NODE1}.unraveldata.com/g" devops/cloudformation/cloudera/template/vm_2_nodes.json
#sed -i "s/snode1.unraveldata.com/${NODE2}.unraveldata.com/g" devops/cloudformation/cloudera/template/vm_2_nodes.json

echo python cloudformation/cloudera/cluster.py --host $NODE1_IP  -t cloudformation/cloudera/template/vm_2_nodes.json -a deploy-template -v $NODE1_CDH_VER 
#cd devops; python cloudformation/cloudera/cluster.py --host #{CONF['ip']} -t cloudformation/cloudera/template/vm_2_nodes.json -a deploy-template -v #{CONF['cdh_version']}
 
echo "Deploying cluster ..."
#cd ..
echo python cloudformation/cloudera/cluster.py --host $NODE1_IP  -a deploy-cms
sed -i "s/tnode2.unraveldata.com/${NODE1}.unraveldata.com/g" devops/template/cm_install.json
cd devops; python cloudformation/cloudera/cluster.py --host $NODE1_IP -a deploy-cms
# rename properties in vagrantconfig.yml #
# grep for hostname for each node #
# grep 'master:' node1/vagrantconfig.yml | cut -d'"' -f2 #
# use that to sed and update hosts and key in ansible hosts file #
# sed -i 's/^node1 /tnode27.unraveldata.com/g' multi_node_hosts # 
# sed -i 's/^node2 /tnode28.unraveldata.com/g' multi_node_hosts # 
# run ansible command with  by getting devops repo path variable and get playbook name #
# Before cluster deployment , the json template needs to be updated with host names #
