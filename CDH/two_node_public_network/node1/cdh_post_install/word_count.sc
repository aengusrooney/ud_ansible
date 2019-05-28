val file = sc.textFile("hdfs://tnode1.unraveldata.com:8020/tmp/sparkin")
val counts = file.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_ + _)
counts.saveAsTextFile("hdfs://tnode1.unraveldata.com:8020/tmp/sparkout1")
