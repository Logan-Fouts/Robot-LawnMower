from matplotlib import pyplot as plt
import numpy as np
from lawn import Lawn
from robot import Robot


def load_map(file_path):
    return np.genfromtxt(file_path, dtype=str, delimiter=",")


def sim_move(ground, robot, vx, vy, dt, scale):
    """
    Moves the robot in a valid direction using gen_rand_vector.
    """
    px, py = robot.px, robot.py
    while True:
        tmp_px = robot.px + vx * dt
        tmp_py = robot.py + vy * dt

        tmp_px = float(tmp_px)
        tmp_py = float(tmp_py)

        if (
            0 <= tmp_px < ground.shape[0]
            and 0 <= tmp_py < ground.shape[1]
            and ground[int(tmp_px)][int(tmp_py)] != "O"
        ):
            px = tmp_px
            py = tmp_py
            break
        else:
            vx, vy = robot.gen_rand_vector(scale)
    return px, py, vx, vy


def plot_path(paths, secs):
    """
    Plots every position as a line to show the robots trace.
    """
    plt.figure(figsize=(8, 6))

    for path in paths:
        x = [point[0] for point in path]
        y = [point[1] for point in path]
        plt.plot(x, y)

    plt.gca().invert_yaxis()
    plt.title(f"Robot Trace after {(secs / 60)} mins")
    plt.show()


if __name__ == "__main__":
    num_runs = 100
    sim_time = 3600 * 10
    delta_t = 1
    pix_size = 5
    map_file = "Maps/complex_map.csv"

    average_percent_mowed = []
    last_run_movement = []

    # Experiment Starts Here
    for i in range(num_runs):
        ground = load_map(map_file)
        lawn = Lawn(ground)
        robot = Robot(velocity=.3)

        robot.px, robot.py = lawn.get_start_pos(pix_size)
        full_lawn = lawn.gen_lawn(pix_size)

        vx, vy = robot.gen_rand_vector(pix_size)
        while True:
            tmp_px = robot.px + vx * delta_t
            tmp_py = robot.py + vy * delta_t

            tmp_px = float(tmp_px)
            tmp_py = float(tmp_py)

            if (
                0 <= tmp_px < full_lawn.shape[0] and
                0 <= tmp_py < full_lawn.shape[1]
            ):
                if full_lawn[int(tmp_px)][int(tmp_py)] != "O":
                    px = tmp_px
                    py = tmp_py
                    break
            else:
                vx, vy = robot.gen_rand_vector(pix_size)

        movement = []
        for _ in range(sim_time):
            lawn.mow_pixel(int(robot.px), int(robot.py))
            robot.px, robot.py, vx, vy = sim_move(
                full_lawn, robot, vx, vy, delta_t, pix_size
            )
            movement.append((robot.py, robot.px))

        percent_mowed = lawn.calc_percent_mowed()
        average_percent_mowed.append(percent_mowed)

        if i == num_runs - 1:
            last_run_movement = movement
            lawn.plot_results(pix_size)

    # Results Printed and Plotted
    print(f"Average Percent Mowed: {np.mean(average_percent_mowed):.2f}%")
    plot_path([last_run_movement], sim_time)
