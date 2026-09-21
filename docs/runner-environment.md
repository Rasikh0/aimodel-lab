# CI runner environment

Date: 2026-09-20
Label: macos-26
Runner version: 2.337.0

## Hardware
- Architecture: arm64 (hw.optional.arm64 = 1, native not Rosetta)
- Model: Apple Virtual Machine 1 / VirtualMac2,1
- Chip: Apple M1 (Virtual)
- Cores: 3
- RAM: 7,516,192,768 bytes (7.0 GiB)
- Disk free: 96 GB

## Software
- macOS: 26.6.2 (build 25G83)
- Xcode: 26.6 (build 17F113)
- macOS SDK: 26.5
- Swift: 6.3.3, target arm64-apple-macosx26.0
- Python (default): 3.14.7, pip 26.2.1 (Homebrew)

## Findings
1. macOS 26 + arm64 satisfies coreai-core's macosx_26_0_arm64 wheel.
   Both Session 1 blockers are cleared on this runner.
2. Runner is a VM. No Neural Engine expected. Confirm in Session 4.
   All latency figures carry a virtualization caveat.
3. Default Python 3.14.7 is too new for torch, which has no 3.14 wheels.
   Pin with actions/setup-python (3.12) in every workflow.
4. Disk is 96 GB, not the ~14 GB assumed in the plan. RAM (7 GiB) is the
   only real constraint on model size.
5. Xcode is 26.6, not 27. Pairs with macOS 26. Whether Core AI needs 27
   is unresolved; test in Session 3.
