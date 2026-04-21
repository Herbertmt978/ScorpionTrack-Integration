"""Coordinator for ScorpionTrack."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyscorpiontrack import (
    ScorpionTrackClient,
    ScorpionTrackConnectionError,
    ScorpionTrackInvalidTokenError,
    ScorpionTrackShare,
    ScorpionTrackShareUnavailableError,
)
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .utils import mask_token

_LOGGER = logging.getLogger(__name__)


class ScorpionTrackCoordinator(DataUpdateCoordinator[ScorpionTrackShare]):
    """Coordinate shared-location updates."""

    def __init__(self, hass: HomeAssistant, client: ScorpionTrackClient) -> None:
        """Initialize the coordinator."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{mask_token(client.token)}",
            update_interval=DEFAULT_SCAN_INTERVAL,
            always_update=False,
        )

    async def _async_update_data(self) -> ScorpionTrackShare:
        """Fetch updated share data."""
        try:
            return await self.client.async_get_share()
        except ScorpionTrackConnectionError as err:
            raise UpdateFailed(f"Could not reach ScorpionTrack: {err}") from err
        except ScorpionTrackInvalidTokenError as err:
            raise UpdateFailed(
                f"ScorpionTrack rejected the configured share token: {err}"
            ) from err
        except ScorpionTrackShareUnavailableError as err:
            raise UpdateFailed(f"Shared location is unavailable: {err}") from err
