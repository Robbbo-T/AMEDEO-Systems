# Third Party SOUP Watchlist
# CI-AD010 AutopilotComputer

## Software of Unknown Provenance (SOUP) Components

### Real-Time Operating System
- **Component**: PikeOS RTOS
- **Version**: 5.1
- **Vendor**: SYSGO AG
- **Certification**: DO-178C DAL-A certified
- **Support Status**: Active (supported until 2027)
- **Version Lifecycle**: 
  - v5.1: Current (2020-2027)
  - v6.0: Available (2024-2031)
  - Migration recommended by Q2 2026

### Math Libraries
- **Component**: ARM CMSIS DSP Library
- **Version**: 1.14.4
- **Vendor**: ARM Limited
- **Support Status**: Active
- **Last Update**: March 2024
- **Security**: No known vulnerabilities
- **Recommendation**: Continue monitoring for updates

### Communication Stack
- **Component**: lwIP TCP/IP Stack
- **Version**: 2.1.3
- **Vendor**: Open Source Community
- **Support Status**: Active development
- **Security**: Regular security patches available
- **Recommendation**: 
  - Monitor for security advisories
  - Plan update to v2.2.x when stable

## Risk Assessment
- **Overall Risk**: LOW
- **Next Review Date**: December 2024
- **Responsible**: Software Architecture Team

## Actions Required
1. Plan PikeOS migration strategy for 2026
2. Evaluate lwIP v2.2.x for 2025 update
3. Continue security monitoring
4. Maintain vendor relationships

*Last Updated: June 2024*
*Classification: DAL-C Compliance*