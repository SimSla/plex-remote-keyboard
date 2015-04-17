try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import shutil

SCRIPT_NAME = "plex-remote-keyboard"
CONFIG_FILE = "settings.cfg"

if not os.path.isfile(CONFIG_FILE):
    exit("%s is missing." % CONFIG_FILE)

if not os.path.exists('build/bin'):
    os.makedirs('build/bin')
shutil.copyfile('src/%s.py' % SCRIPT_NAME, 'build/bin/%s' % SCRIPT_NAME)

setup(name=SCRIPT_NAME,
      version='0.2',
      install_requires=['appdirs'],
      scripts=['build/bin/%s' % SCRIPT_NAME],
      )

