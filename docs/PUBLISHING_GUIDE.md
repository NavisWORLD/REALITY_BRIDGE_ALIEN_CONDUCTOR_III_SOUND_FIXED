# Publishing + Citation Guide

## 1. Tag a release
Use release tags such as `v0.1.0`. Record included HTML/native/Python versions and tested platforms.

## 2. Archive with Zenodo if desired
Connect the GitHub repository to Zenodo, enable archiving, then create a GitHub release. Zenodo can mint a DOI for that archived release and a concept DOI for the project.

**Do not invent a DOI before the archive exists.**

After issuance, update `CITATION.cff` with the exact DOI and release metadata.

## 3. Release notes separate
- implemented behavior
- experimental/artistic mappings
- known browser/platform constraints
- externally required SDKs/signing steps
- validation performed

## 4. Reproducibility package
Include the release source archive, engineering spec, testing document, test command output, native demo audio, and any publication screenshots/video with source/permission documented.

## 5. Citation
Use `CITATION.cff` and only add a DOI after one is actually minted. Cite the exact version used because algorithms and mappings can change.
