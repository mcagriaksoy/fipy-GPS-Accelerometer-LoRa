from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
import time

py = Pytrack()

# display the reset reason code and the sleep remaining in seconds
# possible values of wakeup reason are:
# WAKE_REASON_ACCELEROMETER = 1
# WAKE_REASON_PUSH_BUTTON = 2
# WAKE_REASON_TIMER = 4
# WAKE_REASON_INT_PIN = 8

print("Wakeup reason: " + str(py.get_wake_reason()))
print("Approximate sleep remaining: " + str(py.get_sleep_remaining()) + " sec")
time.sleep(0.5)

# enable wakeup source from INT pin
py.setup_int_pin_wake_up(False)

acc = LIS2HH12()

# enable activity and also inactivity interrupts, using the default callback handler
py.setup_int_wake_up(True, True)

# set the acceleration threshold to 2000mG (2G) and the min duration to 200ms
acc.enable_activity_interrupt(2000, 200)

# go to sleep for 5 minutes maximum if no accelerometer interrupt happens
py.setup_sleep(300)
py.go_to_sleep()
