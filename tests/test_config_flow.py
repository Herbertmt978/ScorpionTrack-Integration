"""Config-flow tests for the standalone ScorpionTrack integration repo."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.config_entries import SOURCE_USER
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.core import HomeAssistant
from tests.common import MockConfigEntry

from custom_components.scorpiontrack.const import CONF_SHARE_TOKEN, DOMAIN


VALIDATION_INFO = {
    "token": "canonical-token",
    "title": "Family Cars",
    "unique_id": "share-101",
}


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """A valid token should create a config entry."""
    with patch(
        "custom_components.scorpiontrack.config_flow._async_validate_input",
        return_value=VALIDATION_INFO,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={CONF_SHARE_TOKEN: "https://app.scorpiontrack.com/shared/location?token=abc"},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Family Cars"
    assert result["data"] == {CONF_SHARE_TOKEN: "canonical-token"}


async def test_user_flow_aborts_for_existing_share(hass: HomeAssistant) -> None:
    """The same share should not be configured twice."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Family Cars",
        unique_id="share-101",
        data={CONF_SHARE_TOKEN: "existing-token"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.scorpiontrack.config_flow._async_validate_input",
        return_value=VALIDATION_INFO,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={CONF_SHARE_TOKEN: "new-token"},
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
