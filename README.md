# RIOT Release collector

This scripts collect the output from [09-compile-and-test-one-board](https://github.com/RIOT-OS/Release-Specs/blob/master/02-tests/compile_and_test_for_board.py) and send it to a Log Server (located at HAW Hamburg).
I took some snippets from the [RIOT Release Manager tool](https://github.com/RIOT-OS/RIOT-release-manager/blob/master/riot_release_manager.py)

# Requirements
- Python > 3.5
- Glob3


# Usage
```
usage: collect.py [-h] [-t ACCESS_TOKEN]
                  [result_directory] [release_candidate]

positional arguments:
  result_directory      Result directory
  release_candidate     Release Candidate number

optional arguments:
  -h, --help            show this help message and exit
  -t ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        Github access token (create one at
                        https://github.com/settings/tokens with access (repo,
                        admin:gpg_key) if required)
```

E.g for uploading tests results from RC-1
```
collect.py /tmp/results 1
```

Data is signed with a Github account, so it's necessary to create a personal token. See [Creating a personal token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)

# WARNING
- This script will upload **ALL** boards present in the `results` folder. Since there's no duplication detection in the log server, please create and upload a **new** `results` folder after every time data is uploaded successfully.
- The folders under `results` folder have to preserve their structure and naming convention (e.g don't change board names, move files, etc).

# Limitations and future work

- Timestamp is set on upload. It should be obtained by time when tests were ran.
- The `09-compile-and-test-one-board` script generates all boards in the same `results` folder. **Take this into consideration, otherwise there might be duplicated uploads!**
- Automatic RC tagging is not (yet) supported. Be careful to specify the proper RC number.

Happy hacking! And thank you for helping us testing RIOT :)
