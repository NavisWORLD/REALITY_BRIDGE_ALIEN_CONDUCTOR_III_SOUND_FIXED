# Synaptic Core v1

Synaptic Core is a deterministic software state primitive for signal memory, coupling and reward-modulated adaptation. The biological vocabulary is metaphorical engineering terminology; the project does **not** claim this class reproduces a biological synapse, nervous system, consciousness, personality, or memory of a person.

## Stable contract

The machine-readable contract is `spec/synaptic_abi_v1.json`. Implementations must preserve update order, defaults, clamps and the golden conformance vector.

### Configuration

| Field | Default | Meaning |
|---|---:|---|
| `decay` | 2.0 | potential relaxation rate |
| `trace_decay` | 1.0 | short-state trace relaxation rate |
| `threshold` | 0.15 | activation center |
| `gain` | 1.0 | activation response gain |
| `plasticity` | 0.05 | reward update rate |
| `weight_min` | 0.10 | minimum adaptive weight |
| `weight_max` | 2.00 | maximum adaptive weight |
| `target_activity` | 0.35 | target absolute activation for threshold adaptation |
| `homeostasis` | 0.02 | threshold adaptation rate |

### State

`potential`, `activation`, `trace`, `weight`, `pending_coupling`, `last_input`, `last_output`, `threshold_offset`, `tick`.

## Pulse algorithm

For one call `pulse(input, modulation, dt)`:

1. Clamp invalid or unbounded inputs to the contract ranges.
2. Compute potential decay `exp(-decay * dt)` and trace decay `exp(-trace_decay * dt)`.
3. Compute `drive = input * weight + pending_coupling + modulation * trace`.
4. Integrate potential toward the drive.
5. Compute activation with `tanh(gain * (potential - effective_threshold))`.
6. Integrate the trace toward activation.
7. Adapt `threshold_offset` toward the target absolute activity.
8. Clear pending coupling, store last input/output, increment tick.

`reinforce(reward)` updates weight by `plasticity * reward * trace * last_input`, bounded by `weight_min`/`weight_max`.

`couple(source_output, strength)` stores bounded coupling drive for the **next** pulse.

## Golden conformance vector

Sequence:

```text
inputs      = [0.25, 0.8, -0.2, 0.6, 0.0, -0.4, 0.9]
modulations = [0.0, 0.1, 0.2, -0.1, 0.05, 0.0, 0.15]
dt          = 0.01
before pulse 2: couple(0.35, 0.4)
after pulse 3: reinforce(0.7)
after pulse 5: reinforce(-0.2)
```

Expected final state (binary64 reference):

```text
potential        0.038840176720408945
activation      -0.11044113874970204
trace           -0.008475792084489108
weight           0.9998629394170829
threshold_offset -0.00031425539024381897
last_output     -0.11044113874970204
tick             7
```

Ports should normally agree within `1e-12`; platforms using different libm implementations may use a documented tolerance up to `1e-10`.

## Native implementations

- C++: `cpp/include/reality_bridge/synapse.hpp` + `cpp/src/synapse.cpp`
- Python: `python/reality_bridge/synapse.py`
- C++ standalone build: `cmake -S cpp/synapse -B build/synapse && cmake --build build/synapse && ctest --test-dir build/synapse`
- Python: `python -m pip install -e './python[test]' && pytest python/tests/test_synapse.py`

## Universal-language rule

Languages with a maintained native port should use that port. Other languages may implement the tiny v1 contract directly from the JSON spec and verify against the golden vector. A port is **not** considered compatible until it passes the same vector.
