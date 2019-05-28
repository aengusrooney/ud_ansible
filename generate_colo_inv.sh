#!/bin/bash

## Usage : generate_colo_inv.sh <colo_mahine_start_number> <colo_mahine_end_number> ##
## Example : generate_colo_inv.sh 58 75 , will generate ansible invetory with ssh options for colo machine 58 to 75 ##

AN_OPTIONS=" ansible_port=22 ansible_user=topcat ansible_ssh_private_key_file=~/.ssh/topcat ansible_ssh_common_args='-o StrictHostKeyChecking=no' "
for i in `seq $1 $2`;do
echo "congo${i} ${AN_OPTIONS}"
done
