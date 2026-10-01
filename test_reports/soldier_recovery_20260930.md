# Soldier recovery verification — 30 September 2026

Validated with the backend virtual environment:

`backend/.venv/Scripts/python.exe -m pytest backend/tests/test_soldier_energy_focus.py backend/tests/test_soldier_ws_account_regression.py backend/tests/test_network_channel_focus.py -q`

Result: 17 passed. Coverage includes the exact 120-second UTC boundary, independent companion deadlines, deactivate/upgrade preservation, fresh actor restoration with monotonic shot/reload timers reset, immutable ordered account persistence, and existing WebSocket roster/account regression coverage.

The HUD test validates owner-only death alerts and two independent right-bottom `mm:ss` companion recovery clocks. `npm run build` completed; its pre-existing optional wagmi connector resolution warnings remain.
