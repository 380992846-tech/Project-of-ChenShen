import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from collect_power import PowerSample, compute_pue, run_collector, summarize  # noqa: E402


def test_compute_pue():
    assert compute_pue(120000, 40000) == 3.000
    assert compute_pue(None, 40000) is None
    assert compute_pue(120000, 0) is None


def test_summarize_basic():
    samples = [
        PowerSample(0, 50, 100, 1200, 60, 40, 0.0),
        PowerSample(1, 60, 200, 1500, 80, 50, 0.0001),
    ]
    s = summarize(samples)
    assert s["count"] == 2
    assert s["avg_power_w"] == 150.0
    assert s["peak_power_w"] == 200.0
    assert s["duration_s"] == 1.0
    assert s["perf_per_watt"] is None  # 未给吞吐


def test_summarize_perf_per_watt():
    samples = [
        PowerSample(0, 50, 100, 1200, 60, 40, 0.0),
        PowerSample(1, 60, 200, 1500, 80, 50, 0.0001),
    ]
    # 平均功耗 150 W，吞吐 1500 tok/s => 10 tok/s/W
    s = summarize(samples, throughput=1500)
    assert s["perf_per_watt"] == 10.0


def test_run_collector_simulate_writes_csv(tmp_path):
    out = str(tmp_path / "curve.csv")
    summary = run_collector(duration=0.4, interval=0.08, out_path=out, simulate=True,
                            facility_w=120000, it_w=40000, throughput=1000)
    assert summary["count"] >= 1
    assert summary["avg_power_w"] > 0
    assert summary["pue_estimate"] == 3.0
    assert summary["perf_per_watt"] is not None
    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert float(rows[0]["power_w"]) > 0
