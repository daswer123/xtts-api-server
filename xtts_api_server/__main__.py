import uvicorn
from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Run the Uvicorn server.")
parser.add_argument("-hs", "--host", default="localhost", help="Host to bind")
parser.add_argument("-p", "--port", default=8020, type=int, help="Port to bind")
parser.add_argument("-sf", "--speaker_folder", default="speakers/", type=str, help="The folder where you get the samples for tts")
parser.add_argument("-o", "--output", default="output/", type=str, help="Output folder")

args = parser.parse_args()

os.environ['OUTPUT'] = args.output  # Set environment variable for output folder.
os.environ['SPEAKER'] = args.speaker_folder  # Set environment variable for speaker folder.
os.environ['BASE_URL'] = "http://" + args.host + ":" + str(args.port)  # Set environment variable for base url."

from xtts_api_server.server import app

uvicorn.run(app, host=args.host, port=args.port)