"""Compatibility shim for constants removed from homeassistant.components.tuya.const.

HA 2024.x removed DPType and several CONF_* constants from the core Tuya integration
when it switched to QR-code-based cloud auth.  This module provides local fallback
definitions so the tuya_ble integration keeps working on HA 2024.x and later while
remaining forward-compatible: if a symbol ever reappears in core it will be used.
"""
from __future__ import annotations

from enum import StrEnum

# ---------------------------------------------------------------------------
# DPType – describes the data type of a Tuya data-point as returned by the
# cloud device-specification API (e.g. "Boolean", "Integer", "Enum", …).
# Removed from homeassistant.components.tuya.const in HA 2024.x.
# ---------------------------------------------------------------------------
try:
    from homeassistant.components.tuya.const import DPType
except ImportError:
    class DPType(StrEnum):  # type: ignore[no-redef]
        """Tuya data-point type, as returned by the cloud specification API."""

        BOOLEAN = "Boolean"
        INTEGER = "Integer"
        JSON = "Json"
        RAW = "Raw"
        STRING = "String"
        ENUM = "Enum"

# ---------------------------------------------------------------------------
# CONF_APP_TYPE – key used to identify the Tuya smart-home app type
# ("tuyaSmart" / "smartlife") in legacy SMART_HOME auth flows.
# Removed from homeassistant.components.tuya.const in HA 2024.x.
# ---------------------------------------------------------------------------
try:
    from homeassistant.components.tuya.const import CONF_APP_TYPE
except ImportError:
    CONF_APP_TYPE = "app_type"

__all__ = ["DPType", "CONF_APP_TYPE"]
