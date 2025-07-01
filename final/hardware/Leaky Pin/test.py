import digitalio
import board

pin = digitalio.DigitalInOut(board.GP24)
pin.switch_to_input()

print(pin.value)  # Should fluctuate when secret_in_gpio25() is called