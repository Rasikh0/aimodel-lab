# Local environment audit

Date: 2026-09-17

## Hardware
- Model: MacBookAir7,2 (13-inch, Early 2015 / 2017)
- CPU: Intel Core i5-5350U @ 1.80GHz (Broadwell, dual-core)
- RAM: 8 GB
- macOS: 12.7.6 Monterey (build 21H1320) — hardware ceiling
- Disk: 113 GB total, 28 GB available

## Toolchain
- git: 2.37.1 (Apple Git-137.1), from Xcode CLT
- uv: 0.12.16 (x86_64-apple-darwin)
- Homebrew: 7.0.1 — Intel now Tier 3, bottles no longer routinely built
- Python: 3.11.16

## PyTorch
- torch 2.2.2 installed and functional.
- This is the last macOS x86_64 release; PyTorch dropped Intel Mac
  wheels at 2.3.0 (April 2024).
- Current torch (2.11.0) ships: manylinux_2_28_aarch64,
  manylinux_2_28_x86_64, macosx_11_0_arm64, win_amd64.
  No macOS x86_64 build exists.

## Core AI toolchain — both blocked, different causes

### coreai-torch
Resolution failure. Its compiled dependency coreai-core (1.0.0b1, 1.0.0b2)
publishes no macosx_12_0_x86_64 wheel.
Available: manylinux1_x86_64, macosx_26_0_arm64.

### coreai-opt
Resolution failure. Pins torch>=2.8.0,<=2.11.0, which has no
macOS x86_64 build at any version in that range.

## Implications
1. Core AI runtime requires arm64 AND macOS 26 -> CI must pin macos-26.
2. Both libraries have Linux x86_64 wheels -> Colab should run the full
   conversion and compression toolchain. Verify in Session 13.
   If confirmed: convert in Colab, benchmark in CI. Iteration loop moves
   from a 3-8 min CI round trip into a notebook cell.
3. coreai-core is beta (1.0.0b2). Pin exact versions in CI; expect at
   least one breaking change over 15 weeks.
4. Local machine is an editor and git client. Nothing else.
