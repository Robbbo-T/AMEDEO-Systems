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

file(GLOB SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.c)
add_executable(tests_ata27_flight_ctrl_host ${SRC_FILES} ${CMAKE_SOURCE_DIR}/tests/ata27_flight_ctrl_host.c)

# Link against libm for math functions
if(UNIX)
  target_link_libraries(tests_ata27_flight_ctrl_host m)
endif()

# Place binaries in out/
set_target_properties(tests_ata27_flight_ctrl_host PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out
)
