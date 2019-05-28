import re
import json
import time
import argparse
import requests

class Hdp_cluster:
    def __init__(self):
        self.options = self.argv_parser()
        self.user = self.options.username
        self.passwd = self.options.password
        self.host = self.options.host
        self.session = requests.Session()
        self.session.auth = (self.user, self.passwd)
        self.session.headers.update({"X-Requested-By": "ambari"})
        self.blueprint = None
        self.host_mapping = None
        self.ver_def = None

    def argv_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-host",
                            "--host",
                            help="Ambari Host name or Ip",
                            required=True)
        parser.add_argument("-b",
                            "--blueprint",
                            help="Ambari blueprint file",
                            default='blueprints/blueprint.json')
        parser.add_argument("-m",
                            "--host-mapping",
                            help="Ambari host mapping file",
                            default='blueprints/cluster.json')
        parser.add_argument("-v",
                            "--hdp-version",
                            "--hdp_version",
                            help="hdp version e.g. 2.6.1.0, 2.5.2.0")
        parser.add_argument("-n",
                            "--node",
                            help="node count",
                            type=int,
                            default=4)
        parser.add_argument("-ha",
                            "--ha",
                            help="use high availability template",
                            action='store_true')
        parser.add_argument("--username",
                            help="ambari username",
                            default="admin")
        parser.add_argument("--password",
                            help="ambari password",
                            default="admin")
        parser.add_argument("-vdf",
                            "--version-definition",
                            dest="version_def",
                            help="version definition file path")
        options = parser.parse_args()

        return options

    def check_process(self):
        res = self.session.get('http://%s:8080/api/v1/clusters/HDP/requests' % self.host)
        result = json.loads(res.text)
        for n, item in enumerate(result['items']):
            res = self.session.get(item['href'])
            requests_dict = json.loads(res.text)['Requests']
            if requests_dict['request_status'] == 'IN_PROGRESS' or requests_dict['request_status'] == 'PENDING':
                # print(requests_dict['request_context'] + ": "+ str(requests_dict['progress_percent']) + "%" )
                return ('Running')
        return ('No Running')

    def create_cluster(self):
        if self.options.hdp_version:
            if re.match('^2\.5', self.options.hdp_version):
                with open('blueprints/blueprint2.5.json', 'r') as f:
                    self.blueprint = json.load(f)
                    f.close()

        if self.options.ha:
            self.options.blueprint = 'blueprints/blueprint-ha.json'

        with open(self.options.blueprint, 'r') as f:
            self.blueprint = json.load(f)
            f.close()
        with open(self.options.host_mapping, 'r') as f:
            self.host_mapping = json.load(f)
            f.close()
        if self.options.version_def:
            with open(self.options.version_def, 'r') as f:
                self.ver_def = json.load(f)
                f.close()

        self.modify_template()

        # Upload blueprint
        res = self.session.post('http://%s:8080/api/v1/blueprints/HDP' % self.host, data=json.dumps(self.blueprint))
        print(res.text)

        # Change VDF
        if self.options.version_def:
            res = self.session.post('http://%s:8080/api/v1/version_definitions' % self.host, data=json.dumps(self.ver_def))
            print(res.text)

        # Create Cluster
        res = self.session.post('http://%s:8080/api/v1/clusters/HDP' % self.host, data=json.dumps(self.host_mapping))
        print(res.text)

        time.sleep(15)

    def modify_template(self):
        if self.host_mapping['host_groups'][0].get('host_count', 0) == 1:
            pass
        # add host if cluster has more than 4 nodes
        elif self.options.ha:
            self.host_mapping['host_groups'][2]['hosts'].append({"fqdn": "data-5.uddev.unraveldata.com"})
            if self.options.node > 5:
                for n in range(6, self.options.node + 1):
                    self.host_mapping['host_groups'][2]['hosts'].append({"fqdn": "data-%s.uddev.unraveldata.com" % n})
        else:
            if self.options.node > 4:
                for n in range(5, self.options.node + 1):
                    self.host_mapping['host_groups'][2]['hosts'].append({"fqdn": "data-%s.uddev.unraveldata.com" % n})

        if self.options.version_def:
            version_xml = {
                "2.6.5": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.5.0/HDP-2.6.5.0-292.xml",
                "2.6.4": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.4.0/HDP-2.6.4.0-91.xml",
                "2.6.3": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.3.0/HDP-2.6.3.0-235.xml",
                "2.6.2": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.2.14/HDP-2.6.2.14-5.xml",
                "2.6.1": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.1.0/HDP-2.6.1.0-129.xml",
                "2.6.0": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.0.3/HDP-2.6.0.3-8.xml",
                "2.5.3": "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.5.3.0/HDP-2.5.3.0-37.xml",
                "3.0.0": "http://public-repo-1.hortonworks.com/HDP/centos7/3.x/updates/3.0.0.0/HDP-3.0.0.0-1634.xml",
                "3.0.1": "http://public-repo-1.hortonworks.com/HDP/centos7/3.x/updates/3.0.1.0/HDP-3.0.1.0-187.xml",
                "3.1.0": "http://public-repo-1.hortonworks.com/HDP/centos7/3.x/updates/3.1.0.0/HDP-3.1.0.0-78.xml"}
            for version, xml_url in version_xml.iteritems():
                if self.options.hdp_version.startswith(version):
                    self.ver_def['VersionDefinition']['version_url'] = xml_url
                    break


def main():
    hdp = Hdp_cluster()

    hdp.create_cluster()

    while True:
        if hdp.check_process() == 'No Running':
            break
        print('Installing Services')
        time.sleep(60)

    print('\nHDP Installation Completed')


if __name__ == '__main__':
    main()
# curl -u admin:admin -H 'X-Requested-By : Unravel' -X POST http://localhost:8080/api/v1/blueprints/HDP -d @blueprints/blueprint.json
# curl -u admin:admin -H 'X-Requested-By: Unravel' -d @blueprints/repo.json -X POST http://localhost:8080/api/v1/stacks/:stack/versions/:stackVersion/operating_systems/:osType/repositories/:repoId
# curl -u admin:admin -H 'X-Requested-By : Unravel' -X POST http://localhost:8080/api/v1/clusters/:clustername -d @blueprints/cluster.json
# Reference: https://cwiki.apache.org/confluence/display/AMBARI/Blueprints
# https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.0.0/bk_ambari-release-notes/content/ambari_relnotes-2.6.0.0-behavioral-changes.html

#curl  -v -u admin:admin -H 'X-Requested-By: Ambari' -d @blueprints/repo.json -X POST http://52.204.158.41:8080/api/v1/version_definitions/
#"version_url":"http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.5.0/HDP-2.6.5.0-292.xml"
#"version_url":"http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.4.0/HDP-2.6.4.0-91.xml"
#"version_url":"http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.3.0/HDP-2.6.3.0-235.xml"
#"version_url": "http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.6.2.14/HDP-2.6.2.14-5.xml"
#"version_url": "http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.6.1.0/HDP-2.6.1.0-129.xml"
#"version_url": "http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.6.0.3/HDP-2.6.0.3-8.xml"
#"version_url":"http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.5.3.0/HDP-2.5.3.0-37.xml"