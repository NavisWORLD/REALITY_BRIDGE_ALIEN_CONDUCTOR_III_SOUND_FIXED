# Cosmic Conductor app paths

1. **PWA:** host the repository through HTTPS and open `index.html`.
2. **Desktop launcher:** `python app/reality_bridge_app.py`.
3. **Native mobile wrapper:** `app/capacitor/` for Android/iOS.

Prepare mobile assets with `python app/prepare_mobile.py`, then use Capacitor plus Android Studio/Xcode. Store signing credentials are intentionally not committed.

A non-WebView native host can embed either `rust/` through the `cc_*` ABI or `cpp/` through the `rb_*` ABI. See `docs/DEVICE_BUILD_GUIDE.md`.
