from argparse import ArgumentParser

from usergroups.app import app
from usergroups import api

if __name__ == "__main__":

    parser = ArgumentParser(description="Runtime args")
    parser.add_argument("-p", "--port", default=5000, dest="port", type=int, help="Port to run on")

    args = parser.parse_args()
    app.run(host='0.0.0.0', debug=True, port=args.port)