HDP ansible playbook for single node vm or multi-vm clusters
#### singleNode-HDP-playbook.yaml
The playbook that needs to be run after the VM provisioning to prepare the environment.
It will do the followings:
- Install and setup Ambari and agent (Version dependent)
- Install EPEL
- Install Mysql Java Connector

#### cluster.py
script to install HDP via Ambari API

Supported HDP versions:
- 2.6.5
- 2.6.4
- 2.6.3
- 2.6.2
- 2.6.1
- 2.5.3

The script needs 5 parameters, script will modify VDF to install corresponding HDP version:
- -host: Ambari server hostname
- -v: HDP version X.Y.Z check Supported HDP versions above
- --blueprint: path to the Ambari blueprint file
- --host-mapping: path to the Ambari Host mapping file
- --version-definition: path to the Ambari VDF file


```bash
python cluster.py -host tnode11.unraveldata.com --blueprint blueprints/singleNode-blueprint.json --host-mapping blueprints/singleNode-cluster.json -v 2.6.5.0 --version-definition blueprints/version_definition.json
```
