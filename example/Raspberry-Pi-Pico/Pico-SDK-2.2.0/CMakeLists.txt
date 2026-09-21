# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
# As far as I know the Raspberry Pi Pico plugin for VSCode does not (yet) support bare RP2350 microcontrollers without a board.
# To adapt the C-SDK for a standard Pico board configure this CMakeLists.txt file via the Raspberry Pi Pico plugin's "Switch Board" option.
set(PICO_BOARD pico CACHE STRING "Board type")

# Uncomment the following two lines to compile for bare RP2350 without a board
# set(PICO_PLATFORM rp2350)
# set(PICO_BOARD none CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(hub75 C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name
add_executable(hub75 hub75_demo.cpp )

pico_set_program_name(hub75 "hub75_demo")
pico_set_program_version(hub75 "3.1")

set(PICO_PIO_VERSION 1)
pico_set_float_implementation(hub75 pico)

set(PANEL_GENERIC 0)
set(PANEL_FM6126A 1)
set(PANEL_RUL6024 2)

set(CHAIN_MODE_SERPENTINE 0)
set(CHAIN_MODE_RASTER 1)

if(PICO_BOARD STREQUAL "pico")
    set(BALANCED_LIGHT_OUTPUT_VALUE false)
else()
    set(BALANCED_LIGHT_OUTPUT_VALUE true)
endif()

set(SWAP_RB_PINS_VALUE false)

set(PANEL_PROFILE "64X32_1_16" CACHE STRING "Hub75 panel profile")
set_property(CACHE PANEL_PROFILE PROPERTY STRINGS
    "64X32_1_16"
    "64X64_1_32"
    "80X40_1_20"
    "96X48_1_24"
    "96X48_1_24_SM5368"
)

if(PANEL_PROFILE STREQUAL "64X64_1_32")
    set(MATRIX_PANEL_WIDTH_VALUE 64)
    set(MATRIX_PANEL_HEIGHT_VALUE 64)
    set(ROWSEL_N_PINS_VALUE 5)
    set(PANEL_SCAN_DEPTH_VALUE 32)
    set(PANEL_DEFINE_VALUE HUB75)
elseif(PANEL_PROFILE STREQUAL "64X32_1_16")
    set(MATRIX_PANEL_WIDTH_VALUE 64)
    set(MATRIX_PANEL_HEIGHT_VALUE 32)
    set(ROWSEL_N_PINS_VALUE 4)
    set(PANEL_SCAN_DEPTH_VALUE 16)
    set(PANEL_DEFINE_VALUE HUB75)
elseif(PANEL_PROFILE STREQUAL "80X40_1_20")
    set(MATRIX_PANEL_WIDTH_VALUE 80)
    set(MATRIX_PANEL_HEIGHT_VALUE 40)
    set(ROWSEL_N_PINS_VALUE 5)
    set(PANEL_SCAN_DEPTH_VALUE 20)
    set(PANEL_DEFINE_VALUE HUB75)
elseif(PANEL_PROFILE STREQUAL "96X48_1_24")
    set(MATRIX_PANEL_WIDTH_VALUE 96)
    set(MATRIX_PANEL_HEIGHT_VALUE 48)
    set(ROWSEL_N_PINS_VALUE 5)
    set(PANEL_SCAN_DEPTH_VALUE 24)
    set(PANEL_DEFINE_VALUE HUB75)
elseif(PANEL_PROFILE STREQUAL "96X48_1_24_SM5368")
    set(MATRIX_PANEL_WIDTH_VALUE 96)
    set(MATRIX_PANEL_HEIGHT_VALUE 48)
    set(ROWSEL_N_PINS_VALUE 3)
    set(PANEL_SCAN_DEPTH_VALUE 24)
    set(PANEL_DEFINE_VALUE HUB75_SM5368_ABC)
    set(SWAP_RB_PINS_VALUE true)
else()
    message(FATAL_ERROR "Unsupported PANEL_PROFILE: ${PANEL_PROFILE}")
endif()

