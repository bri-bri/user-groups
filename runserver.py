from argparse import ArgumentParser

from usergroups.app import app, logger
from usergroups import api

if __name__ == "__main__":

    parser = ArgumentParser(description="Runtime args")
    parser.add_argument("-p", "--port", dest="port", type=int, help="Port to run on")
    parser.add_argument("--log-level", type=int, help="Override log level (10 for DEBUG)")

    args = parser.parse_args()
    port = getattr(args, 'port', app.config['PORT'])

    app.run(host='0.0.0.0', debug=True, port=args.port)