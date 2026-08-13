from reality_bridge.synapse import Synapse, SynapseConfig, conformance_sequence

def test_synapse_bounds_and_learning():
    s=Synapse()
    y=s.pulse(0.8,0.1,0.01)
    assert -1.0<=y<=1.0
    before=s.state.weight
    s.reinforce(0.75)
    assert s.config.weight_min<=s.state.weight<=s.config.weight_max
    assert s.state.tick==1
    assert s.state.weight!=before or s.state.trace==0.0

def test_snapshot_round_trip():
    s=Synapse(SynapseConfig())
    s.pulse(0.4,0.0,0.01)
    snapshot=s.snapshot()
    s.reset()
    s.restore(snapshot)
    assert s.snapshot()==snapshot

def test_batch_and_conformance_sequence():
    s=Synapse()
    out=s.process([0.1,0.2,0.3],[0.0,0.1,0.0])
    assert len(out)==3
    assert all(-1.0<=x<=1.0 for x in out)
    st=conformance_sequence()
    assert st.tick==7
    assert 0.1<=st.weight<=2.0
