import numpy as np
import matplotlib.pyplot as plt

levels = np.arange(10, 40, 2)

values = np.array([
    [(levels[i] + levels[i + 1]) / 2 for i in range(len(levels) - 1)],
    [(levels[i] + levels[i + 1]) / 2 for i in range(len(levels) - 1)]
])

fig, ax = plt.subplots(figsize=(2, 6))

cs = ax.contourf(
    values,
    levels=levels,
    cmap="hot",
    extend="max"
)

ax.axis("off")

plt.colorbar(cs, ax=ax, ticks=levels)

plt.savefig(
    "temperature_legend.png",
    bbox_inches="tight",
    dpi=300,
    transparent=True
)

plt.show()