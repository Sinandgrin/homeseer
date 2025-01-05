**PLEASE NOTE: THIS IS A MAINTAINED FORK OF THE ORIGINAL REPOSITORY. IT IS PROVIDED "AS-IS" WITHOUT ANY WARRANTIES OR GUARANTEES OF SUPPORT.**

# HomeSeer Integration for Home Assistant (Maintained Fork)

**IMPORTANT:** This is a **maintained fork** of the original HomeSeer integration for Home Assistant.  
The original repository has been archived and is no longer actively maintained.  
This version includes updates to ensure compatibility with Home Assistant versions beyond 2025.1.  
Please note that this project comes **as-is** with **no guarantees** or **official support**.

This fork is heavily based on the excellent work done by the original authors and contributors of the [archived repository](https://github.com/marthoc/homeseer). Their efforts laid the foundation for this project, and I am grateful for their contributions.  

I created this fork to maintain the integration for my own personal Home Assistant setup but am happy to share my work with the community. If others want to help support and enhance this fork, contributions are very welcome! However, please note that I cannot guarantee personal support or ongoing maintenance in the long term. At some point, I plan to transition away from using HomeSeer entirely, which will likely mark the end of my updates to this integration.

[Home Assistant](https://home-assistant.io/) custom integration supporting [HomeSeer](www.homeseer.com) Smart Home Software (HS3 and HS4).

This integration will create Home Assistant entities for the following types of devices in HomeSeer by default:

- "Switchable" devices (i.e. devices with On/Off controls) as a Home Assistant switch entity
- "Dimmable" devices (i.e. devices with On/Off and Dim controls) as a Home Assistant light entity
- "Lockable" devices (i.e. devices with Lock/Unlock controls) as a Home Assistant lock entity
- "Status" devices (i.e. devices with no controls) as a Home Assistant sensor entity

The type of entity created can also depend on whether a "quirk" has been added for the device (see below) and options chosen by the user during configuration. This custom integration currently supports creating entities for the following Home Assistant platforms: binary sensor, cover, light, lock, scene, sensor, switch. Fan and Media Player entities may be added in future updates.

## Disclaimer

This repository is a community-maintained fork of the original [HomeSeer integration](https://github.com/marthoc/homeseer).  
- There is **no official affiliation** with HomeSeer or its developers.  
- This software is provided **as-is**, without any warranties or guarantees of functionality.  
- Support is not guaranteed, but issues and pull requests are welcome.

Use this integration at your own risk.

## Key Differences from the Original Repository

- Updated to fix breaking changes introduced in Home Assistant 2025.1.
- Includes compatibility updates for future Home Assistant releases.


### Pre-Installation
This integration communicates with HomeSeer via both JSON and ASCII. You must enable control using JSON and ASCII commands in Tools/Setup/Network in the HomeSeer web interface. 

## Installation
This custom integration must be installed for it to be loaded by Home Assistant.


### Manual

1. Create a `custom_components` director in your Home Assistant configuration directory.
2. Download the latest release from the GitHub "Releases" page.
3. Copy the custom_components/homeseer directory from the archive into the custom_components directory in your Home Assistant configuration directory.
4. Restart Home Assistant and proceed with Configuration (see below).

## Configuration

To enable the integration, add it from the Configuration - Integrations menu in Home Assistant: click `+`, then click "HomeSeer".

The following options must be configured at the first stage of the configuration:

|Parameter|Description|Default|
|---------|-----------|-------|
|Host|The IP address of the HomeSeer instance.|N/A|
|Username|The username used to log into HomeSeer.|"default"|
|Password|The password used to log into HomeSeer.|"default"|
|HTTP Port|The HTTP port of the HomeSeer instance.|80|
|ASCII Port|The ASCII port of the HomeSeer instance.|11000|

After clicking submit, the following additional options will be presented to the user:

|Parameter|Description|Default|
|---------|-----------|-------|
|Namespace|A unique string identifying this HomeSeer instance. You may input any string. (This will be used in a future release to allow connections to multiple HomeSeer instances.)|"homeseer"|
|Entity Name Template|A template (Jinja2 format) describing how Home Assistant entities will be named. Default format is "location2 location name".|"{{ device.location2 }} {{ device.location }} {{ device.name }}"|
|Create Scenes from HomeSeer Events?|If this box is ticked, a Home Assistant Scene will be created for each Event in HomeSeer. Events can be filtered by group during a later stage of the configuration.|True|

After clicking submit, the user will be presented with successive dialogs to select: 
- Technology interfaces present in HomeSeer to allow in Home Assistant. The type "HomeSeer" represents devices native to HomeSeer such as virtual devices. (Note: Z-Wave is best-supported, but most devices from other interfaces should 'just work'.) Deselecting an interface name here means that devices from that interface will NOT create Entities in Home Assistant.
- If the user has ticked "Create scenes from HomeSeer Events?", the user will be able to select Event Groups in HomeSeer to allow in Home Assistant. Selecting any groups here will allow ONLY those groups; selecting no groups here will allow ALL event groups. The selected groups (or all groups) will create a Home Assistant Scene for each Event in that group.
- Switches and Dimmers from HomeSeer to be represented as Covers (i.e. blinds or garage doors) in Home Assistant. Device refs selected here will not create a Switch or Light entity in Home Assistant but instead a garage door or blind.

## Quirks

Certain devices in HomeSeer should be represented as an entity other than their HomeSeer features would suggest. Quirks exist in this integration to allow "forcing" a certain type of device to be a certain Home Assistant entity. Currently, there are quirks for the following types of devices:
- Z-Wave Barrier Operator as "cover" (i.e. a garage door)
- Z-Wave Central Scene as Home Assistant events (see below)
- Z-Wave Sensor Binary as "binary sensor"

Further quirks can be requested by opening an issue in this repository with information about the device (and ideally, debug logs from libhomeseer or the integration itself which will contain the information necessary to create the quirk).

## Home Assistant events

Certain HomeSeer devices should be represented as a Home Assistant event - no entity will be created for these devices. Instead, when one of these devices are updated in HomeSeer, this integration will fire an event on the Home Assistant event bus which can be used to trigger a Home Assistant Automation.

The event will contain the following parameters:

`event_type`: homeseer_event  
`event_data`:
- `id`: Device Ref of the Central Scene device in HomeSeer.
- `event`: Numeric value of the device in HomeSeer for a given event.

Currently, the following types of HomeSeer devices will fire events in Home Assistant:
- Z-Wave Central Scene

Support for other "stateless" devices (i.e. remotes) such as these can be added in future updates. Please request support by opening an issue in this repository.

## Services

The integration exposes the following services:
- homeseer.control_device_by_value

### homeseer.control_device_by_value

Allows the user to set any value on a HomeSeer device.  

|Parameter|Description|Format|Required?|
|---------|-----------|------|---------|
|ref|Ref corresponding to the HomeSeer device |Integer|True|
|value|Value to set the device to (integer) |Integer|True|

## Caveats

The HomeSeer JSON API exposes only limited information about the devices present in HomeSeer. Requests for certain features may be declined due to the required data not being present in the API response.


## Contributions and Feedback

Contributions are welcome!
