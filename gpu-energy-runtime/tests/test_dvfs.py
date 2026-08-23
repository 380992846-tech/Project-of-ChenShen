import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))

from core.dvfs_controller import DVFSController, PowerMode  # noqa: E402


def _ctrl():
    return DVFSController(gpu_index=0, config={})


def test_build_freq_table_sorted_and_covered():
    c = _ctrl()
    assert c.freq_table == sorted(c.freq_table)
    assert c.freq_table[0] == 300 and c.freq_table[-1] == 2100


def test_power_limit_clamped_to_hardware_range():
    c = _ctrl()
    c.set_power_limit(1e9)
    assert c.state.power_limit <= c.max_power_limit + 1e-6
    c.set_power_limit(0.1)
    assert c.state.power_limit >= c.min_power_limit - 1e-6


def test_clock_limit_snaps_to_available_step():
    c = _ctrl()
    c.set_clock_limit(9_999_999)
    assert c.state.core_clock == c.freq_table[-1]


def test_predict_heuristic_by_utilization():
    c = _ctrl()
    c.state.utilization = 95
    assert c.predict_optimal_frequency() == c.freq_table[-1]
    c.state.utilization = 10
    assert c.predict_optimal_frequency() == c.freq_table[2]


def test_mode_switches_update_state():
    c = _ctrl()
    c.set_power_mode(PowerMode.MAX_PERFORMANCE)
    assert c.state.current_mode == PowerMode.MAX_PERFORMANCE
    c.set_power_mode(PowerMode.POWER_SAVE)
    assert c.state.current_mode == PowerMode.POWER_SAVE
    assert c.state.core_clock <= c.freq_table[1]
