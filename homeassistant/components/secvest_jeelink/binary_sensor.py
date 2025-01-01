"""Binary sensor platform for My USB Radio Integration."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SENSORS, SENSOR_TYPE_DOOR, SENSOR_TYPE_MOTION

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up binary sensors based on the config entry."""
    sensors = entry.options.get(CONF_SENSORS, [])
    entities = []

    for sensor_config in sensors:
        name = sensor_config["name"]
        address = sensor_config["address"]
        sensor_type = sensor_config["type"]

        if sensor_type == SENSOR_TYPE_DOOR:
            entities.append(MyDoorBinarySensor(name, address, entry))
        elif sensor_type == SENSOR_TYPE_MOTION:
            entities.append(MyMotionBinarySensor(name, address, entry))

    async_add_entities(entities, True)


class MyDoorBinarySensor(BinarySensorEntity):
    """Representation of a door binary sensor."""

    def __init__(self, name: str, address: str, entry: ConfigEntry):
        self._attr_name = name
        self._address = address
        self._entry = entry
        self._attr_device_class = BinarySensorDeviceClass.DOOR
        self._state = False

    @property
    def is_on(self) -> bool:
        return self._state

    def update_state(self, new_state: bool):
        self._state = new_state
        self.schedule_update_ha_state()


class MyMotionBinarySensor(BinarySensorEntity):
    """Representation of a motion binary sensor."""

    def __init__(self, name: str, address: str, entry: ConfigEntry):
        self._attr_name = name
        self._address = address
        self._entry = entry
        self._attr_device_class = BinarySensorDeviceClass.MOTION
        self._state = False

    @property
    def is_on(self) -> bool:
        return self._state

    def update_state(self, new_state: bool):
        self._state = new_state
        self.schedule_update_ha_state()
