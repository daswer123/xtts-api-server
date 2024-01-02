import os
import subprocess
import sys
import requests

import importlib.metadata as metadata  # Use importlib.metadata
from pathlib import Path
from tqdm import tqdm

from packaging import version
from loguru import logger


def create_directory_if_not_exists(directory):
    if not directory.exists():
        directory.mkdir(parents=True)

def download_file(url, destination):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(destination, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

def install_package(package_link):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_link])

def is_package_installed(package_name):
    try:
        metadata.version(package_name)
        return True
    except metadata.PackageNotFoundError:
        return False

def install_deepspeed_based_on_python_version():
    # check_and_install_torch()
    if not is_package_installed('deepspeed'):
        python_version = sys.version_info

        logger.info(f"Python version: {python_version.major}.{python_version.minor}")

        # Define your package links here
        py310_win = "https://github.com/daswer123/xtts-webui/releases/download/deepspeed/deepspeed-0.11.2+cuda118-cp310-cp310-win_amd64.whl"
        py311_win = "https://github.com/daswer123/xtts-webui/releases/download/deepspeed/deepspeed-0.11.2+cuda118-cp311-cp311-win_amd64.whl"

        # Use generic pip install deepspeed for Linux or custom wheels for Windows.
        deepspeed_link = None

        if sys.platform == 'win32':
            if python_version.major == 3 and python_version.minor == 10:
                deepspeed_link = py310_win

            elif python_version.major == 3 and python_version.minor == 11:
                deepspeed_link = py311_win

            else:
                logger.error("Unsupported Python version on Windows.")

        else: # Assuming Linux/MacOS otherwise (add specific checks if necessary)
             deepspeed_link = 'deepspeed'

        if deepspeed_link:
             logger.info("Installing DeepSpeed...")
             install_package(deepspeed_link)

    # else:
        #  logger.info("'deepspeed' already installed.")

def upgrade_tts_package():
    try:
        logger.warning("TTS version is outdated, attempting to upgrade TTS...")
        subprocess.check_call([sys.executable, "-m", "pip", "install","-q", "--force-reinstall","--no-deps", "tts==0.21.3"])
        logger.info("TTS has been successfully upgraded ")
    except Exception as e:
        logger.error(f"An error occurred while upgrading TTS: {e}")
        logger.info("Try installing the new version manually")
        logger.info("pip install --upgrade tts")


def upgrade_stream2sentence_package():
    try:
        logger.warning("Stream2sentence version is outdated, attempting to upgrade stream2sentence...")
        subprocess.check_call([sys.executable, "-m", "pip", "install","-q", "--upgrade", "stream2sentence"])
        logger.info("Stream2sentence has been successfully upgraded ")
    except Exception as e:
        logger.error(f"An error occurred while upgrading Stream2sentence: {e}")
        logger.info("Stream2sentence installing the new version manually")
        logger.info("pip install --upgrade stream2sentence")

def check_tts_version():
    try:
        tts_version = metadata.version("tts")
        # print(f"[XTTS] TTS version: {tts_version}")

        if version.parse(tts_version) != version.parse("0.21.3"):
            upgrade_tts_package()
            # print("[XTTS] TTS version is too old. Please upgrade to version 0.21.2 or later.")
            # print("[XTTS] pip install --upgrade tts")
        # else:
            # logger.info("TTS version is up to date.")
    except metadata.PackageNotFoundError:
        print("TTS is not installed.")


def check_stream2sentence_version():
    try:
        tts_version = metadata.version("stream2sentence")
        if version.parse(tts_version) < version.parse("0.2.2"):
            upgrade_stream2sentence_package()
    except metadata.PackageNotFoundError:
        print("stream2sentence is not installed.")

def download_model(this_dir,model_version):
    # Define paths
    base_path = this_dir
    model_path = base_path / f'{model_version}'

    # Define files and their corresponding URLs
    files_to_download = {
         "config.json": f"https://huggingface.co/coqui/XTTS-v2/raw/{model_version}/config.json",
         "model.pth": f"https://huggingface.co/coqui/XTTS-v2/resolve/{model_version}/model.pth?download=true",
         "vocab.json": f"https://huggingface.co/coqui/XTTS-v2/raw/{model_version}/vocab.json",
         "speakers_xtts.pth": "https://huggingface.co/coqui/XTTS-v2/resolve/main/speakers_xtts.pth?download=true"
    }

    # Check and create directories
    create_directory_if_not_exists(base_path)
    create_directory_if_not_exists(model_path)

    # Download files if they don't exist
    for filename, url in files_to_download.items():
         destination = model_path / filename
         if not destination.exists():
             print(f"[XTTS] Downloading {filename}...")
             download_file(url, destination)

# if __name__ == "__main__":
#    this_dir = Path(__file__).parent.resolve()
#    main_downloader(this_dir)