"""Reality Bridge reusable musical-state and Synaptic Core engine."""
from .engine import (AccompanimentEngine, BridgeState, HarmonicHypothesis,
                     MediaDNA, NoteEvent, VoiceDNA, midi_to_hz, hz_to_midi)
from .synapse import (SYNAPSE_VERSION, Synapse, SynapseConfig, SynapseState,
                      conformance_sequence)
__all__=['AccompanimentEngine','BridgeState','HarmonicHypothesis','MediaDNA','NoteEvent','VoiceDNA','midi_to_hz','hz_to_midi','SYNAPSE_VERSION','Synapse','SynapseConfig','SynapseState','conformance_sequence']
__version__='0.3.0'
