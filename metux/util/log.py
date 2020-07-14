from sys import stderr

color_normal = "\033[0;32;39m"
color_yellow = "\033[1;32;33m"
color_green  = "\033[1;32;40m"
color_cyan   = "\033[1;32;36m"
color_red    = "\033[1;32;91m"

def _wr(prefix, color, text):
    stderr.write("%s%5s%s %s\n" % (color, prefix, color_normal, text))

def info(text):
    _wr("INFO:", color_green, text)

def warn(text):
    _wr("WARN:", color_yellow, text)

def err(text):
    _wr("ERR:", color_red, text)

def debug(text):
    _wr("DBG:", color_cyan, text)
