#!/bin/bash

echo "=== CHIM XTTS Installation ==="
echo ""
echo "NOTE: CHIM XTTS and Chatterbox use the same port (8020)."
echo "      Only one can be enabled at a time."
echo ""

cd /home/dwemer/xtts-api-server
python3 -m venv /home/dwemer/python-tts
source /home/dwemer/python-tts/bin/activate


PIDS=$(lsof -ti:8020)
if [ -n "$PIDS" ]; then
    echo "Killing processes listening on port 8020: $PIDS"
    kill -9 $PIDS
fi


echo "This will take a while so please wait."

read -p "Do you want to perform a clean install? (yes/no): " clean_install
if [[ "$clean_install" =~ ^[Yy][Ee][Ss]$ || "$clean_install" =~ ^[Yy]$ ]]; then
    rm -fr /home/dwemer/python-tts/*
	python3 -m venv /home/dwemer/python-tts
    source /home/dwemer/python-tts/bin/activate
fi

# Clean previous deepspeed stuff
rm /home/dwemer/.cache/torch_extensions/py311_cu130/transformer_inference/*
# Ask user about GPU
read -p "Are you using a GT10XX series GPU? (yes/no): " gpu_answer
if [[ "$gpu_answer" =~ ^[Yy][Ee][Ss]$ || "$gpu_answer" =~ ^[Yy]$ ]]; then
    cu_tag="cu118"
    torch_url="https://download.pytorch.org/whl/${cu_tag}"
    torch_ver="2.2.2"
    torchaudio_ver="2.2.2"
    python3 -m pip install --upgrade pip wheel ninja virtualenv
    pip install setuptools==68.1.2
    # Install app requirements without auto-pulling torch/torchaudio from deps
    pip install --no-deps -r requirements.txt
    # Pin to stable, CUDA-tagged PyTorch/Torchaudio that do not require TorchCodec
    pip cache purge || true
    pip uninstall -y torch torchaudio torchcodec torchvision || true
    pip install --no-deps --no-cache-dir --index-url "$torch_url" "torch==${torch_ver}+${cu_tag}" "torchaudio==${torchaudio_ver}+${cu_tag}"
    pip check || true
    # Ensure fallback audio loader is available
    pip install --no-cache-dir soundfile
    sed -i 's/checkpoint = load_fsspec(model_path, map_location=torch.device("cpu"))\["model"\]/checkpoint = load_fsspec(model_path, map_location=torch.device("cpu"), weights_only=False)["model"]/' /home/dwemer/python-tts/lib/python3.11/site-packages/TTS/tts/models/xtts.py

else
    read -p "New: Use CUDA13. Needs windows updated drivers. RTX 50XX should use this. Usey cuda13? (yes/no): " gpu5_answer
    if [[ "$gpu5_answer" =~ ^[Yy][Ee][Ss]$ || "$gpu5_answer" =~ ^[Yy]$ ]]; then
	    cu_tag="cu130"
	    torch_url="https://download.pytorch.org/whl/${cu_tag}"
	    echo "Using torch: $torch_url"
	    python3 -m pip install --upgrade pip wheel ninja virtualenv
	    pip install setuptools==68.1.2
	    # Install app requirements without auto-pulling torch/torchaudio from deps
	    #pip install --no-deps -r requirements5.txt  --index-url=$torch_url
	    pip install -r requirements5.txt  --extra-index-url=https://download.pytorch.org/whl/cu130
	    # Pin to stable, CUDA-tagged PyTorch/Torchaudio that do not require TorchCodec
	    pip check || true
	    # Ensure fallback audio loader is available
	    pip install --no-cache-dir soundfile
        # Fix symlinks
		LIBDIR=$(python3 -c 'import site; print(site.getsitepackages()[0])')/nvidia/cu13/lib
	    for f in "$LIBDIR"/lib*.so.*; do
    	    base=$(basename "$f")
        	link="${f%%.so.*}.so"
            if [ ! -e "$link" ]; then
				echo "Creating symlink: $(basename "$link") -> $base"
				ln -s "$base" "$link"
			fi
		done		
	    #pip install xtts-api-server #Fails

    else
	    cu_tag="cu128"
	    torch_url="https://download.pytorch.org/whl/${cu_tag}"
	    echo "Using torch: $torch_url"
	    python3 -m pip install --upgrade pip wheel ninja virtualenv
	    pip install setuptools==68.1.2
	    # Install app requirements without auto-pulling torch/torchaudio from deps
	    pip install --no-deps -r requirements.txt
	    # Pin to stable, CUDA-tagged PyTorch/Torchaudio that do not require TorchCodec
	    pip cache purge || true
	    pip uninstall -y torch torchaudio torchcodec torchvision || true
	    #pip install --index-url "$torch_url" torch torchaudio torchcodec torchvision 
	    pip install torch==2.7.0+cu128 torchaudio==2.7.0+cu128 torchvision==0.22.0+cu128 --index-url=https://download.pytorch.org/whl/
	    pip check || true
	    # Ensure fallback audio loader is available
	    pip install --no-cache-dir soundfile
	    #pip install xtts-api-server #Fails
	    sed -i 's/checkpoint = load_fsspec(model_path, map_location=torch.device("cpu"))\["model"\]/checkpoint = load_fsspec(model_path, map_location=torch.device("cpu"), weights_only=False)["model"]/' /home/dwemer/python-tts/lib/python3.11/site-packages/TTS/tts/models/xtts.py

    fi
fi


cp /home/dwemer/TheNarrator.wav speakers/TheNarrator.wav

source /home/dwemer/python-tts/bin/activate

./conf.sh

echo 
echo "This will start CHIM XTTS to download the selected model"
echo "Wait for the message 'Uvicorn running on http://0.0.0.0:8020 (Press CTRL+C to quit)'"
echo "Then close this window. Press ENTER to continue"
read

echo "please wait...."

# Add CUDA to PATH if the directory exists
if [ -d "/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/lib/" ];
then
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/lib/
  export PATH=/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13/bin:$PATH
  export CUDA_HOME=/home/dwemer/python-tts/lib/python3.11/site-packages/nvidia/cu13
fi

readlink start.sh | grep -q '/home/dwemer/xtts-api-server/start-deepspeed.sh' && export DEEPSPEED="--deepspeed" ||  export DEEPSPEED=""

python -m xtts_api_server --listen $DEEPSPEED

echo "Press Enter"
