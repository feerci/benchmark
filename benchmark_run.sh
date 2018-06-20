#!/usr/bin/env bash
echo "type,name,time,size,round,eer,eer_calced,ci_min,ci_max"

python benchmark_speed.py
python benchmark_accuracy.py