```markdown
# 🔵 Tuya BLE — Home Assistant Integration

> Bluetooth-local control of Tuya BLE devices, fully independent of the official Tuya HA integration.

---

## ✨ Overview

This custom integration brings **Tuya BLE devices** (such as Fingerbots, sensors, locks, valves, and more) into Home Assistant via local Bluetooth — no cloud required for day-to-day operation.

Once installed through HACS, the integration is **completely standalone**. All credentials are entered directly inside Home Assistant when a new device is discovered — no separate app installation or other integration needed.

---

## 👏 Credits & Acknowledgements

| Role | Contributor |
|---|---|
| 🏆 **Original creator** | [@PlusPlus-ua](https://github.com/PlusPlus-ua/ha_tuya_ble) |
| 💡 **BLE PoC inspiration** | [@redphx](https://github.com/redphx/poc-tuya-ble-fingerbot) |
| 🔧 **Additional contributions** | [@airy10](https://github.com/airy10), [@patriot1889](https://github.com/patriot1889) (incl. light support) |
| 🛠️ **This fork (HA 2024.1+–2026.x compatibility fix)** | This repository |

---

## 🩹 Compatibility Fix

This fork resolves all known compatibility issues with **Home Assistant 2024.1 through 2026.x**, including the widely-reported import errors:

```
cannot import name 'CONF_APP_TYPE' from 'homeassistant.components.tuya.const'
cannot import name 'CONF_ACCESS_ID' from 'homeassistant.components.tuya.const'
cannot import name 'DPType' from 'homeassistant.components.tuya.const'
cannot import name 'CONF_COUNTRY_CODE' from 'homeassistant.components.tuya.const'
Config flow error: {"message":"Invalid handler specified"}
```

These errors occurred because the core Home Assistant Tuya integration removed several constants and types that the original `ha_tuya_ble` and all its forks depended on.

This fork defines all required constants and types **locally**, eliminating the dependency on the core Tuya integration's internals entirely. As of April 2026, the original repo ([PlusPlus-ua/ha_tuya_ble](https://github.com/PlusPlus-ua/ha_tuya_ble)) and other popular forks ([markusg1234/ha_tuya_ble](https://github.com/markusg1234/ha_tuya_ble), [garnser/ha_tuya_ble](https://github.com/garnser/ha_tuya_ble)) remain broken.

---

## 📋 Prerequisites

Before installing, make sure you have:

- ✅ A Tuya BLE device (e.g. Fingerbot) **already paired** to the **Tuya Smart** or **Smart Life** app on your phone
- ✅ A **Tuya IoT Cloud** developer account (see Step 1 below)
- ✅ A Bluetooth adapter accessible to Home Assistant — built-in, USB dongle, or an [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy.html)

---

## 🚀 Step-by-Step Setup Guide

### Step 1 — Create a Tuya IoT Cloud Developer Account

1. Go to [https://iot.tuya.com](https://iot.tuya.com) and create an account (or sign in).
2. Navigate to **Cloud** → **Development** → **Create Cloud Project**.
3. Give your project a name (e.g. `Home Assistant`).
4. **Important:** Select the correct **Data Center** for your region:
   - Western America, Eastern America, Central Europe, Western Europe, India, or China — pick the one matching the region your Tuya/Smart Life app account was registered in.
5. Select **Smart Home** as the development method.
6. After creating the project, note your **Access ID** (Client ID) and **Access Secret** (Client Secret) from the project overview page.

---

### Step 2 — Subscribe to the Required Cloud APIs

In your cloud project, go to **Service API** → **Go to Authorize**. Subscribe to:

| API | Required |
|---|---|
| **IoT Core** | ✅ Required |
| **Authorization Token Management** | ✅ Required |
| **Smart Home Basic Service** | ⭐ Recommended |

All of these are **free** to subscribe to.

---

### Step 3 — Pair Your Device in the Tuya App

1. Open the **Tuya Smart** or **Smart Life** app on your phone.
2. Add your Fingerbot (or other BLE device) following the app's instructions. Make sure Bluetooth is enabled.
3. Verify the device works correctly from within the app.

---

### Step 4 — Link Your App Account to the Cloud Project

1. On [iot.tuya.com](https://iot.tuya.com), go to your cloud project → **Devices** → **Link Tuya App Account**.
2. Click **Add App Account** — a QR code will appear.
3. In the **Tuya Smart** or **Smart Life** app → tap your profile → tap the **scan icon** (top right) → scan the QR code.
4. Confirm the link. Your devices should appear in the **All Devices** list on the cloud project page.
5. Verify your Fingerbot (or BLE device) is listed there.

---

### Step 5 — Install This Integration

**Option A — Via HACS (recommended):**

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** → three-dot menu → **Custom repositories**.
3. Add this repository URL and select **Integration** as the category.
4. Search for **Tuya BLE** in HACS and install it.
5. **Restart Home Assistant.**

**Option B — Manual installation:**

1. Download or clone this repository.
2. Copy the `custom_components/tuya_ble` folder into your HA `/config/custom_components/` directory.
3. **Restart Home Assistant.**

---

### Step 6 — Device Discovery & Credential Setup

After restarting, the integration will automatically discover any Tuya BLE devices within Bluetooth range. You can also trigger discovery manually via **Settings** → **Devices & Services** → **Add Integration** → **Tuya BLE**.

When a new device is found, Home Assistant will prompt you to enter your **Tuya IoT Cloud credentials** directly in the integration's config flow:

- **Access ID / Client ID** — from Step 1
- **Access Secret / Client Secret** — from Step 1
- **Account** — your Tuya/Smart Life app email or phone number
- **Password** — your Tuya/Smart Life app password
- **Country / Data Center** — matching your region from Step 1

The integration uses these credentials **once** to fetch the device's BLE encryption key from the cloud. After that, all communication happens entirely **locally over Bluetooth** — no cloud required for day-to-day operation.

> ⚠️ **Important:** After adding your credentials and completing the device setup, **restart Home Assistant one final time** to ensure everything is fully loaded and the device entities are correctly initialised.

---

## 🔧 Troubleshooting

<details>
<summary><strong>Device not discovered?</strong></summary>

Make sure your HA host has Bluetooth access. If using a VM or container, you may need an [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy.html). Ensure the device is within BLE range (~10 m).

</details>

<details>
<summary><strong>"Device is not registered in Tuya cloud"?</strong></summary>

Make sure the device is linked to your IoT Cloud project (Step 4). Try removing and re-adding the device in the Tuya app, then re-linking the app account on the cloud portal.

</details>

<details>
<summary><strong>Entity shows as unavailable?</strong></summary>

Try pressing the physical button on the device to wake it up — BLE devices often enter deep sleep to save battery and only connect briefly.

</details>

---

## 📦 Supported Devices

<details>
<summary><strong>🤖 Fingerbots</strong> — category <code>szjqr</code></summary>

| Device | Product ID(s) | Notes |
|---|---|---|
| Fingerbot | `ltak7e1p`, `y6kttvd6`, `yrnk7mnn`, `nvr2rocq`, `bnt7wajf`, `rvdceqjh`, `5xhbk964` | Original, CR2 battery |
| Adaprox Fingerbot | `y6kttvd6` | Built-in battery, USB-C charging |
| Fingerbot Plus | `blliqpsj`, `ndvkgsrm`, `yiihr7zh`, `neq16kgd`, `mknd4lci`, `riecov42` | Adds manual sensor button; programming supported |
| CubeTouch 1s | `3yqdo5yt` | Built-in battery, USB-C charging |
| CubeTouch II | `xhf790if` | Built-in battery, USB-C charging |

Programming is supported for **Fingerbot Plus** via entities: `Program` (switch), `Repeat forever`, `Repeats count`, `Idle position`, and `Program` (text).
Program text format: `position[/time];...` — position in %, time in seconds (0 if omitted).

</details>

<details>
<summary><strong>🌡️ Temperature & Humidity Sensors</strong> — categories <code>wsdcg</code>, <code>zwjcy</code></summary>

| Device | Product ID | Category |
|---|---|---|
| Soil moisture sensor | `ojzlzzsw` | `wsdcg` |
| Smartlife Plant Sensor SGS01 | `gvygg3m8` | `zwjcy` |

</details>

<details>
<summary><strong>💨 CO₂ Sensors</strong> — category <code>co2bj</code></summary>

| Device | Product ID |
|---|---|
| CO2 Detector | `59s19z5m` |

</details>

<details>
<summary><strong>🔒 Smart Locks</strong> — category <code>ms</code></summary>

| Device | Product ID(s) |
|---|---|
| Smart Lock | `ludzroix`, `isk2p555`, `gumrixyt` |

</details>

<details>
<summary><strong>🌡️ Climate / TRV</strong> — category <code>wk</code></summary>

| Device | Product ID(s) |
|---|---|
| Thermostatic Radiator Valve | `drlajpqc`, `nhj2j7su` |

</details>

<details>
<summary><strong>💧 Smart Water Bottle</strong> — category <code>znhsb</code></summary>

| Device | Product ID |
|---|---|
| Smart water bottle | `cdlandip` |

</details>

<details>
<summary><strong>🌿 Irrigation Computers</strong> — category <code>ggq</code></summary>

| Device | Product ID |
|---|---|
| Irrigation computer | `6pahkcau` |
| 2-outlet computer SGW02 (MOES BWV-YC02-EU-GY) | `hfgdqhho` |

</details>

<details>
<summary><strong>💡 Lights</strong></summary>

Most light products are supported — the Light class attempts to fetch device descriptions from the cloud on addition. Tested:

| Device | Product ID | Category |
|---|---|---|
| Magiacous RGB light bar | `nvfrtxlq` | `dd` (Strip Lights) |

</details>

---

## ❤️ Support the Original Developer

> *The following message is from the original developer of this integration,* [@PlusPlus-ua](https://github.com/PlusPlus-ua)*, and deserves to remain here.*

I am working on this integration in Ukraine. Our country was subjected to brutal aggression by Russia. The war still continues. The capital of Ukraine — Kyiv, where I live — and many other cities and villages are constantly under threat of rocket attacks. Our air defense forces are doing wonders, but they also need support. So if you want to help the development of this integration, donate some money and I will spend it to support our air defense.

<p align="center">
  <a href="https://www.buymeacoffee.com/3PaK6lXr4l">
    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me an air defense">
  </a>
</p>
```
