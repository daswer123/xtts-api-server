import uvicorn
from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Run the Uvicorn server.")
parser.add_argument("-hs", "--host", default="localhost", help="Host to bind")
parser.add_argument("-p", "--port", default=8020, type=int, help="Port to bind")
parser.add_argument("-sf", "--speaker_folder", default="speakers/", type=str, help="The folder where you get the samples for tts")
parser.add_argument("-o", "--output", default="output/", type=str, help="Output folder")
parser.add_argument("-t", "--tunnel", default="", type=str, help="URL of tunnel used (e.g: ngrok, localtunnel)")
parser.add_argument("-ms", "--model-source", default="local", choices=["repo", "local"],
                    help="Define the model source: 'repo' for latest version from repository or 'local' for using local files and model v2.0.2.")
args = parser.parse_args()

os.environ['OUTPUT'] = args.output  # Set environment variable for output folder.
os.environ['SPEAKER'] = args.speaker_folder  # Set environment variable for speaker folder.
os.environ['BASE_URL'] = "http://" + args.host + ":" + str(args.port)  # Set environment variable for base url."
os.environ['TUNNEL_URL'] = args.tunnel  # it is necessary to correctly return correct previews in list of speakers
os.environ['MODEL_SOURCE'] = args.model_source  # Set environment variable for the model source

from xtts_api_server.server import app

uvicorn.run(app, host=args.host, port=args.port)