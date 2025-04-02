from os.path import join as joinpath, dirname

def load_template_str(relpath:str) -> str:
    """
    Because this service is not in the root of the project the flask template
    loading does not work as desired so we do it in a cruder way.
    """
    fullpath = joinpath(dirname(__file__), relpath)
    return load_str(fullpath)


def load_str(filepath:str) -> str:
    """
    Load file to string.
    """
    with open(filepath, 'r') as f:
        return f.read()
