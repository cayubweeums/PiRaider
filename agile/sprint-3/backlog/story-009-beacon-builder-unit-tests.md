# [STORY-009] Beacon builder unit tests

## Summary

Add unit tests for the beacon frame builder: frame length, presence of SSID and BSSID in the frame, and optional random BSSID behavior.

## Description

The PoC requires that every new tool adds tests. The beacon builder (story 008) must be covered by unit tests so that parsing and frame construction are validated without hardware.

**Scope:**
- Tests in `tests/` (e.g. `tests/test_beacon.py` or `tests/core/test_beacon.py`).
- Assert: (1) For a given SSID, the returned bytes have minimum expected length and contain the SSID in the correct place (SSID IE). (2) BSSID/SA are present and, when random is requested, are 6 bytes and equal (SA = BSSID). (3) DA is 0xff:ff:ff:ff:ff:ff. (4) Frame control indicates beacon (0x80 0x00 for management/beacon). (5) Edge cases: empty SSID, very long SSID (truncation or rejection per story 008).
- No dependency on real WiFi hardware or injection. All tests use the builder API only.
- `poetry run pytest` passes.

**ESP32 Marauder:** N/A — tests only; structure is validated against the known beacon format.

## Acceptance criteria

- [ ] There is a test file that imports and tests the beacon builder from core.
- [ ] At least one test asserts the built frame contains the given SSID in the SSID IE.
- [ ] At least one test asserts BSSID/SA are present and consistent (e.g. SA = BSSID when random).
- [ ] At least one test asserts DA is broadcast (0xff:ff:ff:ff:ff:ff).
- [ ] At least one test asserts frame type is beacon (FC bytes).
- [ ] Edge cases: empty SSID and/or long SSID covered as per implementation.
- [ ] `poetry run pytest` passes.

## Definition of done

- Code merged. All new tests pass. No regressions. KISS: minimal test code.

## Subtasks / notes

- SSID IE: tag 0x00, length 1 byte, then SSID. Locate in frame by scanning for 0x00 followed by length.
