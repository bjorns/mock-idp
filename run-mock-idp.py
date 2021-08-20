#!/usr/bin/env python3
import sys

from mockidp.main import main

if __name__ == '__main__':
    try:
        print("Launching main")
        main(sys.argv)
    except KeyboardInterrupt as e:
        sys.exit(-1)

