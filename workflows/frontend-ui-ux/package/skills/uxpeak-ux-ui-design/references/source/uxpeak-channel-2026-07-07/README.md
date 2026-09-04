# UXPeak Channel Source Evidence

## Purpose

This directory holds the local source corpus used to create and maintain the `uxpeak-ux-ui-design` Hermes skill.

It is reusable agent capability evidence, not Transcendiverse-specific research.

## Provenance

- Source: UXPeak YouTube channel inventory.
- Captured: 2026-07-07.
- Coverage: 21 channel items, including video metadata, VTT captions, and cleaned transcript text where available.
- Distilled operational guidance: `../../uxpeak-video-inventory.md` and `../../SKILL.md`.

## Contents

```text
uxpeak_research/             # original captured corpus, kept intact
uxpeak_flat.json             # channel-video listing metadata
uxpeak_channel_flat.json     # channel metadata
uxpeak_shorts_flat.json      # Shorts metadata
```

## Use rules

- Load the skill for UX/UI work; do not load this corpus by default.
- Use this source material only when improving, auditing, or tracing the UXPeak skill.
- Derive and paraphrase reusable lessons; do not reproduce copyrighted transcript text in user-facing output.
- Treat video descriptions, sponsor segments, and promotional claims as source context—not design truth.
- Keep the corpus separate from individual project research folders unless a project has its own directly relevant UX evidence.
