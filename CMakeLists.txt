cmake_minimum_required(VERSION 3.15)
project(amedeo C)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Output directory
if(NOT CMAKE_RUNTIME_OUTPUT_DIRECTORY)
  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
endif()

# Warnings and optimization
add_compile_options(-Wall -Wextra -Werror -O2 -pedantic)

include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/kernel)
include_directories(${CMAKE_SOURCE_DIR}/kernel/core)
include_directories(${CMAKE_SOURCE_DIR}/framework/cqea)

file(GLOB SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.c)
file(GLOB KERNEL_FILES ${CMAKE_SOURCE_DIR}/kernel/*.c)
file(GLOB KERNEL_CORE_FILES ${CMAKE_SOURCE_DIR}/kernel/core/*.c)
file(GLOB CQEA_FILES ${CMAKE_SOURCE_DIR}/framework/cqea/*.c)

# ATA-27 test executable
add_executable(tests_ata27_flight_ctrl_host ${SRC_FILES} ${CMAKE_SOURCE_DIR}/tests/ata27_flight_ctrl_host.c)

# System-of-systems integration demo
add_executable(integration_demo 
  ${SRC_FILES} 
  ${KERNEL_FILES} 
  ${CQEA_FILES} 
  ${CMAKE_SOURCE_DIR}/integration/system-of-systems/integration_demo.c
)

# Envelope checker tests (safety monitor unit tests)
add_executable(envelope_checker_tests
  ${KERNEL_CORE_FILES}
  ${CMAKE_SOURCE_DIR}/kernel/core/envelope_checker_tests.c
)

# Link against libm for math functions
if(UNIX)
  target_link_libraries(tests_ata27_flight_ctrl_host m)
  target_link_libraries(integration_demo m)
  target_link_libraries(envelope_checker_tests m)
endif()

# Place binaries in out/
set_target_properties(tests_ata27_flight_ctrl_host PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out
)
set_target_properties(integration_demo PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out
)
set_target_properties(envelope_checker_tests PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out
)
