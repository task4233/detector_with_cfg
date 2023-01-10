import sys
import os
from detector_with_cfg import classifier

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"you should set a depth of decision tree")
        os.exit(1)
    depth = int(sys.argv[1])
    classifier.Classifier(depth).classify()
