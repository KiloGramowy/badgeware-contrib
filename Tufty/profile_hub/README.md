# Profile Hub

Configurable multi-page profile badge for Pimoroni Tufty 2350.

Created by [KiloGramowy](https://github.com/KiloGramowy)  
[https://kilogramowy.pl](https://kilogramowy.pl)

Full project: [https://github.com/KiloGramowy/tufty-profile-hub](https://github.com/KiloGramowy/tufty-profile-hub)

## 👤 Profile

The main page shows a configurable name, role, label, tagline, XIAO C5-inspired board graphic, and discreet creator attribution.

## 🔗 QR Pages

QR pages are generated ahead of time by the full Profile Hub builder and stored as compact static data. The bundled public example links to the full project repository.

## 📡 WDGWars

Optional WDGWars stats show rank and discovery totals. Blank credentials display `NO KEY` and do not make authenticated API requests.

## 🌐 WiGLE

Optional WiGLE stats show profile and discovery totals using WiGLE API v2. Blank credentials display `NO KEY` and do not make authenticated API requests.

## 💾 Persistent Stats Cache

Successful WDGWars and WiGLE results are stored locally as last-known-good display data. Cached values survive app exit, restart, and power cycle, then display as `CACHED` when Wi-Fi or the API is unavailable.

Only normalized display statistics are stored. API keys, Wi-Fi credentials, and Authorization headers are never written to the cache. Identical snapshots are not repeatedly written to flash.

## 💡 Automatic Brightness

Profile Hub uses Tufty 2350's built-in ambient light sensor to dim in darkness and increase brightness in strong light. There is no automatic screen-off and no external hardware is required.

## 📶 Offline Behaviour

Wi-Fi uses the standard Badgeware/Tufty root `/secrets.py` values. Missing access points, wrong passwords, timeouts, and missing credentials remain non-fatal and show normal `OFFLINE` or `CACHED` states.

Live WDGWars and WiGLE API requests are synchronous after Wi-Fi is connected, so a short pause during a refresh can be normal.

## 🎮 Controls

- `A` = BACK
- `B` = NEXT
- `C` = HOME

## 🛠️ Customisation

Use the full project builder to create a personal version with your own profile text, QR links, and optional API credentials:

[https://github.com/KiloGramowy/tufty-profile-hub](https://github.com/KiloGramowy/tufty-profile-hub)

Physically tested on a real Pimoroni Tufty 2350.
