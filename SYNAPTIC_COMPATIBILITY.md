# Reality Bridge Synaptic Core v0.3.0

Synaptic Core v1 adds one deterministic signal-state model that can be expressed consistently across programming languages.

## First-party source now in this repository

- ✅ C++17 — native reference class, standalone CMake package, unit test and golden-vector executable
- ✅ Python 3.10+ — installable `reality-bridge` 0.3.0 API with tests
- ✅ JavaScript — dependency-free browser/Node ES module with golden-vector test
- ✅ TypeScript — first-class type declarations over the tested JavaScript numerical core
- ✅ Go — dependency-free package with golden-vector test
- ✅ C# — managed .NET/Unity source
- ✅ Java 17+ — dependency-free JVM source
- ✅ Swift — dependency-free Apple-platform source
- ✅ C11 — header-only implementation with golden-vector test

The authoritative contract is `spec/synaptic_abi_v1.json`; the algorithm, state fields and golden vector are documented in `docs/SYNAPTIC_CORE.md`. The detailed binding matrix is `bindings/README.md`.

## Rust and Kotlin

The existing Rust DSP/state crate remains part of the project and continues to pass the repository CI, but a first-party Synaptic Core Rust source port is **not** committed in this revision. Kotlin can call the Java implementation directly on the JVM, but a separate native Kotlin source file is also not committed. They are not marked complete in the binding matrix.

## Universal compatibility policy

A language does not become “supported” merely because somebody translated the method names. A compatible port must preserve the v1 defaults, numerical ranges, update order, state semantics and golden conformance vector. This means the machine-readable contract can be implemented in additional languages without changing the definition of Synaptic Core.

## Verification status

The repository's existing CI is green after the v0.3.0 source changes. It executes the full Python test directory, existing Rust tests, existing C++ build/tests, standalone HTML reconstruction and HTML audit. The new Python Synaptic Core tests therefore run in CI. Additional committed conformance sources exist for C++, JavaScript, Go and C; the current GitHub connector did not permit adding a new multi-language Actions workflow in this revision, so those are not described as Actions-verified here.

## Scope

The word “synaptic” is engineering terminology for trace memory, coupling, bounded activation and reward-modulated adaptation in software. This component does not claim to reproduce a biological synapse, nervous system, consciousness, identity or human memory.
