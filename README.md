# ScorpionTrack

[![Syntax](https://github.com/Herbertmt978/ScorpionTrack-Integration/actions/workflows/validate.yml/badge.svg)](https://github.com/Herbertmt978/ScorpionTrack-Integration/actions/workflows/validate.yml)
[![Hassfest](https://github.com/Herbertmt978/ScorpionTrack-Integration/actions/workflows/hassfest.yml/badge.svg)](https://github.com/Herbertmt978/ScorpionTrack-Integration/actions/workflows/hassfest.yml)

This repository is the clean Home Assistant Core candidate for the public ScorpionTrack share-link flow.

It exists for a narrow reason: the share link is the safest, most reviewable ScorpionTrack surface to take upstream. The full account-login path can stay in the separate custom-integration or HACS repo, while this repo focuses on the one part that has a realistic chance of being accepted into Home Assistant Core.

## What This Repo Covers Right Now

- ScorpionTrack shared-location links only
- UI setup through Home Assistant config flows
- one `device_tracker` per shared vehicle
- a deliberately minimal first-pass Core scope

## What This Repo Deliberately Does Not Cover

- ScorpionTrack account login
- private portal scraping
- HACS packaging metadata
- unofficial write actions or remote controls
- extra share metadata sensors
- binary sensors
- diagnostics in the initial Core PR
- reconfigure helpers in the initial Core PR

That split is intentional. For Core, the goal is a small, understandable, low-risk integration built on the public share mechanism.

## Repository Layout

- `custom_components/scorpiontrack`
  The Home Assistant integration candidate.
- `tests`
  Home Assistant-style tests for the config flow and setup path.
- `docs/core-submission-checklist.md`
  A working checklist for what still has to happen before the real Core PR.

This repo also expects a sibling external library repo named `python-scorpiontrack`, because Home Assistant Core requires protocol and service communication to live outside the integration package.

## Required Sibling Library

Home Assistant Core does not accept integrations that embed all service communication inside the integration itself. The ScorpionTrack share client has therefore been split into a separate Python package:

- sibling repo/package: `python-scorpiontrack`
- import name: `pyscorpiontrack`

Before a real Core submission, that library needs to be published to PyPI and referenced by a tagged public release.

## Local Development Setup

If you want to test this repo locally before any upstream submission:

1. Install the sibling library into the same Python environment Home Assistant uses:
   `pip install -e ../python-scorpiontrack`
2. Copy `custom_components/scorpiontrack` into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.
4. Open `Settings` -> `Devices & services`.
5. Add `ScorpionTrack`.
6. Paste either a full ScorpionTrack shared-location URL or the raw token from that URL.

## Creating a Share Link

Create the share in ScorpionTrack here:

`https://app.scorpiontrack.com/customer/locationshare`

1. Create a location-share entry in ScorpionTrack.
2. Add every vehicle you want Home Assistant to track.
3. Choose an expiry that suits your use case.
4. Copy the generated shared-location URL or token.

One ScorpionTrack share can include multiple vehicles, and this integration imports every vehicle exposed by that single share.

## Entity Model

For the first Home Assistant Core submission, the integration creates:

- a `device_tracker` for each vehicle included in the ScorpionTrack share

That is intentional. Home Assistant's current contribution guidance recommends keeping a new integration PR as small as possible, ideally to a single platform. Extra sensors and secondary features can be layered in later if the base integration is accepted.

## Behaviour Notes

- The config entry stores only the extracted share token.
- Data refreshes every 2 minutes.
- If the share expires, is revoked, or stops returning usable data, the integration will fail setup cleanly or mark entities unavailable on refresh.
- The `device_tracker` keeps Home Assistant zone handling intact while still exposing supporting location context through attributes.
- Speed is normalized in tracker attributes using the share's preferred distance units.

## Privacy Notes

Anyone with a valid ScorpionTrack share token may be able to access that shared-location feed, so treat the URL as sensitive.

This repo does not include live tokens.

## Relationship To The Other Repo

If you want the broader custom-integration path, including the account-login work, use the separate HACS-oriented repo instead.

This repository is the narrower upstream candidate: public share links only, smaller scope, cleaner review surface.

## Removal

To remove the integration from a local custom-components test setup:

1. Remove the ScorpionTrack config entry from Home Assistant.
2. Delete `custom_components/scorpiontrack`.
3. Restart Home Assistant.
4. If you no longer need the sibling client library in that environment, uninstall `pyscorpiontrack`.
