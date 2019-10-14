# SmittenBooth

This is my first attempt at a Raspberry Pi based photobooth. Written in Python

Because of an issue I had where the Raspberry Pi's GPIO pins voltage would fluctuate and trigger incorrectly as a button press, I've incorporated the use of an Arduino Uno purely to detect the button press, and report back to the Pi via Serial connection.

## Dependencies:

- Python2.7, but I believe it should be Python3 compatible, I've yet to test
- [pyserial](https://pypi.org/project/pyserial/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
- [picamera](https://pypi.org/project/picamera/)
- [Pillow](https://pypi.org/project/Pillow/)

```
sudo apt install python pip
pip install pyserial
pip install RPi.GPIO
pip install picamera
pip install Pillow
```
