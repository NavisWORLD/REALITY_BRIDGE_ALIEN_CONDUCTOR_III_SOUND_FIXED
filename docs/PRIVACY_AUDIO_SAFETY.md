# Privacy + Audio Safety

## Local-first baseline
The shipped browser instrument does not require a cloud backend. User-selected media is processed by browser code. Microphone access is requested only for features that need it. Forks adding telemetry, remote inference, uploads or analytics should disclose it clearly and obtain required consent.

## Microphone rule
Analysis and monitoring are separate concepts. Enabling analysis MUST NOT automatically send raw microphone audio to speakers.

## Output rule
- conservative startup gain
- smooth envelopes around starts/stops
- limiter/compressor or bounded nonlinear stage where appropriate
- hard limits on delay feedback and voice counts
- panic/all-notes-off
- finite numeric validation and safe frequency ranges

Users should begin at a low device volume, especially with headphones.

## File handling
Long media should be decoded/analyzed incrementally or at reduced resolution. Do not copy huge user files into persistent settings. Release object URLs and temporary buffers when replaced.

## Accessibility
Do not hide essential actions behind gestures alone. Provide visible play/stop/panic and meaningful assistive labels where practical.
