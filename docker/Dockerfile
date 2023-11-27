FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

LABEL description="Docker image for xtts-api-server"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,rw apt-get update && \
    apt-get install --no-install-recommends -y python3-dev libportaudio2 libasound-dev git python3 python3-pip make g++ ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip,rw pip3 install virtualenv

RUN --mount=type=cache,target=/root/.cache/pip,rw \
    pip3 install --upgrade pip setuptools wheel ninja && \
    pip3 install torch torchvision torchaudio xformers --index-url https://download.pytorch.org/whl/cu121 

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN --mount=type=cache,target=/root/.cache/pip,rw \ 
    pip3 install /app 

EXPOSE ${CONTAINER_PORT:-8020} ${CONTAINER_API_PORT:-8020}
# echo 'y' is to accept coqui tts model download terms
CMD echo "y" | python3 -m xtts_api_server -hs 0.0.0.0 -sf ${EXAMPLE_FOLDER:-"/app/example"} -t ${TUNNEL:-"http://localhost:8020"} -p ${CONTAINER_PORT:-8020}  -ms ${MODEL_SOURCE:-"apiManual"}
