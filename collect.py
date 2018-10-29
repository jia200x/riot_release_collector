from glob import glob
import argparse
import os
import sys
import json
import requests
import configparser

CONFIG_FILE = "config.ini"
POST_URL="https://elk.inet.haw-hamburg.de/post/"
config = configparser.ConfigParser()


def get_access_token(args):
    if hasattr(args, "access_token") and args.access_token:
        if "GitHub" in config:
            config["GitHub"]["access_token"] = args.access_token
        else:
            config["GitHub"] = {"access_token": args.access_token}
        return args.access_token
    else:
        if "GitHub" in config:
            return config["GitHub"].get("access_token")
        else:
            return None


def fetch_logs(result_directory, release_candidate):
    files = glob(os.path.join(result_directory, "*/*/*/*"))
    results = []

    toolchain_file = open(os.path.join(result_directory, "toolchain"), 'r')
    toolchain = toolchain_file.read()
    toolchain_file.close()

    for f in files:
        res = os.path.relpath(f, result_directory).split("/")
        sd = res[3].split(".", 1)

        content_file = open(f, 'r')
        content = content_file.read()
        content_file.close()

        data = dict(board=res[0],
                    concept=res[1],
                    module=res[2],
                    type=sd[0],
                    detail=sd[1],
                    log=content,
                    release_candidate=release_candidate,
                    toolchain=toolchain)

        results.append(data)
    return results


def post_results(access_token, results):
    data = {"token": access_token,
            "results": results}

    request = requests.post(POST_URL, json.dumps(data),
                            headers={'Content-type': 'application/json',
                                     'Accept': 'text/plain'})

    if request.status_code == 200:
        print("Successfully received logs. Thank you")
    else:
        print("There was an error (Wrong token?)")
        sys.exit(1)


def main():
    try:
        config.read(CONFIG_FILE)
    except FileNotFoundError:
        pass

    p = argparse.ArgumentParser()
    p.add_argument('result_directory', nargs='?',
                   help='Result directory, by default "results"')

    p.add_argument('release_candidate', nargs='?', type=int,
                   help='Release Candidate number')

    p.add_argument("-t", "--access-token",
                   help="Github access token (create one at " +
                        "https://github.com/settings/tokens with access " +
                        "(repo, admin:gpg_key) if required)")

    args = p.parse_args()
    result_directory = args.result_directory
    if not result_directory:
        print("No result directory given\n")
        p.print_help()
        sys.exit(1)

    release_candidate = args.release_candidate
    if not release_candidate:
        print("No Release Candidate given\n")
        p.print_help()
        sys.exit(1)

    access_token = get_access_token(args)
    if not access_token:
        print("No access token found\n")
        p.print_help()
        sys.exit(1)

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

    results = fetch_logs(result_directory, release_candidate)
    post_results(access_token, results)


if __name__ == "__main__":
    main()

