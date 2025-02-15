#!/usr/bin/python3
import os

def run() -> str:
    print("Running ls module")
    data = '\n'.join(os.listdir('.'))  # Get contents of a directory
    return data
