#!/bin/bash

# runs.csv
echo "image_name, scenario_name, is_executing_exploit, warmup_time, recording_time, exploit_start_time" > data/runs.csv
norm_count=10
for i in $(seq $norm_count); do
	prefix="normal_"${i}
	echo "log4j, "$prefix", False, 10, 30, -1" >> data/runs.csv
done
exp_count=200
for i in $(seq $exp_count); do
	prefix="exploit_"${i}
	echo "log4j, "$prefix", True, 10, 30, 10" >> data/runs.csv
done

# normal 
for i in $(seq $norm_count); do
	fn_prefix="data/normal_"${i}
	sudo ../start_server.sh &
	sleep 5
	sudo sysdig container.name=victim and evt.type!=futex and evt.type!=switch -w data/normal.scap -s 80 --unbuffered &
	sleep 2
	python3 normal.py
	sudo docker stop victim
	sudo pkill chrome
	sudo pkill sysdig
	sudo sysdig -r data/normal.scap -p"%evt.num %evt.time %evt.cpu %evt.cpu %proc.name %thread.tid %evt.dir %evt.type %evt.args" > $fn_prefix.txt
	rm -f data/normal.scap
done

# exploit
# for i in $(seq $exp_count); do
# 	fn_prefix="data/exploit_"${i}
# 	sudo ../start_server.sh &
# 	sleep 5
# 	sudo sysdig container.name=victim and evt.type!=futex and evt.type!=switch -w data/exploit.scap -s 80 --unbuffered &
# 	sleep 2
# 	python3 normal.py &
# 	../start_poc.sh &
# 	sleep 3
# 	./exploit.sh
# 	sudo docker stop victim
# 	sudo pkill chrome
# 	sudo pkill sysdig
# 	sudo pkill java 
# 	sudo pkill python3 
# 	sudo pkill start_poc.sh 
# 	sudo pkill nc
# 	sudo sysdig -r data/exploit.scap -p"%evt.num %evt.time %evt.cpu %evt.cpu %proc.name %thread.tid %evt.dir %evt.type %evt.args" > $fn_prefix.txt
# 	rm -f data/exploit.scap
# done
