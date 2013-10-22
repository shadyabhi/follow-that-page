import yaml
from html2text import html2text
import urllib2
import time
import os
import hashlib
import difflib
import sys

# Read config file
config_file = yaml.load(open("conf/websites.yaml"))
# Set default encoding to 'UTF-8' instead of 'ascii'
# http://stackoverflow.com/questions/11741574/how-to-set-the-default-encoding-to-utf-8-in-python
# Bad things might happen though
reload(sys)
sys.setdefaultencoding("UTF8")

cache_dir = config_file['settings']['cache_dir']
websites_to_monitor = config_file['websites']
current_time = time.time()

# Create required directories
if not os.path.exists(cache_dir): os.makedirs(cache_dir)

# Lambda that returns full-path where URL contents are stored.
# which is: cache_dir + md5sum(url)
url_path_on_filesystem = lambda url: os.path.join(cache_dir, hashlib.md5(os.path.join(cache_dir + url)).hexdigest())

def read_stored_copy(url):
    """
    Read the stored copy of the URL and return it.
    If it doesn't exist, return None
    """
    path = url_path_on_filesystem(url)
    if os.path.exists(path):
        return open(path).read()
    else:
        # This should not happen.
        return None

def write_stored_copy(url, contents):
    """ Write current page contents to the file """
    path = url_path_on_filesystem(url)

    with open(path, "w") as f:
        f.write(contents)

for w in websites_to_monitor:
    url = w['url']
    frequency = w['frequency']

    url_current_copy = html2text(urllib2.urlopen(url).read())

    try:
        if current_time - os.stat(url_path_on_filesystem(url)).st_mtime < frequency: continue
    except OSError:
        # That means that the file doesn't exist.
        with open(url_path_on_filesystem(url), 'w') as f:
            f.write(url_current_copy)

    if url_current_copy == read_stored_copy(url):
        # No changes. Just change mtime to the current time to keep
        # the track of last time it was checked
        os.utime(url_path_on_filesystem(url), (current_time, current_time))
        pass
    else:
        print "URL changed: ", url
        diff = '\n'.join(difflib.ndiff(read_stored_copy(url).splitlines(), url_current_copy.splitlines()))
        print diff
        write_stored_copy(url, url_current_copy)
