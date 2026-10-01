# Contributing

Code contributions are welcome, and greatly appreciated.
Please follow these guidelines when contributing:

## Reporting a Bug

If you find a bug, please open issue. Use the template provided, and use as much detail as you can.
Issue titles should be clear and concise, and give an overview of the problem.

For example:
- [Suggestion] Add the ability to...
- [Documentation] Elaborate on...
- [Bug] Tracker References: X fails when Y...

Maintainers may edit your title to follow this guideline.

## Project Scope

Tracking Toolkit (TTK) is vendor and runtime agnostic. 
It uses Blender's built-in OpenXR support, and is limited to the compatibility there.
Hardware-specific features are discouraged, with the exception of Vive trackers.

TTK will not support software or protocols other than OpenXR at this time.
This means that pull requests or suggestions for protocols such as OSC, VMC, etc. will be rejected.

If you require these out-of-scope protocols for your project, consider forking TTK and developing them yourself.
Most of the OpenXR-dependent code is in `protocol.py`, and is generally decoupled from the rest of the addon.
It is fairly straightforward to replace it with another protocol, depending on the complexity of the implementation.
We do not provide support for forks that are not intended to be merged into TTK.

## Opening a Pull Request (PR)

When submitting code, please follow these guidelines.

- Fork TTK, and create a branch off `main` for your changes.
- Follow the directions in [DEVELOPMENT.md](DEVELOPMENT.md).
- Use the format `Module: Concise description` as for commit messages. Group relevant changes together, and avoid minor changes to unrelated modules in a single commit.
- Test your changes before pushing. Make sure that TTK can be enabled and disabled, and that it starts up correctly from a fresh Blender instance and file.

In your PR description, you should explain your changes, what they do, and why the problem/feature is implemented.

Reviewers will check your code and may request changes. 
If the feature is out-of-scope, the PR may be rejected.
If in doubt, open an issue first.

Your commits **must be signed** with a [Developer Certificate of Origin](https://developercertificate.org/) (DCO), or the PR will not be accepted.
By opening a PR, you agree to the terms of the DCO.
