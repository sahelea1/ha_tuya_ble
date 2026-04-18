# Changes — ha_tuya_ble HA 2026.x compatibility fix

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
