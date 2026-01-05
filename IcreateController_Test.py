"""IcreateController_Test controller.

Clean, runnable Webots controller for a Create-like robot.
#notes: fixes indentation, enables sensors correctly, checks devices,
# and wraps logic in `main()`.
"""

from controller import Robot
import random
import sys


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # --- Devices (names used by the world) ---
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    bumper_l = robot.getDevice("bumper_left")
    bumper_r = robot.getDevice("bumper_right")

    cliff_l = robot.getDevice("cliff_left")
    cliff_fl = robot.getDevice("cliff_front_left")
    cliff_fr = robot.getDevice("cliff_front_right")
    cliff_r = robot.getDevice("cliff_right")

    # Check required devices exist
    device_map = {
        "left wheel motor": left_motor,
        "right wheel motor": right_motor,
        "bumper_left": bumper_l,
        "bumper_right": bumper_r,
        "cliff_left": cliff_l,
        "cliff_front_left": cliff_fl,
        "cliff_front_right": cliff_fr,
        "cliff_right": cliff_r,
    }
    missing = [name for name, dev in device_map.items() if dev is None]
    if missing:
        print("Device(s) not found on robot:", ", ".join(missing))
        print("Controller will exit.")
        sys.exit(1)

    # --- Motor setup (velocity control) ---
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    # --- Enable sensors ---
    bumper_l.enable(timestep)
    bumper_r.enable(timestep)
    for s in (cliff_l, cliff_fl, cliff_fr, cliff_r):
        s.enable(timestep)

    # --- Tuning constants ---
    FWD = 6.0
    REV = -4.0
    TURN = 4.0
    CLIFF_TH = 100.0

    # FSM states
    FORWARD, BACKUP, TURNING = 0, 1, 2
    state = FORWARD
    state_steps = 0
    turn_dir = 1

    print("Controller running ✔")

    # Main control loop
    while robot.step(timestep) != -1:
        bl = bumper_l.getValue() > 0
        br = bumper_r.getValue() > 0

        cv = [
            cliff_l.getValue(),
            cliff_fl.getValue(),
            cliff_fr.getValue(),
            cliff_r.getValue(),
        ]
        cliff = any(v < CLIFF_TH for v in cv)

        if state == FORWARD:
            left_motor.setVelocity(FWD)
            right_motor.setVelocity(FWD)

            if bl or br or cliff:
                state = BACKUP
                state_steps = 12
                if bl and not br:
                    turn_dir = -1
                elif br and not bl:
                    turn_dir = 1
                else:
                    turn_dir = random.choice([-1, 1])

        elif state == BACKUP:
            left_motor.setVelocity(REV)
            right_motor.setVelocity(REV)
            state_steps -= 1
            if state_steps <= 0:
                state = TURNING
                state_steps = 18

        elif state == TURNING:
            if turn_dir == 1:
                left_motor.setVelocity(-TURN)
                right_motor.setVelocity(TURN)
            else:
                left_motor.setVelocity(TURN)
                right_motor.setVelocity(-TURN)

            state_steps -= 1
            if state_steps <= 0:
                state = FORWARD


if __name__ == "__main__":
    main()