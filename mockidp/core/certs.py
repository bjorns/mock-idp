from os.path import join as joinpath, dirname, curdir, exists
from os import mkdir
from subprocess import Popen, PIPE


def _get_certs_dir() -> str:
    """
    Fetch the certs dir as the current runtime directory. This should be
    extended to support a directory in homedir as well.
    """
    path = joinpath(curdir, 'certs')
    if not exists(path):
        mkdir(path)
    return path


def generate_private_key(filename: str) -> str:
    result_file = joinpath(_get_certs_dir(), filename)
    if not exists(dirname(result_file)):
        mkdir(dirname(result_file))
    cmd = Popen(["openssl", "genrsa", "-out", result_file, "2048"],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file


def generate_certificate_signing_request(private_key_file: str, filename: str) -> str:
    result_file = joinpath(_get_certs_dir(), filename)
    if not exists(dirname(result_file)):
        mkdir(dirname(result_file))
    cmd = Popen(["openssl", "req", "-new", "-key", private_key_file, "-out", result_file, "-subj",
                 "/C=US/ST=New York/L=New York City/O=Some Org/OU=Some Department/CN=example.com/emailAddress=charlies@peanuts.com"],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file

def generate_certificate(private_key_file: str, signing_request_file: str, filename: str) -> str:
    result_file = joinpath(_get_certs_dir(), filename)
    if not exists(dirname(result_file)):
        mkdir(dirname(result_file))
    cmd = Popen(["openssl", "x509", "-req", "-days", "365", "-in", signing_request_file, "-signkey", private_key_file, "-out", result_file],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file
