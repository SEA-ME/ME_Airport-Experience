#!/bin/bash

source ~/env/bin/activate

python ~/mycar/manage.py drive --model ~/mycar/models/mypilot_pruned.tflite --type tflite_linear
