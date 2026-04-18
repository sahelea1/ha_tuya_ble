"""Diagnostics for Tuya BLE — adds a Download Diagnostics button to each device."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .devices import TuyaBLEData


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry (= one BLE device)."""
    data: TuyaBLEData = hass.data[DOMAIN][entry.entry_id]
    device = data.device

    return {
        "title": entry.title,
        "connected": data.coordinator.connected,
        "device": {
            "address": device.address,
            "product_id": device.product_id,
            "product_name": device.product_name,
            "product_model": device.product_model,
            "category": device.category,
            "device_version": device.device_version,
            "hardware_version": device.hardware_version,
            "protocol_version": device.protocol_version,
        },
        "datapoints": {
            str(dp_id): {
                "type": str(dp.type),
                "value": repr(dp.value),
            }
            for dp_id, dp in device.datapoints._datapoints.items()
        },
        "function_count": len(device.function),
        "status_range_count": len(device.status_range),
    }
