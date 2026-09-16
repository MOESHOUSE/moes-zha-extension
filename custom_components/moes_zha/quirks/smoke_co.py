"""MOES TS0601 Smoke + CO sensor quirk."""

import zigpy.types as t
from zigpy.zcl import foundation

from zhaquirks.builder import (
    BinarySensorDeviceClass,
    EntityPlatform,
    EntityType,
)
from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zhaquirks.tuya.mcu import TuyaMCUCluster


class SmokeState(t.enum8):
    """Smoke state."""

    Alarm = 0
    Normal = 1
    Detecting = 2
    Unknown = 3


class COState(t.enum8):
    """CO state."""

    Alarm = 0
    Normal = 1
    Unknown = 255


class CheckingResult(t.enum8):
    """Self test result."""

    Checking = 0
    Check_success = 1
    Check_failure = 2
    Others = 3


class BatteryState(t.enum8):
    """Battery state."""

    Low = 0
    High = 1
    Unknown = 255


def alarm_state(value):
    """Convert Tuya alarm state to binary sensor state."""

    return {0: True, 1: False}.get(int(value))


class MoesSmokeCOCluster(TuyaMCUCluster):
    """MOES Smoke + CO Tuya MCU cluster."""

    def get(self, key, default=None):
        """Return cached attribute value."""

        value = super().get(key, default)

        if value is not None:
            return value

        defaults = {
            "smoke_state": 3,
            "co_state": 255,
            "battery_state": 255,
        }

        if isinstance(key, int) and key in self.attributes:
            key = self.attributes[key].name

        return defaults.get(key, value)


builder = TuyaQuirkBuilder(
    "_TZE284_aoah6bv8",
    "TS0601",
)


for dp, name, enum, label, category in (
    (1, "smoke_state", SmokeState, "Smoke state", EntityType.STANDARD),
    (
        9,
        "checking_result",
        CheckingResult,
        "Self test result",
        EntityType.DIAGNOSTIC,
    ),
    (
        14,
        "battery_state",
        BatteryState,
        "Battery state",
        EntityType.DIAGNOSTIC,
    ),
    (18, "co_state", COState, "CO state", EntityType.STANDARD),
):
    builder.tuya_enum(
        dp_id=dp,
        attribute_name=name,
        enum_class=enum,
        access=(
            foundation.ZCLAttributeAccess.Read
            | foundation.ZCLAttributeAccess.Report
        ),
        entity_platform=EntityPlatform.SENSOR,
        entity_type=category,
        translation_key=name,
        fallback_name=label,
    )


for name, device_class, label, category in (
    (
        "smoke_state",
        BinarySensorDeviceClass.SMOKE,
        "Smoke alarm",
        EntityType.STANDARD,
    ),
    (
        "co_state",
        BinarySensorDeviceClass.CO,
        "CO alarm",
        EntityType.STANDARD,
    ),
    (
        "battery_state",
        BinarySensorDeviceClass.BATTERY,
        "Battery low",
        EntityType.DIAGNOSTIC,
    ),
):
    builder.binary_sensor(
        attribute_name=name,
        cluster_id=0xEF00,
        attribute_converter=alarm_state,
        device_class=device_class,
        entity_type=category,
        unique_id_suffix=name + "_alarm",
        translation_key=name + "_alarm",
        fallback_name=label,
    )


builder.tuya_sensor(
    dp_id=11,
    attribute_name="fault_bitmap",
    type=t.bitmap32,
    entity_type=EntityType.DIAGNOSTIC,
    translation_key="fault_bitmap",
    fallback_name="Fault bitmap",
)


builder.tuya_switch(
    dp_id=16,
    attribute_name="muffling",
    translation_key="muffling",
    fallback_name="Silence alarm",
)


QUIRK = (
    builder
    .skip_configuration()
    .add_to_registry(
        replacement_cluster=MoesSmokeCOCluster
    )
)
