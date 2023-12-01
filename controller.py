import cv2
import pygame
from axibo import Axibo

# Prompt for the AXIBO IP address
axibo_ip = input("Enter AXIBO IP Address: ")

# Initialize the Axibo
axibo = Axibo(axibo_ip)
axibo.camera.set_resolution(640, 480)

# Initialize Pygame for Xbox controller
pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    raise IOError("No joystick detected")
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to map joystick input to movement speed
def map_joystick_to_speed(axis_value, max_speed):
    dead_zone = 0.1
    if -dead_zone < axis_value < dead_zone:
        return 0
    return axis_value * max_speed

# Initialize speed variable
speed = 5

try:
    while True:
        pygame.event.pump()
        pan_axis = joystick.get_axis(0)
        tilt_axis = -1 * joystick.get_axis(1)

        # Check bumper buttons for speed adjustment
        if joystick.get_button(9):  # Left bumper
            speed = max(1, speed - 1)  # Decrease speed, minimum of 1
        if joystick.get_button(10):  # Right bumper
            speed = min(10, speed + 1)  # Increase speed, maximum of 10

        pan_speed = map_joystick_to_speed(pan_axis, speed)
        tilt_speed = map_joystick_to_speed(tilt_axis, speed)

        axibo.motion.set_relative_move("pan", pan_speed, speed=speed)
        axibo.motion.set_relative_move("tilt", tilt_speed, speed=speed)
        axibo.motion.move_now()

        frame = axibo.camera.capture_opencv_image()
        current_position = axibo.motion.get_location()

        # Overlay position and speed data
        cv2.putText(frame, f"Position: {current_position}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)
        cv2.putText(frame, f"Speed: {speed}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)
        
        cv2.imshow("AXIBO Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pygame.quit()
    cv2.destroyAllWindows()
