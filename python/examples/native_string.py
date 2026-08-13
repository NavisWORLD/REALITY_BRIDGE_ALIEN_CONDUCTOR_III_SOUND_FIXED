from reality_bridge.native import NativeString
with NativeString(48_000.0) as voice:
    voice.pluck(220.0)
    samples=[voice.process() for _ in range(256)]
    print(samples[:16])
