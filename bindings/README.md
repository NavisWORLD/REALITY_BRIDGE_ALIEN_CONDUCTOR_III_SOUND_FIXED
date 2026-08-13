# Synaptic Core language compatibility

The shared numerical contract is `../spec/synaptic_abi_v1.json`. See `../docs/SYNAPTIC_CORE.md` for the algorithm and golden conformance vector.

## Implemented first-party ports

| Language | Status | Path |
|---|---|---|
| C++17 | ✅ | `../cpp/include/reality_bridge/synapse.hpp` |
| Python 3.10+ | ✅ CI tested | `../python/reality_bridge/synapse.py` |
| Rust 2021+ | ✅ CI tested | `cosmic_synapse/` |
| JavaScript | ✅ | `javascript/synapse.mjs` |
| TypeScript | ✅ typings over JS core | `typescript/synapse.d.ts` |
| Go | ✅ | `go/synapse.go` |
| C# / .NET / Unity | ✅ | `csharp/Synapse.cs` |
| Java 17+ | ✅ | `java/Synapse.java` |
| Kotlin/JVM | ✅ Java-backed first-party facade | `kotlin/CosmicSynapse.kt` |
| Swift | ✅ | `swift/Synapse.swift` |
| C11 | ✅ | `c/synapse.h` |

The standalone Rust crate is `cosmic-synapse` v0.3.0 and is dependency-free. Repository CI runs both the existing `rust/` engine test suite and `cargo test --manifest-path bindings/cosmic_synapse/Cargo.toml --all-targets`.

Kotlin intentionally delegates its numerical operations to the canonical Java implementation in the same JVM package. This keeps Java and Kotlin behavior identical instead of maintaining two drifting copies of the same equations.

JavaScript, Go and C include committed golden-vector tests. C++ includes its own standalone CMake test/conformance target. Python and Rust Synaptic Core tests run in the repository's normal CI suite.

## Additional contract targets

Zig, Lua, Ruby, PHP, Julia, Dart/Flutter, Fortran, Nim and Free Pascal remain valid Synaptic Core Contract v1 targets, but are not marked as maintained first-party source ports in this revision.

A language is not marked implemented merely because the contract can be ported to it.

## Common API

First-party ports expose the local-language equivalent of `SynapseConfig`, `SynapseState`, `pulse`/`step`, `reinforce`, `couple`, `reset`, snapshot/state, restore, and batch processing where idiomatic.

“Synaptic” is engineering terminology for a deterministic software state model. It does not claim biological synapse, nervous-system, consciousness, identity or human-memory equivalence.
