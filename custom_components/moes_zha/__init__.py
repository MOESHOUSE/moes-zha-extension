"""MOES ZHA Extension."""

from __future__ import annotations

import logging
from pathlib import Path

import zhaquirks

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

ZHA_DOMAIN = "zha"
QUIRKS_DIR = Path(__file__).parent / "quirks"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up MOES ZHA Extension."""

    if not QUIRKS_DIR.is_dir():
        _LOGGER.error(
            "MOES ZHA quirks directory does not exist: %s",
            QUIRKS_DIR,
        )
        return False

    # Load MOES custom quirks into the ZHA/zigpy registries.
    await hass.async_add_executor_job(
        zhaquirks.setup,
        str(QUIRKS_DIR),
    )

    _LOGGER.info(
        "Loaded MOES ZHA quirks from %s",
        QUIRKS_DIR,
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "quirks_dir": str(QUIRKS_DIR),
    }

    # If ZHA is already running, reload it once so existing devices
    # are reconstructed with the newly registered MOES quirks.
    for zha_entry in hass.config_entries.async_entries(ZHA_DOMAIN):
        if zha_entry.state is ConfigEntryState.LOADED:
            _LOGGER.info(
                "Reloading ZHA config entry %s after loading MOES quirks",
                zha_entry.entry_id,
            )

            await hass.config_entries.async_reload(
                zha_entry.entry_id
            )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload MOES ZHA Extension."""

    domain_data = hass.data.get(DOMAIN)

    if domain_data is not None:
        domain_data.pop(entry.entry_id, None)

        if not domain_data:
            hass.data.pop(DOMAIN, None)

    return True
