# App packaging

The repo ships three practical app paths.

1. **PWA / any modern browser** — deploy the repository root over HTTPS and choose *Add to Home Screen / Install App*.
2. **Desktop** — run `python app/reality_bridge_app.py`. It serves the instrument on localhost so browser audio/microphone permissions behave predictably.
3. **Android/iOS wrapper** — run `python app/prepare_mobile.py`, then from `app/capacitor` run `npm install`, `npx cap add android` or `npx cap add ios`, and `npx cap sync`. Open the native project with Android Studio/Xcode and sign it with your own credentials.

The repository does **not** include platform signing certificates or claim that unsigned source is a store-ready binary. iOS builds require macOS/Xcode; Android builds require the Android SDK.
