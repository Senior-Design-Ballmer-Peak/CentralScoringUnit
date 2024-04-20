#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate

pip install requests
pip install numpy
pip install opencv-python