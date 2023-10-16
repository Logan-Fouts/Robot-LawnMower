from matplotlib import patches
import numpy as np
import matplotlib.pyplot as plt


class Lawn:
    def __init__(self, ground):
        self.ground = np.array(ground)
        self.full_lawn = None
        self.rows = len(ground)
        self.cols = len(ground[0])
        self.mowed = None

    def gen_lawn(self, pixel_size):
        """
        Expands lawn to full size using NP magic based on pixel size.
        """
        full_lawn = np.repeat(
            np.repeat(self.ground, pixel_size, axis=0), pixel_size, axis=1
        )
        self.mowed = np.zeros_like(full_lawn, dtype=int)
        self.full_lawn = full_lawn
        return full_lawn

    def get_start_pos(self, pix_size):
        """
        Loop through small lawn so its faster and return converted (x, y)
        position.
        """
        for x in range(self.rows):
            for y in range(self.cols):
                if self.ground[x][y] == "S":
                    return (x * pix_size, y * pix_size)
        print("Error: No Starting Position")
        return None

    def mow_pixel(self, x, y):
        self.mowed[x][y] = 1

    def calc_percent_mowed(self):
        """
        Calculates perecentage of lawn mowed taking into account the obsticles.
        """
        mowed_pixels, total_obsitcles = np.sum(self.mowed == 1), np.sum(
            self.full_lawn == "O"
        )
        return (mowed_pixels / (self.full_lawn.size - total_obsitcles)) * 100

    def plot_results(self, pix_size):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

        self.plot_ground(ax1)

        self.plot_coverage(ax2, pix_size)

        plt.show()

    def plot_ground(self, ax):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "black" if self.ground[i][j] == "O" else "green"
                color = "yellow" if self.ground[i][j] == "S" else color
                rect = patches.Rectangle(
                    (j, i),
                    1,
                    1,
                    linewidth=1,
                    edgecolor="black",
                    facecolor=color,
                )
                ax.add_patch(rect)

        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.invert_yaxis()
        ax.set_aspect("equal")
        ax.set_xticks(np.arange(0, self.cols, 1))
        ax.set_yticks(np.arange(0, self.rows, 1))
        ax.grid(True, color="black", linewidth=1)
        ax.set_title("Ground Map")

    def plot_coverage(self, ax, pix_size):
        for i in range(self.rows * pix_size):
            for j in range(self.cols * pix_size):
                color = "white" if self.mowed[i][j] == 0 else "red"
                color = "black" if self.full_lawn[i][j] == "O" else color
                rect = patches.Rectangle(
                    (j * 1, i * 1),
                    1,
                    1,
                    linewidth=1,
                    edgecolor="black",
                    facecolor=color,
                )
                ax.add_patch(rect)

        ax.set_xlim(0, self.cols * pix_size)
        ax.set_ylim(0, self.rows * pix_size)
        ax.invert_yaxis()
        ax.set_aspect("equal")
        ax.grid(True, color="black", linewidth=1)
        ax.set_title("Coverage Map")
