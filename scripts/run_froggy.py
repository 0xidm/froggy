#!/usr/bin/env python

import time

from dotenv import load_dotenv
load_dotenv()

from froggy import Froggy

while True:
    try:
        Froggy().run()
    except Exception as e:
        print(e)
        time.sleep(5)
