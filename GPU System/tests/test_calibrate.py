import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from calibrate import fit_power_model, load_csv_points  # noqa: E402


def test_load_csv_points(tmp_path):
    path = tmp_path / "p.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["core_clock_mhz", "power_w"])
        w.writeheader()
        w.writerow({"core_clock_mhz": "1200", "power_w": "140"})
        w.writerow({"core_clock_mhz": "1800", "power_w": "260"})
    freqs, powers = load_csv_points(str(path))
    assert freqs == [1200.0, 1800.0]
    assert powers == [140.0, 260.0]


def test_fit_power_model():
    pytest.importorskip("numpy")
    alpha, beta = fit_power_model(
        [300, 600, 900, 1200, 1500, 1800, 2100],
        [35, 60, 95, 140, 195, 260, 335],
    )
    assert alpha > 0
    assert beta > 1.0
