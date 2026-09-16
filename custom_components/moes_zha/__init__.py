"""MOES ZHA Extension."""

from __future__ import annotations

import logging
from pathlib import Path

import zhaquirks

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

QUIRKS_DIR = Path(__file__).parent / "quirks"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up MOES ZHA Extension."""

    _LOGGER.warning(
        "MOES_TEST_1 Extension setup started"
    )

    _LOGGER.warning(
        "MOES_TEST_2 Quirks directory: %s exists=%s",
        QUIRKS_DIR,
        QUIRKS_DIR.is_dir(),
    )

    await hass.async_add_executor_job(
        zhaquirks.setup,
        str(QUIRKS_DIR),
    )

    _LOGGER.warning(
        "MOES_TEST_3 zhaquirks.setup completed"
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "quirks_dir": str(QUIRKS_DIR),
    }

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload MOES ZHA Extension."""

    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
