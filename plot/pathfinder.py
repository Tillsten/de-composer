#!/usr/bin/epython

import sys
import os.path
import random

def find():
    p = os.path.realpath(__file__)
    q = os.path.split(os.path.dirname(p))
    sys.path.append(os.path.join(q[0], "src"))
    
    return None
