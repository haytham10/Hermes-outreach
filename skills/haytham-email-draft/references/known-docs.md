# Known Notion Docs — Current vs Outdated

## Current / Reliable — read the LOCAL cache, never fetch from Notion

Canonical copies live at `~/projects/hermes-outreach/docs/`. The Notion IDs below are provenance only; fetching these pages from Notion wastes tokens and risks drift.

| Doc | Notion ID | When to use |
|---|---|---|
| The Bible | `383382c8-4585-81ce-9f60-ecf42658b0ae` | Methodology: funnel walk, targeting, rules, lanes, artifact engine. Some sections may be stale but the core is reliable. |
| Email OS | `387382c8-4585-81ba-91e1-e4bde838a339` | Cold email mechanics: finding emails, writing, follow-up sequences, tracking. |
| SMYKM Test Layer | `389382c8-4585-8174-a5b4-d2b0194dcfc1` | Subject line rules, 48h bump test, human-first research layer. |
| The Drafting Doc | `389382c8-4585-811d-8782-fa23ffd2e5ee` | Harry Dry copywriting: visualize, falsify, bespoke. |
| Haytham's Voice | `389382c8-4585-8130-85ec-ef54bb73813a` | Tone, belief system, kill list. |
| Grand Slam Offer v2 | `391382c8-4585-817a-8307-c9e91dbf01b8` | Current pricing: Track A $200 / Track B $700. |
| PWH Case Study | `35a382c8-4585-8142-8e72-f12124daa0fc` | Proof asset for calls and proposals. |

## Outdated / Do NOT fetch

| Doc | Reason |
|---|---|
| Prompt Starter | Old Claude session start sequence. Replaced by Hermes skills. |
| Launch Support Framework | Dec 2025 client deliverable for Dr. Hanaa, not current. |
| The Offer (390382c8-4585-810c-a42d-c44c0b3da0c2) | Superseded by Grand Slam Offer v2. |
| Sourced Leads — Batch 1 | Stale batch data. Pipeline is the source of truth. |

## Always fetch from Notion for live state

- **Lead Pipeline** — never trust chat memory for pipeline state.
  - MCP data source ID: `c6209e29-55ef-4781-b735-73b2a254e34f`
  - REST API database ID: `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6`
- Any lead's individual page — always re-fetch before editing (needs exact character matching).