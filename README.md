![images/cover.png](images/cover.png)

Tracking Toolkit allows you to view and record [OpenXR](https://www.khronos.org/openxr/) devices inside Blender
with NLA integration and [SMPTE timecode](https://en.wikipedia.org/wiki/SMPTE_timecode).

It allows camera/object tracking with high degrees of clarity,
and can also track the movement of actors for motion capture.

You can view the [demonstration video](https://youtu.be/W6DTAmQiJ4Q) on YouTube. 
There is also a [tutorial](https://youtu.be/watch?v=wcLYXi85080) available.

⚠️ If you are viewing this README from the `main` branch, it may contain details applicable to an unreleased version.

## Requirements

Tracking Toolkit works with Blender 5.2 or later. Vive tracker support requires at least Blender 5.3.

Additionally, you will need an OpenXR runtime and a device to go with it.

| Runtime   | Example Devices           |
|-----------|---------------------------|
| SteamVR   | Valve Index, HTC VIVE     |
| Meta Link | Meta Quest 3, Oculus Rift |
| VDXR      | Meta Quest 3, Vive Focus  |
| Monado    | Open Source/Community     |

Because Tracking Toolkit uses Blender's native XR features, additional OpenXR device and feature support must be added to Blender's core source code.

## Installation

1) Download `tracking_toolkit-latest.zip` from the [latest release](https://github.com/ethanporcaro/tracking-toolkit/releases/latest)
2) Open Blender, use `Edit > Preferences > Get Extensions > (Arrow in top right corner) > Install from disk`, and select the downloaded zip.

## Usage

1) Navigate to the new "Track TK" tab on the sidebar.


2) Press the `Start/Connect OpenXR` button to establish a connection to your runtime. 
If your runtime is not open, it will be launched. 
The list below will populate with names of detected controllers/trackers.


3) Press `Create References` to add the detected trackers to your scene. 
This will create bones, but you can toggle the checkbox to create empties instead.


4) At this point, a large `Start Recording` button will be visible. 
When pressed, it will record the tracker's positions until you press stop.
Existing recordings will be pushed down onto a new NLA strip and muted.
You can also set an optional delay timer.

<p>
<img src="images/panel-quickstart.png" height="400px"/>
<img src="images/panel-record.png" height="400px"/>
</p>

## Additional Information

<details>

<summary>Tracker List</summary>

### Tracker List

When new trackers are detected, they will appear on the list.
You can press `Create References` again to add them to the scene.

Even if controllers are disconnected, they will still remain on the list.

You can click the eyeball icon to show and hide the trackers in the viewport.

⚠️ If you are using Vive Trackers, you will need to use SteamVR as your OpenXR runtime. 
You will also need to assign a role to each tracker (waist, foot, etc.) in the SteamVR tracker settings,
or the trackers will not appear on the list.

You can double click a tracker's name on the list to give it a nickname.
A nickname must be unique, and cannot be set to the original name of another tracker.
You should not directly rename empties or bones in the outliner, as it can break references and recording.

You may also set nicknames in the addon preferences that apply to all future files.

</details>

<details>

<summary>References</summary>

### References

References represent your tracker in the scene.

These will either be bones in an armature, or empties. 
You can toggle `Use Bones For Trackers` checkbox at any time to change this.
All your existing takes/actions will be converted.

Each tracker will have two references:

* The tracking point will follow the tracker's exact location in 3D space. 
It will have the keyframe data when recording.
Generally, it should be left untouched, as data will be overwritten when recording.

* The offset point is a child of the tracking point. 
It receives no data, and should be used for tweaking/aligning the tracker.
Objects or cameras in your scene should be constrained to this offset, rather than the tracking point.

</details>

<details>

<summary>Recording</summary>

### Recording

By default, trackers will be recorded at your scene's FPS.
You can override this in the addon preferences.
You can also set intervals (eg. record on 2s), which will calculate tracking FPS based on scene FPS and interval.

The FPS of takes cannot be increased after recording, but you can decrease them manually or using Blender's [action baking](https://docs.blender.org/manual/en/latest/editors/nla/editing/strip.html?utm_source=blender-5.2.3-lts#bpy-ops-nla-bake) feature.

High FPS values may cause performance issues, and precision may stop increasing at a certain point.

