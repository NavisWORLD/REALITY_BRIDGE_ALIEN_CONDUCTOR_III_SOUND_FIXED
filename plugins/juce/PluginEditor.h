#pragma once
#include <JuceHeader.h>
#include "PluginProcessor.h"
class RealityBridgeEditor:public juce::AudioProcessorEditor{public:explicit RealityBridgeEditor(RealityBridgeProcessor&);void paint(juce::Graphics&)override;void resized()override;private:RealityBridgeProcessor&p_;juce::Label title_;JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(RealityBridgeEditor)};
