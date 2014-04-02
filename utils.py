import os


def current_dir():
    return os.path.split(os.path.abspath(__file__))[0]


def make_folder(out_folder):
    """
    Creates a folder, falls through if folder already exists
    """
    try:
        os.makedirs(out_folder)
        print "created folder %s" % out_folder
    except OSError, e:
        if e.errno != 17:
            raise
