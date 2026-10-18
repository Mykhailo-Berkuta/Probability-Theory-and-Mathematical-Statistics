# -*- coding: utf-8 -*-
"""Лабораторна робота № 1. Побудова дискретних варіаційних рядів.
Розрахунок їх характеристик. Варіанти: В11 (n = 20) та № 16 (n = 100)."""
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.rcParams["font.family"] = ["Times New Roman", "Liberation Serif", "DejaVu Serif"]
plt.rcParams["mathtext.fontset"] = "stix"

DATA_1 = [1, 1, 2, 2, 1, 2, 3, 2, 3, 2, 2, 4, 2, 4, 5, 2, 5, 4, 2, 6]
DATA_2 = [
    4, 8, 3, 5, 2, 0, 3, 7, 4, 4, 0, 4, 2, 1, 3, 4, 7, 4, 4, 7, 1, 3, 3, 4, 3, 3, 12, 5, 2, 3, 3, 6, 4, 5,
    3, 2, 3, 4, 1, 4, 4, 1, 3, 5, 3, 4, 1, 1, 7, 2, 1, 2, 4, 5, 3, 2, 7, 1, 0, 0, 3, 3, 7, 3, 6, 3, 3, 4,
    3, 4, 3, 4, 3, 3, 3, 3, 5, 4, 7, 1, 5, 3, 6, 0, 3, 1, 7, 4, 3, 4, 3, 1, 1, 0, 7, 3, 4, 4, 3, 2,
]


def r4(x):
    """Округлення до 4 знаків «як у математиці» (0,5 -> вгору)."""
    return Decimal(repr(round(x, 10))).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def comma(x):
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def draw_polygon(v, w, xlim, path):
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.vlines(v, 0, w, colors="#777777", linestyles="--", lw=0.8)
    ax.plot(v, w, "-o", color="#1f4e79", ms=4.5, lw=1.6, zorder=3)
    for a, b in zip(v, w):
        ax.annotate(comma(b), (a, b), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=9)
    ax.set_xlim(*xlim)
    ax.set_ylim(0, max(w) * 1.2)
    ax.set_xticks(v)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: comma(y)))
    ax.set_xlabel("Варіанти $v_i$", fontsize=11)
    ax.set_ylabel("Відносна частота $w_i$", fontsize=11)
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.17, top=0.95)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def draw_ecdf(v, cum, n, xlim, path):
    c = [x / n for x in cum]
    k = len(v)
    col = "#1f4e79"
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.plot([xlim[0], v[0]], [0, 0], color=col, lw=1.8)
    ax.plot([v[0]], [0], "o", color=col, ms=5, zorder=4)
    for i in range(k - 1):
        ax.plot([v[i], v[i + 1]], [c[i], c[i]], color=col, lw=1.8)
        ax.plot([v[i + 1]], [c[i]], "o", color=col, ms=5, zorder=4)
    ax.plot([v[-1], xlim[1]], [1, 1], color=col, lw=1.8)
    for i in range(k):
        ax.plot([v[i]], [c[i]], "o", mfc="white", mec=col, ms=5, zorder=5)
        prev = c[i - 1] if i > 0 else 0
        ax.plot([v[i], v[i]], [prev, c[i]], color="#999999", lw=0.8, ls="--", zorder=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.04, 1.08)
    ax.set_xticks(v)
    ax.set_yticks([i / 10 for i in range(11)])
    ax.tick_params(axis="y", labelsize=8)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: comma(y)))
    ax.set_xlabel("$x$", fontsize=11)
    ax.set_ylabel("$F^*(x)$", fontsize=11)
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.17, top=0.95)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def analyze(name, data, xlim, tag):
    n = len(data)                                   # об'єм вибірки
    freq = Counter(data)
    v = sorted(freq)                                # варіанти v_j
    f = [freq[x] for x in v]                        # частоти f_j
    k = len(v)                                      # кількість різних значень

    print(f"== {name} (n={n}, k={k}) ==")
    print("Варіаційний ряд:", *sorted(data))

    cum_list = []
    cum = 0
    for i in range(k):
        cum += f[i]                                 # накопичена частота
        w = f[i] / n                                # відносна частота
        wc = cum / n                                # накопичена відносна частота
        cum_list.append(cum)
        print(i + 1, v[i], f[i], r4(w), cum, r4(wc), sep="\t")

    mean = sum(v[j] * f[j] for j in range(k)) / n

    max_f = max(f)
    mode = [v[j] for j in range(k) if f[j] == max_f]

    s = sorted(data)
    median = (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]

    d = sum(abs(v[j] - mean) * f[j] for j in range(k)) / n

    disp = sum((v[j] - mean) ** 2 * f[j] for j in range(k)) / n
    sd = disp ** 0.5

    m3 = sum((x - mean) ** 3 for x in data) / n
    As = m3 / sd ** 3

    m4 = sum((x - mean) ** 4 for x in data) / n
    Ek = m4 / sd ** 4 - 3

    print(f"mean={r4(mean)} mode={','.join(map(str, mode))} median={median:g} d={r4(d)} disp={r4(disp)} "
          f"sd={r4(sd)} m3={r4(m3)} m4={r4(m4)} As={r4(As)} Ek={r4(Ek)}")

    draw_polygon(v, [x / n for x in f], xlim, f"polygon_{tag}.png")
    draw_ecdf(v, cum_list, n, xlim, f"ecdf_{tag}.png")


if __name__ == "__main__":
    analyze("Вибірка 1 (B11)", DATA_1, (0, 7), 1)
    analyze("Вибірка 2 (№16)", DATA_2, (-1, 13), 2)
