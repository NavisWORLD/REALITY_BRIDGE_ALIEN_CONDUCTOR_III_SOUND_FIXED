# Reality Bridge Synaptic Core v0.3.0

Synaptic Core v1 adds one deterministic signal-state model that can be expressed consistently across programming languages.

## First-party source now in this repository

- ✅ C++17 — native reference class, standalone CMake package, unit test and golden-vector executable
- ✅ Python 3.10+ — installable `reality-bridge` 0.3.0 API with tests
- ✅ Rust 2021+ — dependency-free `cosmic-synapse` 0.3.0 crate with tests and golden-vector conformance
- ✅ JavaScript — dependency-free browser/Node ES module with golden-vector test
- ✅ TypeScript — first-class type declarations over the tested JavaScript numerical core
- ✅ Go — dependency-free package with golden-vector test
- ✅ C# — managed .NET/Unity source
- ✅ Java 17+ — dependency-free JVM source
- ✅ Kotlin/JVM — first-party `CosmicSynapse` facade over the canonical Java numerical implementation
- ✅ Swift — dependency-free Apple-platform source
- ✅ C11 — header-only implementation with golden-vector test

The authoritative contract is `spec/synaptic_abi_v1.json`; the algorithm, state fields and golden vector are documented in `docs/SYNAPTIC_CORE.md`. The detailed binding matrix is `bindings/README.md`.

## Rust

The existing `rust/` Cosmic Conductor DSP/state crate remains intact and continues to pass CI. Synaptic Core is published in-repository as a separate safe Cargo package at `bindings/cosmic_synapse/`. It exposes `SynapseConfig`, `SynapseState`, `Synapse`, `pulse`, `step`, `reinforce`, `couple`, `reset`, `snapshot`, `restore`, batch processing and the shared conformance sequence.

The repository CI runs both Rust suites independently:

```bash
cargo test --manifest-path rust/Cargo.toml --all-targets
cargo test --manifest-path bindings/cosmic_synapse/Cargo.toml --all-targets
```

This separation avoids coupling the safe Synaptic Core package to the existing audio crate's FFI surface.

## Kotlin

`bindings/kotlin/CosmicSynapse.kt` is a first-party Kotlin/JVM API. It delegates numerical state transitions to the canonical Java `realitybridge.synaptic.Synapse` class in the same package, so Java and Kotlin share one implementation of the v1 contract rather than duplicating equations that could drift.

## Universal compatibility policy

A language does not become “supported” merely because somebody translated the method names. A compatible port must preserve the v1 defaults, numerical ranges, update order, state semantics and golden conformance vector. This means the machine-readable contract can be implemented in additional languages without changing the definition of Synaptic Core.

## Verification status

The repository CI now tests the full Python suite, the existing Rust engine, the standalone Rust Synaptic Core crate, the existing C++ build/tests, standalone HTML reconstruction and HTML audit. Rust Synaptic Core includes direct golden-vector, configuration-boundary and snapshot/restore tests.

Additional committed conformance sources exist for C++, JavaScript, Go and C. The first-party JVM, .NET and Swift sources remain available for host-specific integration and further platform testing.

## Scope

The word “synaptic” is engineering terminology for trace memory, coupling, bounded activation and reward-modulated adaptation in software. This component does not claim to reproduce a biological synapse, nervous system, consciousness, identity or human memory.
