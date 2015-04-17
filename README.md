# plex-remote-keyboard
Uses the [Plex Home Theatre REST API](https://code.google.com/p/plex-api/wiki/PlaybackControl) to remotely control Plex with a keyboard.

Tested on Mac OS X and Python 2.7. *Might* work on other systems.

## Installation
Run the setup script to install the script and add it to your path.

    $ python setup.py install
    $ plex-remote-keyboard
    ...

You can also run the script without installing.

    $ python src/plex-remote-keyboard.py
    ...

## Usage

```
$ plex-remote-keyboard -h
usage: plex-remote-keyboard [-h] [-a ADDRESS] [-p PORT] [-u]

Uses the Plex Home Theatre REST API to remotely control Plex with a keyboard.

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        IP address of PHT host.
  -p PORT, --port PORT  Port where PHT host can be reached. (default: 3005)
  -u, --update_defaults
                        Causes the current defaults to be overwritten with the
                        supplied address and/or port.
```

### Example

Run without arguments to use the default IP address and port. The default IP address and port can be configured on the first run and can be changed at any time.
```
$ plex-remote-keyboard
```
![Screenshot 1](https://cloud.githubusercontent.com/assets/2266504/7202090/414c11b8-e50f-11e4-9d05-302f68f662c4.png)

![Screenshot 2](https://cloud.githubusercontent.com/assets/2266504/7202514/545f6b66-e513-11e4-9ebb-99ad720ab2bf.png)
