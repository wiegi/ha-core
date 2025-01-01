"""Config flow for My USB Radio Integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_DEVICE_PATH,
    CONF_SENSORS,
    DOMAIN,
    SENSOR_TYPE_DOOR,
    SENSOR_TYPE_MOTION,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_PATH, default="/dev/ttyUSB0"): str,
    }
)


class MyUsbRadioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for My USB Radio Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where user enters the USB device path."""
        errors = {}

        if user_input is not None:
            device_path = user_input[CONF_DEVICE_PATH]

            # (Optional) Validate the device path if necessary
            if not device_path:
                errors["base"] = "invalid_path"
            else:
                # Create the entry
                # Store the device path in data, and initialize options with an empty sensor list.
                return self.async_create_entry(
                    title="USB Radio",
                    data={
                        CONF_DEVICE_PATH: device_path,
                    },
                    options={
                        CONF_SENSORS: [],
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return MyUsbRadioOptionsFlowHandler(config_entry.entry_id)


class MyUsbRadioOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle adding/removing sensors in the options flow."""

    def __init__(self, entry_id: str) -> None:
        """Store only the entry_id, not the entire ConfigEntry."""
        self._entry_id = entry_id

    @property
    def config_entry(self) -> config_entries.ConfigEntry | None:
        """Retrieve the current config entry from Home Assistant."""
        return self.hass.config_entries.async_get_entry(self._entry_id)

    @property
    def sensors(self) -> list[dict]:
        """Return the current list of sensors from config_entry.options."""
        if self.config_entry is None:
            return []
        return list(self.config_entry.options.get(CONF_SENSORS, []))

    async def async_step_init(self, user_input=None):
        """First screen of the options flow - menu or direct form."""
        return self.async_show_menu(
            step_id="init",
            menu_options={"add_sensor": "Add Sensor", "remove_sensor": "Remove Sensor"},
        )

    async def async_step_add_sensor(self, user_input=None):
        """Add a new sensor."""
        errors = {}
        schema = vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("address"): str,
                vol.Required("type", default=SENSOR_TYPE_DOOR): vol.In(
                    [SENSOR_TYPE_DOOR, SENSOR_TYPE_MOTION]
                ),
            }
        )

        if user_input is not None:
            new_sensor = {
                "name": user_input["name"],
                "address": user_input["adress"],
                "type": user_input["type"],
            }
            updated_sensors = self.sensors
            updated_sensors.append(new_sensor)
            # Create a new options entry containing the updated list:
            return self.async_create_entry(
                title="", data={CONF_SENSORS: updated_sensors}
            )

        return self.async_show_form(
            step_id="add_sensor", data_schema=schema, errors=errors
        )

    async def async_step_remove_sensor(self, user_input=None):
        """Remove an existing sensor."""
        errors = {}
        sensor_names = [s["name"] for s in self.sensors]
        if not sensor_names:
            return self.async_abort(reason="no_sensors_to_remove")

        schema = vol.Schema(
            {
                vol.Required("sensor_name"): vol.In(sensor_names),
            }
        )

        if user_input is not None:
            sensor_name_to_remove = user_input["sensor_name"]
            updated_sensors = [
                s for s in self.sensors if s["name"] != sensor_name_to_remove
            ]
            return self.async_create_entry(
                title="", data={CONF_SENSORS: updated_sensors}
            )

        return self.async_show_form(
            step_id="remove_sensor", data_schema=schema, errors=errors
        )

    async def async_step_finish(self, user_input=None):
        """Finish the options flow."""
        return self.async_create_entry(title="", data=self.config_entry.options)
