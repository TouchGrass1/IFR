import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap



cumLapTimes = {
    'driverOne': [113.901, 190.353, 261.857, 331.104, 398.652,
                    466.026, 536.357, 605.743, 671.024, 736.401,
                    808.066, 873.338, 938.436, 1003.34, 1083.0],
    'driverTwo': [40.594, 117.581, 191.908, 264.67, 338.821,
                    413.768, 487.82, 561.371, 636.068, 708.539,
                    783.379, 862.935, 940.344, 1036.0],
}


def cleanDf(df):
    # df.columns = (
    #     df.columns
    #     .str.strip()          # remove leading/trailing spaces
    #     .str.lower()          # consistent casing
    #     .str.replace(r"\s+", "_", regex=True)  # spaces -> underscores
    #     .str.replace(r"[^\w]", "", regex=True) # drop punctuation
    # )
    df.fillna(0)
    return df

def add_lap_lines(ax, cumLapTimes, drivers=('driverOne', 'driverTwo'),
                  color1='green', color2='royalblue'):
    styles = ['-', '--']
    for name, style, color in zip(drivers, styles, (color1, color2)):
        for i, t in enumerate(cumLapTimes[name]):
            ax.axvline(t, color=color, linestyle=style, linewidth=0.8,
                       alpha=0.6)
            ax.text(t, ax.get_ylim()[1], str(i + 1), color=color,
                    fontsize=7, ha='right', va='top')

    return ax


files = ["Driver1EnduranceData.csv", "Driver2EnduranceData.csv"]

if __name__ == "__main__":

    drivers = {
            'driverOne': pd.read_csv(files[0]),
            'driverTwo': pd.read_csv(files[1]),
        }
    for name in drivers:
        df = cleanDf(drivers[name])
    #Offet driver 1 to align data
    lapTimeOffset = 74.9
    drivers['driverOne']['Time (s)'] -= lapTimeOffset
    drivers['driverOne'] = drivers['driverOne'][drivers['driverOne']["Time (s)"] >= 0]
    cumLapTimes['driverOne'] = [x - lapTimeOffset for x in cumLapTimes['driverOne']]


    # Assign each telemetry row to a lap number, then plot per column
    for name, d in drivers.items():
        d['Lap'] = np.searchsorted(cumLapTimes[name], d['Time (s)'], side='right') + 1

    # Set Time (s) to x-axis
    columns = [c for c in drivers['driverOne'].columns if c not in ('Time (s)', 'Lap')]

    # Choose Header
    for i, c in enumerate(columns):
        print(i, ':', c)
    header = columns[int(input("Enter header index: "))]
    heat = columns[int(input("Enter index for heat mapping: "))]

    # Driver 1: green -> red-orange
    cmap1 = LinearSegmentedColormap.from_list('d1', ['#00c000', '#ff8c00'])
    # Driver 2: blue-green -> red
    cmap2 = LinearSegmentedColormap.from_list('d2', ['#00b8b8', '#ff3030'])

    fig, ax = plt.subplots(figsize=(12, 6))
    lcs = []
    for name, cmap in zip(drivers, (cmap1, cmap2)):
        d = drivers[name]
        x = d['Time (s)']
        y = gaussian_filter1d(d[header], sigma=15)

        h = d[heat].values
        norm_h = (h - h.min()) / (np.ptp(h) or 1)   # 0% -> 100% per driver

        pts = np.column_stack([x, y]).reshape(-1, 1, 2)
        segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = LineCollection(segments, cmap=cmap, linewidth=3,
                            array=norm_h[:-1], label=name)
        ax.add_collection(lc)
        lcs.append((lc, heat, h.min(), h.max()))


    ax.set(xlabel='Time (s)', ylabel=header, title=f"{header} vs Time (colour = {heat})")
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.legend()

    # One colourbar per driver, labelled with real values
    cbar1 = fig.colorbar(lcs[0][0], ax=ax, pad=0.02)
    cbar1.set_ticks([0, 1]); cbar1.set_ticklabels([f"{lcs[0][2]:.1f}", f"{lcs[0][3]:.1f}"])
    cbar1.set_label(f"{name} {heat}")
    cbar2 = fig.colorbar(lcs[1][0], ax=ax, pad=0.06)
    cbar2.set_ticks([0, 1]); cbar2.set_ticklabels([f"{lcs[1][2]:.1f}", f"{lcs[1][3]:.1f}"])
    cbar2.set_label(f"{name} {heat}")
    add_lap_lines(ax, cumLapTimes)
    plt.show()
