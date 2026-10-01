# Backend market repair report — 2026-10-01

Implemented backend work for the off-game market, payment verification, durable delivery claims, missions, and progress persistence. The changes use owner-scoped database reads, revision-checked progress saves, persisted order/claim idempotency markers, and durable pending inbox entitlements. Quote creation and renewal use compare-and-set guards; submitted transaction hashes are reserved before RPC verification so RPC outages remain recoverable by retrying the same hash. The server now exposes the owned mission roster and UTC server time, and mission start can atomically recall an explicitly selected active soldier.

VIP expiry is restored from persisted account state and refreshed from the database before live actor persistence, so a live market save does not overwrite a newly purchased expiry with a stale actor snapshot. The live actor also applies persisted grants and claim results idempotently.

Focused verification on this machine:

```powershell
& .\backend\.venv\Scripts\python.exe -m pytest backend/tests/test_market_durability_regression.py backend/tests/test_offgame_market_and_economy.py backend/tests/test_soldier_ws_account_regression.py -q
```

Result: **17 passed**, with two Starlette/AnyIO deprecation warnings. `compileall` passed for the touched backend modules. Tests use isolated mongomock databases and temporary storage paths; they do not write live user progress.

Payment verification is mocked; no wallet signature, live transfer, or on-chain payment was performed. The verifier requires two confirmations, which are a soft confirmation threshold and do not represent Ethereum L1 finality. Hash reservation is deliberately immutable after submission: a malformed-format hash is rejected, but a syntactically valid hash that later proves absent or invalid remains bound for same-hash retry/support review rather than allowing an unsafe replacement.

References: [Coinbase Prices API](https://docs.cdp.coinbase.com/coinbase-app/track-apis/prices); [Robinhood Chain: add network to wallet](https://docs.robinhood.com/chain/add-network-to-wallet/); [Robinhood Chain transaction finality](https://docs.robinhood.com/chain/transaction-finality/).

## Post-restart API QA

Backend was restarted on 2026-10-01 and checked through the live local API. Catalog returned HTTP 200; unauthenticated orders returned HTTP 401. The configured treasury address matched the expected value, chain 4663 was reported, and the catalog prices matched 1000 / 2000 / 3500 / 6000. Luck Box odds reported 15 draws. No funds were sent.
