#!/bin/sh
set -eu

TIMES=100

: > bench.dat

n=0
while [ ${n} -lt ${TIMES} ]
do
	seed=$(date +%s%N)
	rtg1=$(./run.py -a 'genetic1' -s "${seed}" | grep '^All that in' | awk '{print $5}')
	rtg2=$(./run.py -a 'genetic2' -s "${seed}" | grep '^All that in' | awk '{print $5}')
	rtg3=$(./run.py -a 'genetic3' -s "${seed}" | grep '^All that in' | awk '{print $5}')
	echo "${n} ${rtg1} ${rtg2} ${rtg3}" | tee -a bench.dat
	n=$((n + 1))
done

sum=$(awk '{print $2}' < bench.dat | tr '\\n' '+' | sed 's/+$//')
mean=$(printf "scale=3\\n(%s)/%s\\n" "${sum}" "${TIMES}" | bc -l)
echo "AlgoGenetic1 : ${mean} seconds (mean time)"

sum=$(awk '{print $3}' < bench.dat | tr '\\n' '+' | sed 's/+$//')
mean=$(printf "scale=3\\n(%s)/%s\\n" "${sum}" "${TIMES}" | bc -l)
echo "AlgoGenetic2 : ${mean} seconds (mean time)"

sum=$(awk '{print $4}' < bench.dat | tr '\\n' '+' | sed 's/+$//')
mean=$(printf "scale=3\\n(%s)/%s\\n" "${sum}" "${TIMES}" | bc -l)
echo "AlgoGenetic3 : ${mean} seconds (mean time)"

./bench.gpi
