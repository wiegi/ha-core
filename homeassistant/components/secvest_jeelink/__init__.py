"""Initialization of My USB Radio Integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_DEVICE_PATH, CONF_SENSORS, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""

    device_path = entry.data.get(CONF_DEVICE_PATH)
    # sensors are now stored in entry.options
    sensors = entry.options.get(CONF_SENSORS, [])

    _LOGGER.debug("Setting up USB radio at: %s", device_path)
    _LOGGER.debug("Sensors in options: %s", sensors)

    # TODO: Open serial, if needed

    # Forward the binary_sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration when user removes it or disables it."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["binary_sensor"]
    )
    if unload_ok:
        # Close resources if needed
        _LOGGER.debug("Unloaded integration for %s", entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Reload the config entry when options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)
