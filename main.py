import array
import time
from machine import Pin
from rp2 import StateMachine, asm_pio, PIO

# Configure the number of WS2812 LEDs
NUM_LEDS = 84

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
         autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on Pin(6)
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
sm.active(1)  # Start the StateMachine

# Display a pattern on the LEDs via an array of LED RGB values
pixel_array = array.array("I", [0 for _ in range(NUM_LEDS)])

def updatePixel(brightness=0.3):
    dimmer_array = array.array("I", [0 for _ in range(NUM_LEDS)])
    for ii, cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness)
        g = int(((cc >> 16) & 0xFF) * brightness)
        b = int((cc & 0xFF) * brightness)
        dimmer_array[ii] = (g << 16) + (r << 8) + b
    sm.put(dimmer_array, 8)

def set_led_color(index, color):
    pixel_array[index] = (color[1] << 16) + (color[0] << 8) + color[2]

def wheel(pos, brightness=0.2):
    """Generate a rainbow color with adjustable brightness."""
    brightness = max(0.0, min(1.0, brightness))  # Clamp between 0-1
    if pos < 85:
        r = int((255 - pos * 3) * brightness)
        g = int((pos * 3) * brightness)
        b = 0
    elif pos < 170:
        pos -= 85
        r = 0
        g = int((255 - pos * 3) * brightness)
        b = int((pos * 3) * brightness)
    else:
        pos -= 170
        r = int((pos * 3) * brightness)
        g = 0
        b = int((255 - pos * 3) * brightness)
    return (r, g, b)

def rainbow_cycle(wait, brightness=0.2):
    """Smooth scrolling rainbow effect across all LEDs."""
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            set_led_color(i, wheel(rc_index & 255, brightness))
        updatePixel()
        time.sleep_ms(wait)

while True:
    rainbow_cycle(250, brightness=1.0)  # Adjust brightness here (0.0 to 1.0)
