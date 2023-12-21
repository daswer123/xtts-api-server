import uvicorn
from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Run the Uvicorn server.")
parser.add_argument("-hs", "--host", default="localhost", help="Host to bind")
parser.add_argument("-p", "--port", default=8020, type=int, help="Port to bind")
parser.add_argument("-d", "--device", default="cuda", type=str, help="Device that will be used, you can choose cpu or cuda")
parser.add_argument("-sf", "--speaker_folder", default="speakers/", type=str, help="The folder where you get the samples for tts")
parser.add_argument("-o", "--output", default="output/", type=str, help="Output folder")
parser.add_argument("-t", "--tunnel", default="", type=str, help="URL of tunnel used (e.g: ngrok, localtunnel)")
parser.add_argument("-ms", "--model-source", default="local", choices=["api","apiManual", "local"],
                    help="Define the model source: 'api' for latest version from repository, apiManual for 2.0.2 model and api inference or 'local' for using local inference and model v2.0.2.")
parser.add_argument("-v", "--version", default="v2.0.2", type=str, help="You can specify which version of xtts to use,This version will be used everywhere in local, api and apiManual.")
parser.add_argument("--lowvram", action='store_true', help="Enable low vram mode which switches the model to RAM when not actively processing.")
parser.add_argument("--deepspeed", action='store_true', help="Enables deepspeed mode, speeds up processing by several times.")
parser.add_argument("--use-cache", action='store_true', help="Enables caching of results, your results will be saved and if there will be a repeated request, you will get a file instead of generation.")
parser.add_argument("--streaming-mode", action='store_true', help="Enables streaming mode, currently needs a lot of work.")
parser.add_argument("--streaming-mode-improve", action='store_true', help="Includes an improved streaming mode that consumes 2gb more VRAM and uses a better tokenizer, good for languages such as Chinese")
parser.add_argument("--stream-play-sync", action='store_true', help="Additional flag for streaming mod that allows you to play all audio one at a time without interruption")

args = parser.parse_args()

os.environ['DEVICE'] = args.device  # Set environment variable for output folder.
os.environ['OUTPUT'] = args.output  # Set environment variable for output folder.
os.environ['SPEAKER'] = args.speaker_folder  # Set environment variable for speaker folder.
os.environ['BASE_URL'] = "http://" + args.host + ":" + str(args.port)  # Set environment variable for base url."
os.environ['TUNNEL_URL'] = args.tunnel  # it is necessary to correctly return correct previews in list of speakers
os.environ['MODEL_SOURCE'] = args.model_source  # Set environment variable for the model source
os.environ["MODEL_VERSION"] = args.version # Specify version of XTTS model
os.environ["USE_CACHE"] = str(args.use_cache).lower() # Set lowvram mode
os.environ["DEEPSPEED"] = str(args.deepspeed).lower() # Set lowvram mode
os.environ["LOWVRAM_MODE"] = str(args.lowvram).lower() # Set lowvram mode
os.environ["STREAM_MODE"] = str(args.streaming_mode).lower() # Enable Streaming mode
os.environ["STREAM_MODE_IMPROVE"] = str(args.streaming_mode_improve).lower() # Enable improved Streaming mode
os.environ["STREAM_PLAY_SYNC"] = str(args.stream_play_sync).lower() # Enable Streaming mode



from xtts_api_server.server import app

uvicorn.run(app, host=args.host, port=args.port)