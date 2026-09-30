1. nn.Module
   A Python object. Lives in memory. Contains weights as tensors and a
   forward() method that is arbitrary Python — loops, conditionals, whatever.
   Cannot be shipped anywhere, because running it requires Python and PyTorch.

2. torch.export(model, args)  →  ExportedProgram
   Traces forward() and captures it as a static computation graph. Control
   flow is resolved or rejected. Now it's data describing operations, not
   code that executes them. This is where SmolVLM will fight you.

3. coreai_torch.TorchConverter  →  MLIR (coreai dialect)
   Translates PyTorch operations into Apple's intermediate representation.
   From Session 4 you know this is MLIR-based: coreai/_compiler/_mlir_libs/
   with dialects for coreai, param, debuginfo.

4. coreai-opt  →  MLIR, transformed
   Optional. Applies quantization or palettization by rewriting the graph and
   weights. Same format in, same format out — just smaller and lossier.

5. serialization  →  .aimodel
   A file on disk. Graph plus weights plus metadata. This is the shippable
   artifact — the thing you'd bundle with an app, or in your case, the thing
   you benchmark.

6. first load  →  specialized form
   Core AI compiles the .aimodel for the specific chip it's running on.
   Slow the first time, cached afterward. This is why cold-start and
   steady-state latency are different numbers.

7. coreai.runtime  →  inference
   Loads the specialized form, feeds it inputs, returns outputs.
   _aimodel.py, _inference_function.py, and the compiled .so you found.