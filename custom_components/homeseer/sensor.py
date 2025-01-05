"""Support for HomeSeer sensor-type devices."""

import logging
from libhomeseer import (
    DEVICE_ZWAVE_BATTERY,
    DEVICE_ZWAVE_DOOR_LOCK_LOGGING,
    DEVICE_ZWAVE_ELECTRIC_METER,
    DEVICE_ZWAVE_FAN_STATE,
    DEVICE_ZWAVE_LUMINANCE,
    DEVICE_ZWAVE_OPERATING_STATE,
    DEVICE_ZWAVE_RELATIVE_HUMIDITY,
    DEVICE_ZWAVE_SENSOR_MULTILEVEL,
    HS_UNIT_A,
    HS_UNIT_AMPERES,
    HS_UNIT_CELSIUS,
    HS_UNIT_FAHRENHEIT,
    HS_UNIT_KW,
    HS_UNIT_KWH,
    HS_UNIT_LUX,
    HS_UNIT_PERCENTAGE,
    HS_UNIT_V,
    HS_UNIT_VOLTS,
    HS_UNIT_W,
    HS_UNIT_WATTS,
    get_uom_from_status,
)

from homeassistant.const import (
    LIGHT_LUX,
    PERCENTAGE,
    UnitOfElectricPotential,  # Updated import
    UnitOfTemperature,
    UnitOfPower,
    UnitOfElectricCurrent,
    UnitOfEnergy,
)
from .const import DOMAIN
from .homeseer import HomeSeerEntity

_LOGGER = logging.getLogger(__name__)

GENERIC_VALUE_SENSOR_TYPES = [
    DEVICE_ZWAVE_ELECTRIC_METER,
    DEVICE_ZWAVE_LUMINANCE,
    DEVICE_ZWAVE_SENSOR_MULTILEVEL,
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer sensor-type devices."""
    sensor_entities = []
    bridge = hass.data[DOMAIN]

    for device in bridge.devices["sensor"]:
        entity = get_sensor_entity(device, bridge)
        sensor_entities.append(entity)
        _LOGGER.info(
            f"Added HomeSeer sensor-type device: {entity.name} ({entity.device_state_attributes})"
        )

    if sensor_entities:
        async_add_entities(sensor_entities)


class HomeSeerStatusSensor(HomeSeerEntity):
    """Base representation of a HomeSeer sensor-type device that reports text values (status)."""

    @property
    def state(self):
        return self._device.status


class HomeSeerValueSensor(HomeSeerEntity):
    """Base representation of a HomeSeer sensor-type device that reports numeric values."""

    @property
    def state(self):
        return self._device.value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement parsed from the device's status."""
        unit = get_uom_from_status(self._device.status)
        if unit == HS_UNIT_LUX:
            return LIGHT_LUX
        elif unit == HS_UNIT_CELSIUS:
            return UnitOfTemperature.CELSIUS
        elif unit == HS_UNIT_FAHRENHEIT:
            return UnitOfTemperature.FAHRENHEIT
        elif unit == HS_UNIT_PERCENTAGE:
            return PERCENTAGE
        elif unit == HS_UNIT_A or unit == HS_UNIT_AMPERES:
            return UnitOfElectricCurrent.AMPERE
        elif unit == HS_UNIT_KW:
            return UnitOfPower.KILO_WATT
        elif unit == HS_UNIT_KWH:
            return UnitOfEnergy.KILO_WATT_HOUR
        elif unit == HS_UNIT_V or unit == HS_UNIT_VOLTS:
            return UnitOfElectricPotential.VOLT  # Updated usage
        elif unit == HS_UNIT_W or unit == HS_UNIT_WATTS:
            return UnitOfPower.WATT
        return None

    @property
    def device_class(self):
        """Return the device class of the device based on the device's unit of measure."""
        unit = get_uom_from_status(self._device.status)
        if unit == HS_UNIT_LUX:
            return "illuminance"
        elif unit == HS_UNIT_CELSIUS or unit == HS_UNIT_FAHRENHEIT:
            return "temperature"
        elif unit == HS_UNIT_A or unit == HS_UNIT_AMPERES:
            return "current"
        elif unit == HS_UNIT_KW:
            return "power"
        elif unit == HS_UNIT_KWH:
            return "energy"
        elif unit == HS_UNIT_V or unit == HS_UNIT_VOLTS:
            return "voltage"
        elif unit == HS_UNIT_W or unit == HS_UNIT_WATTS:
            return "power"
        return None


class HomeSeerBatterySensor(HomeSeerValueSensor):
    """Representation of a HomeSeer device that reports battery level."""

    @property
    def device_class(self):
        return "battery"

    @property
    def icon(self):
        if self.state == 100:
            return "mdi:battery"
        elif self.state > 89:
            return "mdi:battery-90"
        elif self.state > 79:
            return "mdi:battery-80"
        elif self.state > 69:
            return "mdi:battery-70"
        elif self.state > 59:
            return "mdi:battery-60"
        elif self.state > 49:
            return "mdi:battery-50"
        elif self.state > 39:
            return "mdi:battery-40"
        elif self.state > 29:
            return "mdi:battery-30"
        elif self.state > 19:
            return "mdi:battery-20"
        elif self.state > 9:
            return "mdi:battery-10"
        return None


class HomeSeerHumiditySensor(HomeSeerValueSensor):
    """Representation of a HomeSeer humidity sensor device."""

    @property
    def device_class(self):
        return "humidity"


class HomeSeerFanStateSensor(HomeSeerStatusSensor):
    """Representation of a HomeSeer HVAC fan state sensor device."""

    @property
    def icon(self):
        if self._device.value == 0:
            return "mdi:fan-off"
        return "mdi:fan"


class HomeSeerOperatingStateSensor(HomeSeerStatusSensor):
    """Representation of a HomeSeer HVAC operating state sensor device."""

    @property
    def icon(self):
        if self.state == "Idle":
            return "mdi:fan-off"
        elif self.state == "Heating":
            return "mdi:flame"
        elif self.state == "Cooling":
            return "mdi:snowflake"
        return "mdi:fan"


class HomeSeerDoorLockLoggingSensor(HomeSeerStatusSensor):
    """Representation of a door-lock-logging sensor."""

    @property
    def icon(self) -> str:
        """Return an appropriate lock icon."""
        return "mdi:lock-clock"


def get_sensor_entity(device, connection):
    """Return the proper sensor object based on device type."""
    if device.device_type_string == DEVICE_ZWAVE_BATTERY:
        return HomeSeerBatterySensor(device, connection)
    elif device.device_type_string == DEVICE_ZWAVE_RELATIVE_HUMIDITY:
        return HomeSeerHumiditySensor(device, connection)
    elif device.device_type_string == DEVICE_ZWAVE_FAN_STATE:
        return HomeSeerFanStateSensor(device, connection)
    elif device.device_type_string == DEVICE_ZWAVE_OPERATING_STATE:
        return HomeSeerOperatingStateSensor(device, connection)
    elif device.device_type_string == DEVICE_ZWAVE_DOOR_LOCK_LOGGING:
        return HomeSeerDoorLockLoggingSensor(device, connection)
    elif device.device_type_string in GENERIC_VALUE_SENSOR_TYPES:
        return HomeSeerValueSensor(device, connection)
    return HomeSeerStatusSensor(device, connection)
