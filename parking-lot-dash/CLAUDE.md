# Claude Rules — Parking Lot Dash

## Project Context
IoT parking lot control dashboard for VŠB-TUO BroadbandLIGHT project.
- **MQTT** controls DALI lights (10 poles, 18 devices) and 3 beacons
- **Dash** (Plotly/Flask) serves the web UI
- **Weather** via Telnet (GIOM 3000), **Cameras** proxied through Flask
- Deployed to `parkoviste@158.196.15.41`; start everything via `scripts/start.sh`

## Single Entry Point
`scripts/start.sh` must start the full system — Dash app, MQTT client, and any future services (e.g. DALI bridge).
Never require the user to start services manually in separate terminals.

## Code Structure
```
src/
  app.py                    # App init, server export, client wiring — nothing else
  mqtt_client.py            # MQTT connection + device commands
  weather_client.py         # Telnet weather client
  ui/
    layout.py               # Root layout — sidebar + main content + camera panel wiring
    screens/                # One file per screen (lights.py, beacons.py, weather.py, dashboard.py)
    toolkit/                # Design system — single source of truth for style + shared components
      theme.py              # COLORS dict + style() helper — only place raw hex strings live
      components/           # Every reusable component (light_card.py, beacon_switch.py, camera_feed.py, sidebar.py, auth_guard.py, ...)
  callbacks/                # Dash callbacks grouped by domain (lights.py, beacons.py, cameras.py, weather.py)
config/
  devices.py                # All device config, IPs, MQTT topics — single source of truth
scripts/                    # Shell and standalone Python utilities
```

- Keep `src/app.py` thin — init only (Dash app, Flask server, clients, route registration)
- Never put callbacks or layout HTML directly in `app.py`
- One screen per file in `ui/screens/`
- Every component that could appear on more than one screen goes in `ui/toolkit/components/` — not inside a screen file
- Import colors only from `src/ui/toolkit/theme.py` — never use raw hex strings anywhere else
- MQTT topic strings only in `config/devices.py` — never hardcode elsewhere

## Config
- This is a single-use deployed app — hardcoding IPs, ports, and credentials directly in `config/devices.py` is fine
- No `.env` complexity needed; keep all config in one place: `config/devices.py`

## Auth & Roles
Two roles, no in-between:

| Role | Access |
|------|--------|
| **Visitor** (logged out) | Read-only — can view lights, cameras, weather, status |
| **Admin** (logged in) | Full control — can change lights, beacons, any device state |

### Rules
- Auth state is stored in `dcc.Store('auth-state')` in the root layout — available to all callbacks
- Every callback that triggers a write action (MQTT publish, device command) **must** check auth state first and do nothing if the user is not admin
- On the UI side, all interactive controls (sliders, switches, buttons) are **disabled** for visitors — not hidden, disabled — so the layout does not shift
- The sidebar shows a login/logout button reflecting current state
- A login screen/modal is the only way to become admin; credentials defined in `config/devices.py`
- `ui/components/` must include an `auth_guard.py` helper that wraps the role check so every callback uses the same logic — never inline the check

## UI Conventions
- **No emojis** anywhere in the UI
- **Python + Dash only** — use `dash`, `dash_bootstrap_components`, `dash_daq`; no JS frameworks
- UI labels stay in **Czech** (Osvětlení, Majáčky, Meteostanice, Kamery, Stožár)
- **Color palette** — defined below, always use these tokens, never raw hex elsewhere in code
- **Font Awesome icons** for all icons (via `dbc.icons.FONT_AWESOME`)

### Color Palette
All colors are defined once in `src/ui/toolkit/theme.py` and imported wherever needed. Never use raw hex strings outside of `theme.py`.

```python
COLORS = {
    # Brand
    "primary":          "#004D40",
    "primary_600":      "#00332B",
    "primary_300":      "#2A7D72",
    "accent":           "#00C853",
    "accent_700":       "#00A63F",
    # Backgrounds
    "bg":               "#0B1214",
    "surface":          "#102022",
    "surface_variant":  "#0E1A1C",
    # Text
    "text_primary":     "#E6F7EF",
    "text_secondary":   "#8AA39A",
    # Semantic
    "info":             "#00E5FF",
    "success":          "#00C853",
    "danger":           "#E74C3C",
    "border":           "#183233",
    # Glows (use sparingly — active states, CTAs)
    "glow_cyan":        "rgba(0,229,255,0.08)",
    "glow_green":       "rgba(0,200,83,0.18)",
}
```

**Usage rules:**
- Header / sidebar background: `primary` on `bg`, text in `text_primary`
- Cards / panels: `surface` background, `border` border, subtle box-shadow
- Active / CTA buttons: `accent` with `glow_green` box-shadow
- Device online: `success` icon + label; device offline: `danger` icon + label — always both, never color alone
- Secondary info, tooltips, chips: `info` (cyan)
- Body text: `text_primary`; muted/secondary text: `text_secondary`
- WCAG AA contrast must hold for all text on their background — if a combination fails, lighten the text token

### Layout
```
+------------------+----------------------------------+
|                  |                                  |
|   LEFT SIDEBAR   |         MAIN CONTENT             |
|                  |         (active screen)          |
|  - Nav links     |                                  |
|  - Controls      |                                  |
|  - Status        +----------------------------------+
|                  |   CAMERA PANEL (sticky/pinned)   |
|                  |   always visible, switchable     |
+------------------+----------------------------------+
```
- Navigation and screen-switching controls live in the **left sidebar** — not in top tabs
- Camera panel is **pinned to a fixed region** of the screen; switching screens does not hide it
- User can select which camera is displayed in the camera panel without leaving the current screen
- DAQ widgets (sliders, switches) for physical device controls

## Testing
- After any MQTT change: run `python scripts/test_mqtt.py`
- After any camera change: run `python scripts/test_camera_urls.py`
- After any light change: run `python scripts/test_light_status.py`
- For new features, write a focused test script in `scripts/test_<feature>.py`
- Prefer small, runnable scripts over framework-heavy test suites unless the project grows

## Documentation
- No markdown files unless explicitly requested
- No docstrings on obvious functions
- Inline comments only where logic is non-obvious
- Keep this CLAUDE.md updated when architecture changes

## Workflow
- Read the relevant file before modifying it
- After making changes, test them (run the app or a targeted script)
- Prefer editing existing files over creating new ones
- No backwards-compat shims — if something is renamed, rename it everywhere
