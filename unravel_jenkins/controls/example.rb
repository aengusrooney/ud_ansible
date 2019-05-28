# encoding: utf-8
# copyright: 2018, DevOps@unravel

# List of installed software on Jenkins Master #
packages = { "mvn --version" => "3.5.4", "ruby --version" => "2.0.0p648", "/opt/bin/git --version" => "2.1", "node --version" => "6.1", "/usr/local/bin/python --version" => "3.5.6", "/opt/apache-tomcat-7.0.92/bin/catalina.sh version" => "7.0.92", "java -jar /usr/lib/jenkins/jenkins.war  --version" => "2.1", "java -version" => '1.8.0_192' }

# Check if Jenkins & Tomcat are up #
urls = { "http://172.16.1.205:8080" => "Welcome to Jenkins!" , "http://172.16.1.205:8090" => "Apache Tomcat" }

title 'Unravel Jenkins Post Deploy Tests'

  describe os.family do
    it { should eq 'redhat' }
  end

  describe os.name do
    it { should eq 'centos' }
  end

  describe os.arch do
    it { should eq 'x86_64' }
  end

packages.each do |cmd, ver|
  #puts(cmd, ver)
  describe command(cmd) do
    if cmd =~ /java -version/
      its('stderr') { should match /#{ver}/ }
    else
      its('stdout') { should match /#{ver}/ }
    end
    its('exit_status') { should eq 0 }
  end
end

urls.each do |url, welcome_str|
  describe http(url) do
  its('status') { should cmp 200 }
  its('body') { should match /#{welcome_str}/ }
  end
end
