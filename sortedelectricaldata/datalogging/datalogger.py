import numpy as np
import time
import os

def create_file_path(sampleID):
    if sampleID = None:
        sampleID = "unlabeled"

    if os.path.exists("Data/sampleID"):
        pass
    else:
        os.makedirs("Data/sampleID")