# No need to modify preprocessor defines in hub75.cpp - instead set their values here.
#
# Example:
# Settings for a RP2350B microcontroller with GPIO pins spanning from 30 to 43.
# Beware to set `PICO_PLATFORM rp2350` and `PICO_BOARD none` prior to `include(pico_sdk_import.cmake)`
target_compile_definitions(hub75 PRIVATE
    # PICO_RP2350A=0              # PICO_RP2350A=0` means not a RP2350A but a RP2350B microcontroller - uncomment for RP235xB microcontroller only!
    USE_PICO_GRAPHICS=true      # set to false if you use hub75 as a library - any reference to pico_graphics is removed
    MATRIX_PANEL_WIDTH=${MATRIX_PANEL_WIDTH_VALUE}   # panel width from PANEL_PROFILE
    MATRIX_PANEL_HEIGHT=${MATRIX_PANEL_HEIGHT_VALUE} # panel height from PANEL_PROFILE
    CHAIN_MODE=CHAIN_MODE_SERPENTINE # set chain-mode - default is serpentine (U-Turn with compensation for 180° rotation)
    CHAIN_COLS=1                # number of panels chained left-to-right in a single chain row (columns)
    CHAIN_ROWS=1                # number of chain rows stacked vertically (rows)
    DATA_BASE_PIN=0             # base GPIO pin (aka start index) of R0, G0, B0, R1, G1, B1 GPIO pins
    DATA_N_PINS=6               # number (count) of colour pins (usually 6)
    SWAP_RB_PINS=${SWAP_RB_PINS_VALUE}               # swap R/B data pin mapping in software
    ROWSEL_BASE_PIN=6           # base GPIO row select pin (aka start index) of A, B (, C, D. E) GPIO pins
    ROWSEL_N_PINS=${ROWSEL_N_PINS_VALUE}             # row select pin count from PANEL_PROFILE
    PANEL_SCAN_DEPTH=${PANEL_SCAN_DEPTH_VALUE}       # scan depth from PANEL_PROFILE
    CLK_PIN=11                  # GPIO pin for CLK 
    STROBE_PIN=12               # GPIO pin for STROBE (LATCH)
    OEN_PIN=13                  # GPIO for OE pin
    PANEL_TYPE=PANEL_GENERIC    # select PANEL_TYPE
    INVERTED_STB=false          # inverted pin signal for OE (untested)
    SM_CLOCKDIV_FACTOR=2.0f     # to prevent flicker or ghosting it might be worth a try to reduce state machine speed
    BITPLANES=8                 # number (count) of bit-planes used for BCM (Binary Code Modulation) - valid values for BIT_DEPTH are 8 or 10
    BALANCED_LIGHT_OUTPUT=${BALANCED_LIGHT_OUTPUT_VALUE} # false on pico, true on other boards
    SEPARATE_CIE_CHANNELS=true  # use separate CIE channels for improved colour representation - needs more memory
    CCM_RG_SHIFT=6              # CCM Cross-channel mixing - mix ~1.6% green into the red channel
    CCM_GB_SHIFT=7              # CCM Cross-channel mixing - mix ~0.8% blue into the green channel
    BASE_LATCH_NS=120           # wait time in nano-seconds to stabilise latch
    BASE_ADDR_NS=200            # wait time in nano-seconds to stabilise row addressing
    BASE_OE_NS=60               # pre-Oe guard wait time in nano-seconds (prevents ghost flashes)
    HUB75_MULTICORE=true        # use core1 for the hub75 driver
    FRAME_RATE=false            # for testing and debugging purpose only: output frame rate information (printf) in monitor - set to `false` for production
)

target_compile_definitions(hub75 PRIVATE ${PANEL_DEFINE_VALUE})

# Generate PIO header
pico_generate_pio_header(hub75 ${CMAKE_CURRENT_LIST_DIR}/src/hub75.pio)

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(hub75 0)
pico_enable_stdio_usb(hub75 1)

add_subdirectory(common)
add_subdirectory(libraries)

target_sources(hub75 PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/src/hub75.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/bouncing_balls.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/antialiased_line.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/fire_effect.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/rotator.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/analog_clock.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/pixel_fill.hpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/grey_scale_stripes.hpp
        ${CMAKE_CURRENT_LIST_DIR}/src/rul6024.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/fm6126a.cpp
        ${CMAKE_CURRENT_LIST_DIR}/examples/hue_value_spectrum.hpp
        ${CMAKE_CURRENT_LIST_DIR}/hub75_demo.cpp
        )

# Add the standard library to the build
target_link_libraries(hub75
        pico_stdlib
        pico_multicore
        pico_aon_timer
        hardware_pio
        hardware_dma
        hardware_vreg
        pico_graphics)

if(PICO_CYW43_SUPPORTED)
    target_link_libraries(hub75
                          pico_cyw43_arch_none)
endif()

# Add the standard include files to the build
target_include_directories(hub75 PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/src
        ${CMAKE_CURRENT_LIST_DIR}/examples
        ${CMAKE_CURRENT_LIST_DIR}
)

pico_add_extra_outputs(hub75)
