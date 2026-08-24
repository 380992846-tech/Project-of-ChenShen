import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))

from core.thermal_manager import ThermalManager, ThermalStatus


def test_thermal_classification_thresholds():
    tm = ThermalManager()
    tm.update_thermal_state(50)
    assert tm.state.status == ThermalStatus.COOL
    tm.update_thermal_state(60)
    assert tm.state.status == ThermalStatus.NOMINAL
    tm.update_thermal_state(78)
    assert tm.state.status == ThermalStatus.WARM
    tm.update_thermal_state(86)
    assert tm.state.status == ThermalStatus.HOT
    tm.update_thermal_state(95)
    assert tm.state.status == ThermalStatus.CRITICAL


def test_heat_recovery_zero_below_baseline():
    tm = ThermalManager()
    tm.update_thermal_state(38)
    assert tm.state.heat_recovery_rate_w == 0.0


def test_heat_recovery_positive_above_baseline():
    tm = ThermalManager()
    tm.update_thermal_state(80)
    assert tm.state.heat_recovery_rate_w > 0.0


def test_guidance_action_for_critical():
    tm = ThermalManager()
    tm.update_thermal_state(95)
    guidance = tm.thermal_guidance()
    assert "严重" in guidance["action"]
    assert guidance["status"] == "critical"
