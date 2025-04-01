# WS2812_LEDStrip_SmoothRainbow
Smooth rainbow scrolling via merging a script for pi pico and a script for the full big raspberry pi


Base Script Credits: 

https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/

and

https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage


Note: I have it set to use GPIO 0 for the data line and have my 84 LEDs set as the number of LEDs already. You will need to adjust those if your strip is different.
Note2: This is a fairly slow scroll so it may not look immediately look like it is doing anything. You can adjust the speed and brightness at the bottom rainbow_cycle area portion of the script.
