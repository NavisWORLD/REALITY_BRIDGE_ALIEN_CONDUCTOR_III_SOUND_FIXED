"""Cross-platform ctypes adapter for the Reality Bridge native C++ core."""
from __future__ import annotations
import ctypes, os, platform
from pathlib import Path
from typing import Iterable

def candidate_library_names()->tuple[str,...]:
    system=platform.system()
    if system=="Windows": return ("reality_bridge.dll","libreality_bridge.dll")
    if system=="Darwin": return ("libreality_bridge.dylib","reality_bridge.dylib")
    return ("libreality_bridge.so","reality_bridge.so")

def candidate_library_paths(repo_root:Path|None=None)->list[Path]:
    paths=[]
    explicit=os.environ.get("COSMIC_CONDUCTOR_NATIVE_LIB")
    if explicit: paths.append(Path(explicit).expanduser())
    root=repo_root or Path(__file__).resolve().parents[2]
    for directory in (root/"build"/"cpp",root/"build"/"cpp"/"Release",root/"cpp"/"build",root/"cpp"/"build"/"Release"):
        for name in candidate_library_names(): paths.append(directory/name)
    return paths

def _configure(lib:ctypes.CDLL)->ctypes.CDLL:
    lib.rb_string_create.argtypes=[ctypes.c_double]; lib.rb_string_create.restype=ctypes.c_void_p
    lib.rb_string_destroy.argtypes=[ctypes.c_void_p]; lib.rb_string_destroy.restype=None
    lib.rb_string_pluck.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]; lib.rb_string_pluck.restype=None
    lib.rb_string_process.argtypes=[ctypes.c_void_p]; lib.rb_string_process.restype=ctypes.c_float
    lib.rb_string_stop.argtypes=[ctypes.c_void_p]; lib.rb_string_stop.restype=None
    lib.rb_midi_to_hz.argtypes=[ctypes.c_double,ctypes.c_double]; lib.rb_midi_to_hz.restype=ctypes.c_double
    lib.rb_hz_to_midi.argtypes=[ctypes.c_double,ctypes.c_double]; lib.rb_hz_to_midi.restype=ctypes.c_double
    lib.rb_soft_limit.argtypes=[ctypes.c_float,ctypes.c_float]; lib.rb_soft_limit.restype=ctypes.c_float
    return lib

def load_native(paths:Iterable[Path]|None=None)->ctypes.CDLL:
    attempted=[]
    for path in paths or candidate_library_paths():
        attempted.append(str(path))
        if path.exists(): return _configure(ctypes.CDLL(str(path)))
    raise FileNotFoundError("Reality Bridge native library not found. Build cpp/ or set COSMIC_CONDUCTOR_NATIVE_LIB. Tried:\n- "+"\n- ".join(attempted))

class NativeString:
    def __init__(self,sample_rate:float=48_000.0,library:ctypes.CDLL|None=None):
        self._lib=library or load_native(); self._handle=self._lib.rb_string_create(float(sample_rate))
        if not self._handle: raise RuntimeError("rb_string_create returned null")
    def pluck(self,hz:float,force:float=0.8,damping:float=0.7,brightness:float=0.6,pick_position:float=0.25)->None:
        self._lib.rb_string_pluck(self._handle,float(hz),float(force),float(damping),float(brightness),float(pick_position))
    def process(self)->float: return float(self._lib.rb_string_process(self._handle))
    def stop(self)->None: self._lib.rb_string_stop(self._handle)
    def close(self)->None:
        if getattr(self,"_handle",None): self._lib.rb_string_destroy(self._handle); self._handle=None
    def __enter__(self)->"NativeString": return self
    def __exit__(self,exc_type,exc,tb)->None: self.close()
    def __del__(self)->None: self.close()
