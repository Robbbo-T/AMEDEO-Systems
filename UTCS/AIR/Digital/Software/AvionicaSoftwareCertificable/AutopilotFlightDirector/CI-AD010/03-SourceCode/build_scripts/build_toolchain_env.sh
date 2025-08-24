#!/bin/bash
# Build toolchain environment setup for CI-AD010 AutopilotComputer
# UTCS/AIR System - DAL-C Compliant Build Environment

echo "Setting up CI-AD010 AutopilotComputer build environment..."

# Set environment variables for certified build
export APC_ROOT="$(pwd)/.."
export APC_SRC="$APC_ROOT/src"
export APC_INC="$APC_ROOT/inc"
export APC_BUILD="$APC_ROOT/build_scripts"
export APC_EXEC="$APC_ROOT/../04-Executables"

# Compiler settings for DAL-C compliance
export CC="gcc"
export CFLAGS="-Wall -Wextra -std=c99 -O2 -DDAL_C_COMPLIANCE"

# Tool versions (for certification traceability)
export COMPILER_VERSION="$(gcc --version | head -n1)"
export BUILD_DATE="$(date -u +%Y%m%d_%H%M%S)"

echo "Environment setup complete."
echo "CC: $CC"
echo "CFLAGS: $CFLAGS" 
echo "APC_ROOT: $APC_ROOT"
echo "Build Date: $BUILD_DATE"
echo "Compiler Version: $COMPILER_VERSION"