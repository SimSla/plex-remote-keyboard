# plex-remote-keyboard
Uses the [Plex Home Theatre REST API](https://code.google.com/p/plex-api/wiki/PlaybackControl) to remotely control Plex with a keyboard.

Tested on Mac OS X and Python 2.7. *Might* work on other systems.

## Installation
Change the IP address in `src/plex-remote-keyboard.py` to match that of your PHT host.

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
usage: plex-remote-keyboard [-h] [-a ADDRESS] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        IP address of PHT host. (default: 192.168.1.104)
  -p PORT, --port PORT  Port where PHT host can be reached. (default: 3005)
```

### Example

Run without arguments to use the default IP address and port (192.168.1.104:3005). The default IP address is arbitrary and can be changed in the source code.
```
$ plex-remote-keyboard
```
![Screenshot 1](https://cloud.githubusercontent.com/assets/2266504/7202090/414c11b8-e50f-11e4-9d05-302f68f662c4.png)

![Screenshot 2](https://cloud.githubusercontent.com/assets/2266504/7202514/545f6b66-e513-11e4-9ebb-99ad720ab2bf.png)
