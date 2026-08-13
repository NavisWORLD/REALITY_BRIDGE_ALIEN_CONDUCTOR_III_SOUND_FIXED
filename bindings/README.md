# Synaptic Core language compatibility

The shared numerical contract is `../spec/synaptic_abi_v1.json`. See `../docs/SYNAPTIC_CORE.md` for the algorithm and golden conformance vector.

## Implemented first-party ports

| Language | Status | Path |
|---|---|---|
| C++17 | ✅ | `../cpp/include/reality_bridge/synapse.hpp` |
| Python 3.10+ | ✅ CI tested | `../python/reality_bridge/synapse.py` |
| JavaScript | ✅ | `javascript/synapse.mjs` |
| TypeScript | ✅ typings over JS core | `typescript/synapse.d.ts` |
| Go | ✅ | `go/synapse.go` |
| C# / .NET / Unity | ✅ | `csharp/Synapse.cs` |
| Java 17+ | ✅ | `java/Synapse.java` |
| Swift | ✅ | `swift/Synapse.swift` |
| C11 | ✅ | `c/synapse.h` |

JavaScript, Go and C include committed golden-vector tests. C++ includes its own standalone CMake test/conformance target. Python tests are included in the repository's normal CI suite.

## Compatibility targets not yet committed as native ports

Rust remains supported by the existing `../rust/` DSP/state crate, but the Synaptic Core Rust port is not committed. Kotlin can directly call the Java implementation on the JVM, but a native Kotlin source port is not committed. Zig, Lua, Ruby, PHP, Julia, Dart/Flutter, Fortran, Nim and Free Pascal are contract targets rather than first-party ports in this revision.

A language is not marked implemented merely because the contract can be ported to it.

## Common API

First-party ports expose the local-language equivalent of `SynapseConfig`, `SynapseState`, `pulse`/`step`, `reinforce`, `couple`, `reset`, snapshot/state, restore, and batch processing where idiomatic.

“Synaptic” is engineering terminology for a deterministic software state model. It does not claim biological synapse, nervous-system, consciousness, identity or human-memory equivalence.
