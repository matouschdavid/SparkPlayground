import sys

from batch_main import batch_main
from stream_main import stream_main


def handle_batch():
    print("Batch function called.")

def handle_other():
    print("Other function called.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "batch":
            batch_main()
        else:
            stream_main()
    else:
        print("No argument provided.")
