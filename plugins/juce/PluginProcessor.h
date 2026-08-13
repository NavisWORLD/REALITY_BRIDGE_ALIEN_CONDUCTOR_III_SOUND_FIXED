#pragma once
#include <JuceHeader.h>
#include "reality_bridge/dsp.hpp"
#include <array>
class RealityBridgeProcessor:public juce::AudioProcessor{
public:
 RealityBridgeProcessor();void prepareToPlay(double,int)override;void releaseResources()override{}bool isBusesLayoutSupported(const BusesLayout&)const override;void processBlock(juce::AudioBuffer<float>&,juce::MidiBuffer&)override;juce::AudioProcessorEditor* createEditor()override;bool hasEditor()const override{return true;}const juce::String getName()const override{return "Reality Bridge Alien Conductor";}bool acceptsMidi()const override{return true;}bool producesMidi()const override{return false;}bool isMidiEffect()const override{return false;}double getTailLengthSeconds()const override{return 8.;}int getNumPrograms()override{return 1;}int getCurrentProgram()override{return 0;}void setCurrentProgram(int)override{}const juce::String getProgramName(int)override{return{};}void changeProgramName(int,const juce::String&)override{}void getStateInformation(juce::MemoryBlock&)override;void setStateInformation(const void*,int)override;juce::AudioProcessorValueTreeState state;
private:
 struct Voice{reality_bridge::KarplusStrongString string;int note=-1;bool active=false;explicit Voice(double sr=48000.):string(sr){}};std::array<Voice,16> voices_{};reality_bridge::StereoBody body_;reality_bridge::SoftLimiter limiter_;int voiceCursor_=0;double sr_=48000.;void noteOn(int,float);void allNotesOff();static juce::AudioProcessorValueTreeState::ParameterLayout params();JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(RealityBridgeProcessor)
};
