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


## Session 3 — Core AI toolchain probe (2026-09-20)

### Python: works
- coreai-core  1.0.0b2   (beta - pin exactly in CI)
- coreai-opt   0.2.1
- coreai-torch 0.4.2
- torch        2.11.0
- torchao      0.17.0    (quantization backend behind coreai-opt)
- numpy        2.3.5
- Python 3.12 via actions/setup-python
- All import successfully. Session 1's inference confirmed by execution.

### Warning
coremltools reports torch 2.11.0 untested; 2.7.0 is the most recent
tested version. coreai-opt pulls coremltools. If conversion behaves
strangely in Phase 1, pin torch==2.7.0 first.

### Swift: absent
- SDK is MacOSX26.5.sdk. Contains FoundationModels.framework,
  NOT CoreAI.framework.
- `import CoreAI` fails: no such module.
- `xcrun coreai-build` not found.
- Apple docs: coreai-models CLI requires Xcode 27.0+. Runner has 26.6.
- Blocks Phase 4 (Swift CLI), not Phases 1-3.
- TODO: check `ls /Applications | grep -i xcode` for a newer Xcode;
  try `runs-on: macos-27`.

### Two Python environments in one job
`uv run` inside coreai-models creates its own .venv (picked 3.11.9),
ignoring the job's pinned Python. Registry and export tools run there;
our own conversion code runs in the job environment. Keep them distinct.

### Registry: Apple's existing recipes (exclusion list for Session 11)
LLM: Qwen2.5/3 family, Gemma 3 + 3n, Mistral/Mixtral, GPT-OSS-20B,
Phi-3/3.5/4-mini, SmolLM2 (135M/360M/1.7B), OLMo2-1B, Muse-Glimmer-30B
Diffusion: SD 1.5/2.1/3.5-medium, FLUX.2-klein-4B, Wan2.1-T2V-1.3B
Other: CLIP ViT-B/32, CLAP, Whisper large-v3 + turbo, wav2vec2-base,
YOLOS base/tiny, EfficientSAM, SAM3, SAM3-video, Depth-Anything-3-small,
EDSR-x2, RoBERTa-base, T5 small/base/large, PVT-v2-b0

### Observation for Session 11
No VLM anywhere in the registry - conspicuous gap.
The entire "Image, Text, Audio" table ships UNCOMPRESSED. Compression
analysis on any of those 17 is unexplored even where Apple has a recipe.
Possible reframe: not "a model Apple missed" but "a model Apple ships
with no compression story."

## Session 4 — Compute units (2026-09-23)

### Available
- CPU: yes
- GPU: yes. Metal device "Apple Paravirtual device", unified memory,
  max buffer 3.5 GB, command queue OK. torch mps also available.
  CAVEAT: paravirtual. Absolute numbers will not match bare metal;
  relative comparisons between configs should hold. Disclose in 
methodology.
- ANE: no. No AppleH11ANEInterface, no AppleNeuralEngine, no device-tree
  ANE nodes. NVRAM "ane-type" marked not present.

### Xcode
14 Xcodes on the image, all 26.x. No Xcode 27 anywhere.
The Swift gap from Session 3 is structural, not configuration.
Phase 4 needs a macos-27 runner label or external contributors.

### Core AI Python API — the important finding
Import name is `coreai`, NOT `coreai_core`. Lazy namespace package,
so dir(coreai) is empty; import submodules directly.

Submodules: _compiler, _version, authoring, runtime, utils

coreai.runtime contains:
  _aimodel.py                      load .aimodel files
  _inference_function.py           run inference
  _specialization_options.py       likely compute unit selection
  _coreai_runtime.cpython-312-darwin.so    compiled runtime
  _coreai_runtime_os.cpython-312-darwin.so

=> .aimodel files CAN be loaded and executed from Python on this runner.
   Phases 1-3 need no Swift. Benchmarking plan is viable as designed.

coreai_torch exposes conversion only (TorchConverter, ExternalizeSpec,
MetalParameter, get_decomp_table) - no compute unit selection there.

coreai_opt.ExportBackend has members: CoreAI, CoreML.
=> a CoreML fallback path exists if needed.

coremltools 9.0 available, ComputeUnit enum: CPU_ONLY, CPU_AND_GPU,
CPU_AND_NE, ALL. Fallback for compute-unit-specific benchmarking.

### Next
Session 5-7 are applications and referrals. Before Session 11, read
coreai/runtime/_specialization_options.py to learn how compute units
are selected.
