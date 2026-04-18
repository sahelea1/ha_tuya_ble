# Changes — ha_tuya_ble HA 2026.x compatibility fix

## 0.1.10 — Light platform kelvin migration + pycountry unblocking

After installing 0.1.9 the device setup still failed with "Einrichtungsfehler".
Home Assistant 2024.3+ removed the mireds-based color-temperature API from
`homeassistant.components.light`, so importing the `light` platform raised
`ImportError: cannot import name 'ATTR_COLOR_TEMP'` and the whole config entry
setup aborted (every device loads every platform module).

Fixed:

- `light.py` — migrated from the removed mireds API to the current kelvin API:
  - `ATTR_COLOR_TEMP` → `ATTR_COLOR_TEMP_KELVIN`
  - `self.min_mireds` / `self.max_mireds` → `self.min_color_temp_kelvin` /
    `self.max_color_temp_kelvin`
  - `color_temp` property → `color_temp_kelvin`
  - Removed `reverse=True` from the remap: mireds are inverse of kelvin, so the
    mapping direction flips when switching units (Tuya `temp_value` 0 = warm,
    max = cool; kelvin low = warm, high = cool → direct mapping).
- `config_flow.py` — `pycountry.countries.get(alpha_2=...)` is synchronous file
  I/O and triggered HA's blocking-call detector inside the event loop. Wrapped
  in `hass.async_add_executor_job(...)` and `_show_login_form` is now a
  coroutine awaited by both callers.
- `manifest.json` — bumped to `0.1.10`.

## Problem

All existing forks crash on import in Home Assistant 2024.x and later:

```
cannot import name 'CONF_APP_TYPE' from 'homeassistant.components.tuya.const'
cannot import name 'DPType' from 'homeassistant.components.tuya.const'
```

The HA core Tuya integration switched to QR-code-based cloud auth in 2024.x and removed
several legacy constants/types that `ha_tuya_ble` depended on.

## Root cause

Two symbols were removed from `homeassistant.components.tuya.const`:

| Symbol | Affected files | Fix |
|--------|---------------|-----|
| `DPType` (StrEnum describing Tuya DP data types) | `devices.py`, `light.py`, `tuya_ble/tuya_ble.py` | local definition via `tuya_compat.py` |
| `CONF_APP_TYPE` (string key `"app_type"`) | `cloud.py`, `config_flow.py` | local definition via `tuya_compat.py` |

All other imports from `homeassistant.components.tuya.const` (`DPCode`, `WorkMode`,
`CONF_ENDPOINT`, `TUYA_RESPONSE_*`, `DOMAIN`) are still present in HA core and unchanged.

## Changes made

### New file: `custom_components/tuya_ble/tuya_compat.py`

Compatibility shim.  For each removed symbol it first tries to import from core (for
forward-compatibility), then falls back to a locally-defined equivalent:

- **`DPType`** — `StrEnum` with members `BOOLEAN`, `INTEGER`, `JSON`, `RAW`, `STRING`,
  `ENUM` matching the string values used by the Tuya cloud specification API
  (`"Boolean"`, `"Integer"`, etc.).
- **`CONF_APP_TYPE`** — string constant `"app_type"`.

### Modified files

- `cloud.py` — removed `CONF_APP_TYPE` from core import; added `from .tuya_compat import CONF_APP_TYPE`
- `config_flow.py` — same as above
- `devices.py` — removed `DPType` from core import; added `from .tuya_compat import DPType`
- `light.py` — same as above
- `tuya_ble/tuya_ble.py` — removed `DPType` from core import; added `from ..tuya_compat import DPType`

## Installation

1. Copy `custom_components/tuya_ble/` into your HA config directory:
   ```
   /config/custom_components/tuya_ble/
   ```
2. Restart Home Assistant.
3. Add the integration via **Settings → Devices & Services → Add Integration → Tuya BLE**.
4. Enter your Tuya IoT Platform credentials (Access ID, Access Secret, username, password).
