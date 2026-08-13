# Synaptic Core language bindings

All ports in this directory implement **Synaptic Core Contract v1** from `../spec/synaptic_abi_v1.json` and use IEEE-754 binary64 arithmetic where the language exposes it.

A language port is considered conformant only when its golden vector matches `../docs/SYNAPTIC_CORE.md` within the documented tolerance.

| Language/runtime | Path | Integration style |
|---|---|---|
| C++17 | `../cpp/include/reality_bridge/synapse.hpp` | native reference implementation |
| Python 3.10+ | `../python/reality_bridge/synapse.py` | native reference implementation / pip package |
| JavaScript / Node / browser | `javascript/synapse.mjs` | dependency-free ES module |
| TypeScript | `typescript/synapse.ts` | typed dependency-free port |
| Go | `go/synapse.go` | dependency-free package |
| C# / .NET / Unity | `csharp/Synapse.cs` | dependency-free managed class |
| Java 17+ | `java/Synapse.java` | dependency-free class |
| Kotlin/JVM | `kotlin/Synapse.kt` | dependency-free class |
| Swift | `swift/Synapse.swift` | dependency-free value/reference types |
| C11 | `c/synapse.h` | header-only implementation |
| Zig | `zig/synapse.zig` | native struct |
| Lua 5.3+ | `lua/synapse.lua` | pure Lua module |
| Ruby 3+ | `ruby/synapse.rb` | pure Ruby class |
| PHP 8+ | `php/Synapse.php` | pure PHP class |
| Julia 1.9+ | `julia/Synapse.jl` | pure Julia module |
| Dart 3+ | `dart/lib/synapse.dart` | pure Dart class |
| Fortran 2008 | `fortran/synapse.f90` | module/type implementation |
| Nim 2+ | `nim/synapse.nim` | native object implementation |
| Free Pascal | `pascal/synapse.pas` | unit/class implementation |

## Why ports instead of one unsafe FFI boundary?

The audio/DSP engine still exposes its existing stable C ABI. Synaptic Core v1 is intentionally tiny enough to port directly. Direct ports avoid allocator ownership and raw-pointer lifetime mismatches across managed runtimes, mobile sandboxes and WebAssembly. The conformance vector prevents silent semantic drift.

## Required API shape

Each maintained port exposes the local-language equivalent of:

```text
SynapseConfig defaults
SynapseState
Synapse(config?)
pulse(input, modulation=0, dt=0.01) -> number
step(...) -> number
reinforce(reward)
couple(sourceOutput, strength)
reset()
state/snapshot
restore(state)
```

If a language cannot represent a feature idiomatically, document the deviation in that binding's README and preserve the numerical contract.
