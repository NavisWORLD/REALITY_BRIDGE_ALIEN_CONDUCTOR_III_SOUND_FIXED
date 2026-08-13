# Reality Bridge // Cosmic Conductor Engine — C++

Build:
```bash
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp --config Release
ctest --test-dir build/cpp -C Release --output-on-failure
```

The C++ layer is the original host-neutral native DSP implementation. It exports the stable `rb_*` C ABI from `include/reality_bridge/c_api.h`, making it callable from Python ctypes, Rust FFI, Swift/Objective-C, JNI glue, C#, Unity, Unreal and other hosts.
