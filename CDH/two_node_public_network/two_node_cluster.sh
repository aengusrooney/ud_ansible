#!/usr/bin/env bash

echo "Creating 2 node cluster woth Public IPs"

echo "Creating node1 ...."

cd node1; nohup vagrant up  > ../node1.log &

cd ..

echo "Check node1.log for progress"

echo "Creating node2 ...."


cd node2; nohup vagrant up > ../node2.log &

cd ..

echo "Check node2.log for progress"
