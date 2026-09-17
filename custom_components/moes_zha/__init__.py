"""MOES ZHA Extension."""

from __future__ import annotations

import logging
from pathlib import Path

import zhaquirks

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import CoreState, Event, HomeAssistant

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

QUIRKS_DIR = Path(__file__).parent / "quirks"


async def _async_reload_zha(hass: HomeAssistant) -> None:
    """Reload ZHA after MOES quirks have been registered."""

    for zha_entry in hass.config_entries.async_entries("zha"):
        if zha_entry.state is not ConfigEntryState.LOADED:
            continue

        _LOGGER.info(
            "Reloading ZHA to apply MOES quirks"
        )

        await hass.config_entries.async_reload(
            zha_entry.entry_id
        )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up MOES ZHA Extension."""

    await hass.async_add_executor_job(
        zhaquirks.setup,
        str(QUIRKS_DIR),
    )

    _LOGGER.info(
        "MOES ZHA quirks registered from %s",
        QUIRKS_DIR,
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "quirks_dir": str(QUIRKS_DIR),
    }

    async def _reload_after_start(
        event: Event | None = None,
    ) -> None:
        await _async_reload_zha(hass)

    if hass.state is CoreState.running:
        # MOES integration was loaded/reloaded while HA is already running.
        hass.async_create_task(
            _reload_after_start()
        )
    else:
        # During HA startup, wait until normal startup has finished
        # before restarting ZHA.
        remove_listener = hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED,
            _reload_after_start,
        )
        entry.async_on_unload(remove_listener)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload MOES ZHA Extension."""

    hass.data.get(DOMAIN, {}).pop(
        entry.entry_id,
        None,
    )

    return True
