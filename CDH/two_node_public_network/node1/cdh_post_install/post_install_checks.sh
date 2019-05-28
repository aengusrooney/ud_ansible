#Force NN to leave safemode
#echo "Force NameNode to leave SafeMode"
#sudo -u hdfs hdfs dfsadmin -safemode leave
#Create hive table
echo '################################################'
echo          Hive 
echo '################################################'
echo "Creating hive table"
hive -f /vagrant/cdh_post_install/create_table.sql

#Create HDFS file
echo '################################################'
echo              HDFS 
echo '################################################'
echo "Create file in hdfs"
echo "1 input file received" > /tmp/test
sudo -u hdfs hadoop fs -put /tmp/test /user/hive/warehouse/tstin/

#Get data
echo '################################################'
echo              Hive Query 
echo '################################################'
echo "Issuing a Hive Query"
sudo -u hdfs hive -f /vagrant/cdh_post_install/query_hive.sql

#Get data from impala
echo '################################################'
echo              IMPALA
echo '################################################'
echo "Get data using Impala"
impala-shell -f /vagrant/cdh_post_install/query_impala.sql

#Run map-reduce 
echo '################################################'
echo             Map-Reduce 
echo '################################################'
echo "Run a Map reduce job"
sudo -u hdfs hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar pi 1 1

#Run Hbase
#echo "Executing Hbase commands"
#sudo -u hdfs hbase shell hbase_cmds.txt

#Run spark job
#echo "this is the end. the only end. my friend." > /tmp/sparkin
#sudo -u hdfs hadoop fs -put /tmp/sparkin /tmp/
#spark-shell -i word_count.sc
#sudo -u hdfs hadoop fs -cat /tmp/sparkout
echo '################################################'
echo                 Spark
echo '################################################'
echo "Run Spark App"
sudo -u hdfs spark-submit --class org.apache.spark.examples.SparkPi --master yarn --deploy-mode cluster /opt/cloudera/parcels/CDH/lib/spark/lib/spark-examples.jar  2
