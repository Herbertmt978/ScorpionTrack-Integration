# ScorpionTrack Core Submission Checklist

This repo is the staging area for a Home Assistant Core submission that only covers ScorpionTrack shared-location links.

The official Home Assistant guidance driving this split is:

- contributing integrations to Core: [developers.home-assistant.io/docs/core/integration/contributing_to_core](https://developers.home-assistant.io/docs/core/integration/contributing_to_core)
- integration quality scale: [developers.home-assistant.io/docs/core/integration-quality-scale](https://developers.home-assistant.io/docs/core/integration-quality-scale)
- development checklist: [developers.home-assistant.io/docs/development_checklist](https://developers.home-assistant.io/docs/development_checklist)
- Python library guide: [developers.home-assistant.io/docs/api_lib_index](https://developers.home-assistant.io/docs/api_lib_index)

## What This Repo Already Does

- limits scope to the public share-link flow
- uses a UI config flow
- stores runtime state in `ConfigEntry.runtime_data`
- prevents duplicate setup with a unique config entry ID
- validates the share during setup
- keeps the initial Core candidate to a single platform
- keeps entity unique IDs stable

## What Still Has To Happen Before A Real Core PR

### External library

- publish `python-scorpiontrack` as `pyscorpiontrack` on PyPI
- tag a public release that matches the pinned manifest version
- make sure the library issue tracker is live

### Home Assistant documentation and branding

- submit the ScorpionTrack docs page to `home-assistant.io`
- submit brand assets to `home-assistant/brands`
- keep local brand assets out of the Core integration tree
- document installation, scope, removal, and the absence of service actions in the final docs page

### Core PR work

- copy the integration into Home Assistant Core
- wire the new dependency into Core requirements
- run the full Home Assistant test suite for the integration inside the Core tree
- satisfy review feedback on typing, tests, naming, and docs wording

## Intentional Scope Decision

This repo is not trying to sneak the full private portal integration into Core by degrees.

The purpose is the opposite: isolate the smallest public, maintainable ScorpionTrack surface that is realistic for upstream review. The account-login path belongs in the custom integration repo, not this one.
