# MOES ZHA Extension

MOES ZHA Extension provides additional Home Assistant ZHA support for selected MOES Zigbee devices through custom ZHA quirks.

It is designed to extend device compatibility for MOES Zigbee products that are not yet fully supported by the upstream ZHA device handler library.

## Requirements

- Home Assistant
- Zigbee Home Automation (ZHA)
- A compatible Zigbee coordinator

ZHA must already be installed and configured before using MOES ZHA Extension.

## Installation

### HACS

1. Open HACS.
2. Add this repository as a custom repository:
   `MOESHOUSE/moes-zha-extension`
3. Select `Integration` as the repository category.
4. Install `MOES ZHA Extension`.
5. Restart Home Assistant.
6. Go to:
   `Settings -> Devices & services -> Add integration`
7. Search for `MOES ZHA Extension` and add it.

No manual ZHA `custom_quirks_path` configuration is required.

## Device support

Support for additional MOES Zigbee devices is added continuously.

A separate supported-device list will be maintained as the project expands.

## How it works

MOES ZHA Extension registers MOES-specific ZHA quirks when the integration starts.

After the quirks are registered, the integration reloads ZHA so that existing Zigbee devices can be matched against the MOES quirks.

During this process, ZHA devices may temporarily become unavailable while the Zigbee network is initialized again.

This behavior is expected.

## Updating

When a new version is available through HACS:

1. Update MOES ZHA Extension.
2. Restart Home Assistant.

Updated quirks will be loaded automatically.

## Troubleshooting

If a supported MOES device does not expose the expected entities or controls:

1. Confirm that MOES ZHA Extension is enabled.
2. Confirm that ZHA is running normally.
3. Restart Home Assistant.
4. Allow ZHA enough time to finish initializing all Zigbee devices.

Avoid installing duplicate copies of the same MOES quirk through a separate ZHA `custom_quirks_path`, as this can make troubleshooting more difficult.

## Reporting issues

Please report device compatibility problems and bugs through GitHub Issues:

https://github.com/MOESHOUSE/moes-zha-extension/issues

When reporting a device compatibility issue, please include:

- MOES product model
- Zigbee model
- Zigbee manufacturer identifier
- Home Assistant version
- Relevant ZHA debug logs
- Expected behavior
- Actual behavior

## Disclaimer

MOES ZHA Extension is a custom Home Assistant integration and is not part of the Home Assistant Core project.

Device functionality may vary depending on device firmware, Zigbee coordinator, Home Assistant version, and ZHA version.

## License

Licensed under the Apache License 2.0.