There is a dropdown below the record button that allows you to set a delay before data is captured.

Each time you record a new take, old ones are pushed down onto new [NLA strips](https://docs.blender.org/manual/en/latest/editors/nla/introduction.html) and muted.
The action's name will be a [SMPTE timecode](https://en.wikipedia.org/wiki/SMPTE_timecode]) 
(prefixed with the tracker's name if using empties).

### Controller Input Recording

Controller inputs, such as thumbsticks and buttons, will be recorded as custom properties.
If using bone references, they will be stored as bone properties. 
If using empties, they will be stored as object properties.

These custom properties are keyframed and can be viewed in the [Graph Editor](https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html).
They can also be referenced inside drivers.

Vive Tracker inputs through pogo pins are not currently recorded.

</details>

<details>

<summary>Input Mapping</summary>

### Input Mapping

Controller buttons can be used to trigger TTK functions. These bindings can be configured in the addon preferences.

The following actions can be bound:

#### Start/Stop Capture
Behaves identically to the `Start Recording`/`Stop Recording` button.

#### Capture Single Frame
"Stamps" the live tracker pose onto the scene's current frame. See [#45](https://github.com/varrett-llc/tracking-toolkit/issues/45).

#### Frame Backward
Decrements the scene's frame by 1.

#### Frame Forward
Increments the scene's frame by 1.

#### Start/Stop Playback
Toggles playback of the scene's animation.

The `Restart playback from beginning` option will restart playback from frame 0. 
Otherwise, the playback will continue from the current frame.

</details>

## Troubleshooting

Here are the solutions for common problems. 
Feel free to [open an issue](https://github.com/varrett-llc/tracking-toolkit/issues/new?template=bug-report.md) if you have additional questions or problems.
Please use the provided issue template.

* If controllers or trackers fail to appear on the list, ensure in-headset system menus are closed (eg. the SteamVR dashboard overlay).
If you are using Vive Trackers without a HMD, you can close this menu by clicking the `☰` button on the SteamVR status panel, then click `Toggle Dashboard`. 
If trackers still do not appear, ensure that you assigned them roles.
* Stopping and restarting OpenXR with the button at the top of the Tracking Toolkit panel may often resolve issues.
* A complete restart of Blender and/or your runtime may also fix many common problems.
* Manual changes to the reference objects, bones, and names can break tracking. 
Delete the `XR Trackers` armature (if using bones) or the `XR Root` object and all children (if using empties). Then recreate references.

<details>

<summary>Frequently Asked Questions</summary>

### FAQ

**Q:** How many trackers do I need?

**A:** You only need 1 to get started, but you'll need more for things like full-body motion capture.

**Q:** Can I view my scene in VR?

**A:** Yes! Do note that complex scenes or render modes may cause performance issues.

**Q:** Can I only use Vive Trackers without a headset?

**A:** Yes! Make sure to disable `Pause VR when headset is idle` in the SteamVR video settings. 
If you have no headset attached at all, you may need to enable the Mock HMD driver.
If your trackers do not appear in the list, make sure the in-headset dashboard/menu is closed.

**Q:** Will my scene animations play during recording?

**A:** No. That may change in the future if needed.

</details>

# Credits

Lead Developer & Maintainer [Ethan Porcaro](https://www.linkedin.com/in/ethan-porcaro/).

Technical Art & Project Management [John Kraus](https://jrk.art).

# Contributions

Tracking Toolkit will always remain free, and contributions are welcome. You can donate on [Ko-fi](https://ko-fi.com/varrett) and [Patreon](https://www.patreon.com/c/Varrett).

If you want to assist with development, see [DEVELOPMENT.md](DEVELOPMENT.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

# License

This extension is licensed under [GPL 3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html).

Files under `/images` and `/assets` are in the [Public Domain (CC0)](https://spdx.org/licenses/CC0-1.0.html).

Branding files are public domain, but trademark rights are reserved.

```text
Copyright (C) 2026 Ethan Porcaro

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
```

# Projects using Tracking Toolkit

* ["Liam Right"](https://www.youtube.com/watch?v=5hOd7XADGaM&list=PLrBKkYQIF33SXziwFjMSMQx_r_6CZ_spu) by Ethan Porcaro
* Yours? (Let us know!)