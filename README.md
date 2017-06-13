# findmyboard
A way to find my test machines.

The script to grep out board details from the lab dhcp webpage. The assigned
ip/mac/sys details can be retrieved using the script. It is also possible to do
the partial string search on ip/mac/hostnames.
It is very useful to collect the host details over terminal without any GUI/
browser.

The commandline synatx would be

```
    $ ./findmyboard.py --help
    usage: findmyboard.py [-h] [-V] [-ip IPADDR] [-mac MACADDR] [-n NAME] [-a]

    findmyboard -- Find the board with its name/IP/MAC

      Created by Sugesh Chandran on 2017-06-12.

      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0

      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.

    USAGE

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -ip IPADDR            Ip address of the board to search(partial search is
                            allowed).
      -mac MACADDR          Mac address of the board to search(partial search is
                            allowed).
      -n NAME, --name NAME  Hostname of the board to search(partial search is
                            allowed).
      -a, --all             Find all matches for the given input.
```
