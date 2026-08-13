# Contributing

Contributions are welcome when they preserve the project's central rule: **do not make the interface claim more than the implementation measures or computes.**

## Before submitting

1. Keep audio output bounded and conservative.
2. Label inference as inference; expose confidence where meaningful.
3. Keep artistic macro names separate from scientific claims.
4. Do not add automatic network upload of user microphone/media data.
5. Do not vendor proprietary SDKs or signing credentials.
6. Add or update tests for DSP, state logic and integration behavior.

Run:

```bash
cd python && python -m pip install -e '.[test]' && pytest -q
cd ..
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure
python tools/reconstruct_standalone.py
node tools/audit_html.mjs
```

By intentionally submitting a contribution, you agree it may be licensed under Apache-2.0 as described by the repository license.
