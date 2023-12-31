import argparse
import multiprocessing as mp
from os import mkdir, path


def init_parser():
    parser = argparse.ArgumentParser(
        description="Python package that downloads files from common \
        crawler's database.\n \
        An example usage is `ftf.py -l 5 -f jpg png -o out_dir` \n  \
        This'll make it download 5 jpgs and 5 pngs into out_dir"
    )

    parser.add_argument(
        "-l",
        "--limit",
        help="Max number of files to download (for each filetype)",
        required=True,
        metavar="<limit>",
        type=int,
    )

    parser.add_argument(
        "-f",
        "--filetypes",
        help="Desired filetypes to fetch. "
        + "NOTE: check the config file: filetype_config.json, "
        + "if the desired filetype is in there, "
        + "make sure the filetype passed in lines up. "
        + "Put in '*' for all filetypes",
        required=True,
        nargs="+",
        type=str,
    )

    parser.add_argument(
        "-p",
        "--num_procs",
        help="Number of processes to use, default is 1",
        required=False,
        default=1,
        type=int,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory to store downloaded files",
        required=True,
        type=str,
    )

    parser.add_argument(
        "-t",
        "--tolerance",
        help="Number of fails for a given hostname before we ignore this host",
        required=False,
        type=int,
        default=10,
    )

    parser.add_argument(
        "--log",
        help="Log file to store debug and error messages",
        required=False,
        type=str,
        default="cmoncrawl.log",
    )

    return parser


# returns 0 on success, returns 1 on fail
def validate_args(args):
    if args.limit <= 0:
        print("Limit (-l,--limit) must be a positive number")
        return -1

    # if they want more processes than what's detected
    if args.num_procs > mp.cpu_count():
        print(
            "Too many processes, multiprocessing library detected only "
            + str(mp.cpu_count())
            + " cores"
        )
        return -1

    # create output directory if it doesn't exist
    if not path.exists(args.output):
        try:
            mkdir(args.output)
        except FileNotFoundError:
            print("Output directory (-o,--output) is an invalid file path")
            return -1
        except Exception as err:
            print("Error trying to create output directory (-o,--output)")
            print(err)
            return -1

    # verify output directory is a directory
    if not path.isdir(args.output):
        print("Expected output (-o,--output) to be a directory")
        return -1

    if args.output[-1] != "/":
        args.output += "/"
    return 0

    if args.tolerance <= 0:
        print(
            "Dude how can the tolerance (-t, --tolerance)  be <= 0? "
            + "It's the number of failed download attempts from "
            + "a given hostname before we skip files from that hostname."
        )
        return -1


def get_validated_args():
    # initialize parser and parse arguments using argparse library
    parser = init_parser()
    args = parser.parse_args()

    if validate_args(args) == -1:
        print("validate_args() has failed")
        return -1

    return args
