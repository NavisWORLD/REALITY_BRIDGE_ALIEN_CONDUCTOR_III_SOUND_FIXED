from pathlib import Path
from reality_bridge.native import candidate_library_names,candidate_library_paths

def test_candidate_library_names_are_platform_specific():
    names=candidate_library_names(); assert names; assert all(name.startswith(("reality_bridge","libreality_bridge")) for name in names)

def test_candidate_paths_include_repo_build(tmp_path:Path):
    paths=candidate_library_paths(tmp_path); assert any("build" in str(path) and "cpp" in str(path) for path in paths)
