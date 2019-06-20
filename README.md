# MicroPython-MCP7940
A MicroPython driver for the Microchip MCP7940 RTC chip

## Example usage

```python
import mcp7940
from machine import Pin, I2C
import utime as time

i2c = I2C(sda=Pin(21), scl=Pin(22)) # Correct I2C pins for TinyPICO
mcp = mcp7940.MCP7940(i2c)

mcp.time # Read time
mcp.time = time.localtime() # Set time
mcp.start() # Start MCP oscillator
mcp.time # Read time after setting it, repeat to see time incrementing
```

