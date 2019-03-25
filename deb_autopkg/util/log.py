from sys import stderr

def info(text):
    stderr.write("[INFO] "+text+"\n")

def warn(text):
    stderr.write("[WARN] "+text+"\n")
