#!/bin/bash
# Add CUDA to PATH if the directory exists
if [ -d "/usr/local/cuda-12.8/bin" ]; then
  export PATH="/usr/local/cuda-12.8/bin:$PATH"
fi

cd /home/dwemer/xtts-api-server/

source /home/dwemer/python-tts/bin/activate

# Add CUDA to PATH if the directory exists
if [ -d "/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/lib/" ];
then
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/lib/
  export PATH=/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/bin:$PATH
  export CUDA_HOME=/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13
fi

python -m xtts_api_server --deepspeed --listen &> log.txt &



