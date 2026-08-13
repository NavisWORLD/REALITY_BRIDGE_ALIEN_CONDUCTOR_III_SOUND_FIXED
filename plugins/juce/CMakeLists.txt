cmake_minimum_required(VERSION 3.22)
project(RealityBridgePlugin VERSION 0.1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(DEFINED JUCE_DIR)
  add_subdirectory(${JUCE_DIR} JUCE-build)
elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/JUCE/CMakeLists.txt")
  add_subdirectory(JUCE)
else()
  message(FATAL_ERROR "JUCE not found. Pass -DJUCE_DIR=/path/to/JUCE or clone JUCE into plugins/juce/JUCE")
endif()
add_subdirectory(../../cpp rb-dsp-build)
juce_add_plugin(RealityBridgeInstrument
  COMPANY_NAME "NavisWORLD"
  BUNDLE_ID "world.navis.realitybridge.instrument"
  PLUGIN_MANUFACTURER_CODE NvWd
  PLUGIN_CODE RbAi
  FORMATS VST3 AU Standalone
  PRODUCT_NAME "Reality Bridge Alien Conductor"
  IS_SYNTH TRUE
  NEEDS_MIDI_INPUT TRUE
  NEEDS_MIDI_OUTPUT FALSE
  EDITOR_WANTS_KEYBOARD_FOCUS FALSE)
target_sources(RealityBridgeInstrument PRIVATE PluginProcessor.cpp PluginEditor.cpp)
target_include_directories(RealityBridgeInstrument PRIVATE ../../cpp/include)
target_link_libraries(RealityBridgeInstrument PRIVATE reality_bridge juce::juce_audio_utils juce::juce_dsp)
target_compile_definitions(RealityBridgeInstrument PRIVATE JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0)
