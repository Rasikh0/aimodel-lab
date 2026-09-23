# aimodel-lab

Reproducible benchmarking harness for deploying a small open-source model
to Apple silicon with Core AI.

Built entirely on a 2015 Intel MacBook Air. All Apple silicon work runs on
free GitHub Actions M1 runners; all PyTorch work runs on Colab.

## What runs where, and why

The development machine (MacBookAir7,2, Intel i5, macOS 12.7.6) cannot run
Apple's Core AI toolchain at all. `coreai-core` publishes wheels only for
`manylinux1_x86_64` and `macosx_26_0_arm64`; there is no macOS x86_64 build.
PyTorch also stopped shipping macOS x86_64 wheels at 2.3.0, capping the
laptop at torch 2.2.2.

| Machine | Role |
|---|---|
| Local (Intel MacBook Air) | Editor, git, docs |
| Colab / Kaggle (Linux x86_64 + GPU) | PyTorch work, export, training |
| GitHub Actions `macos-26` (M1, arm64) | Conversion, validation, benchmarking |

Full audit: [docs/environment.md](docs/environment.md) and
[docs/runner-environment.md](docs/runner-environment.md)

## Benchmarking environment and its limits

Benchmarks run on a GitHub Actions `macos-26` runner: Apple M1 (Virtual),
3 cores, 7 GiB RAM, macOS 26.6.2.

| Compute path | Available | Notes |
|---|---|---|
| CPU | Yes | |
| GPU | Yes | Metal "Apple Paravirtual device", unified memory, 3.5 GB max buffer |
| Neural Engine | **No** | No ANE driver class present in the VM |

**These are virtualized numbers.** The runner is a VM (`VirtualMac2,1`) with
a paravirtual GPU. Absolute latency will not match bare metal, and the
Neural Engine — the compute unit most on-device deployments actually target —
cannot be measured here at all.

The project is designed around this rather than hiding it: the harness is
built so anyone with real Apple silicon can run the identical benchmark and
contribute their numbers. See Phase 4.

## Status

Session 4 of 90. Environment characterised; no model converted yet.

- [x] Local and CI environments audited
- [x] Core AI Python toolchain verified on the runner
- [x] Compute unit availability established
- [ ] Model selected
- [ ] First conversion
- [ ] Measurement harness
- [ ] Compression sweeps

## License

MIT
