import json
import requests
requests.adapters.DEFAULT_RETRIES=3

API="http://www.tehlab.io/api"

def start(token):
    response = requests.get(API + "/start", params = {"token": token})
    return response.text

def status(token, uid):
    response = requests.get(API + "/status", params = {"token": token, "uid": uid})
    return json.loads(response.text.strip().decode("utf8"))

def stop(token, uid):
    response = requests.get(API + "/stop", params = {"token": token, "uid": uid})
    return json.loads(response.text.strip().decode("utf8"))

def push_urls_from_file(api, filename, uid = ""):
    with open(filename, "rb") as urlfile:
        return _push_urls(api, urlfile, uid=uid)

def fetch_urls_to_file(api, filename, uid):
    with open(filename, "w") as urlfile:
        for line in _fetch_urls(api, uid):
            urlfile.write(line)
            urlfile.write("\r\n")

def push_fetch_urls_file(api, infilename, outfilename, uid = ""):
    with open(infilename, "rb") as infile, open(outfilename, "w") as outfile:
        for line in _push_fetch_urls(api, infile, uid=uid):
            outfile.write(line)
            urlfile.write("\r\n")

def push_urls(api, urls, uid = ""):
    urlfile = "\r\n".join(urls)
    return _push_urls(api, urlfile, uid=uid)

def fetch_urls(api, uid):
    for line in _fetch_urls(api, uid):
        yield json.loads(line.decode("utf8"))

def push_fetch_urls(api, urls, uid = ""):
    urlfile = "\r\n".join(urls)
    for line in _push_fetch_urls(api, urlfile, uid=uid):
        yield json.loads(line.decode("utf8"))

def _push_urls(api, urlfile, uid):
    response = requests.post(api, params = {"wait": 0, "uid": uid}, data = urlfile)
    return response.text

def _push_fetch_urls(api, urlfile, uid):
    response = requests.get(api, params = {"uid": uid}, data = urlfile, stream = True, timeout = None)
    for line in response.iter_lines():
        yield line.strip()

def _fetch_urls(api, uid):
    response = requests.get(api, params = {"uid": uid}, stream = True, timeout = None)
    for line in response.iter_lines():
        yield line.strip()
