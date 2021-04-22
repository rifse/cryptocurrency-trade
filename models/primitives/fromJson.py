import json
import os

def load(relative_path):  # must be relative (start with ../) 
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, relative_path)
    dataDict = {}
    try:
        with open(file_path, 'r') as inFile:
            dataDict = json.load(inFile)  # dict of static local data
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        return dataDict
