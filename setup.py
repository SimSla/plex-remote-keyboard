from distutils.core import setup
import os
import shutil

SCRIPT_NAME = "plex-remote-keyboard"
if not os.path.exists('build/bin'):
    os.makedirs('build/bin')
shutil.copyfile('src/%s.py' % SCRIPT_NAME, 'build/bin/%s' % SCRIPT_NAME)

setup(name=SCRIPT_NAME,
      version='0.1',
      scripts=['build/bin/%s' % SCRIPT_NAME],
      )