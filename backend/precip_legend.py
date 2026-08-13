import numpy as np
import matplotlib.pyplot as plt

levels = [0, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 100]


values = np.array([
    [(levels[i] + levels[i + 1]) / 2 for i in range(len(levels) - 1)],
    [(levels[i] + levels[i + 1]) / 2 for i in range(len(levels) - 1)]
])

fig, ax = plt.subplots(figsize=(2, 6))

cs = ax.contourf(
    values,
    levels=levels,
    cmap="turbo",
    extend="max"
)

ax.axis("off")


cbar = plt.colorbar(cs, ax=ax, ticks=levels)


plt.savefig(
    "precipitation_legend.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
)

plt.show()