FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
LABEL description="Docker image for xtts-api-server"

# Set default values for environment variables if they are not provided
ENV HOST="localhost" \
    PORT=8020 \
    DEVICE="cuda" \
    SPEAKER_FOLDER="/app/speakers/" \
    OUTPUT="/app/output/" \
    TUNNEL="" \
    MODEL_FOLDER="/app/xtts_models/" \
    MODEL_SOURCE="local" \
    VERSION="v2.0.2" \
    LISTEN=false \
    LOWVRAM=false \
    DEEPSPEED=false \
    USE_CACHE=false \
    STREAMPLAYSYNC=false

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,rw apt-get update && \
    apt-get install --no-install-recommends -y python3-dev portaudio19-dev libportaudio2 libasound2-dev libportaudiocpp0 git python3 python3-pip make g++ ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip,rw pip3 install virtualenv

RUN --mount=type=cache,target=/root/.cache/pip,rw \
    pip3 install --upgrade pip setuptools wheel ninja && \
    pip3 install torch torchaudio --index-url https://download.pytorch.org/whl/cu118 \
    pip3 install deepspeed==12.4

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN --mount=type=cache,target=/root/.cache/pip,rw \ 
    pip3 install /app 

EXPOSE ${CONTAINER_PORT:-8020} ${CONTAINER_API_PORT:-8020}
# echo 'y' is to accept coqui tts model download terms
CMD python3 -m xtts_api_server -sf ${EXAMPLE_FOLDER:-"/app/speakers"} --deepspeed