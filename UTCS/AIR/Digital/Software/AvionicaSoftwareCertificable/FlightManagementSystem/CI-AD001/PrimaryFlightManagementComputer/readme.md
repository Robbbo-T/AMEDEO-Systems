AIR/
└── Digital/
    └── Software/
        └── AvionicaSoftwareCertificable/
            └── FlightManagementSystem/
                └── CI-AD001/  # [PrimaryFlightManagementComputer]
                    │
                    ├── 01-Requirements/                   # System and Software Requirements
                    │   ├── System-Interface-Requirements/ # Documents describing interfaces with other systems/hardware
                    │   │   ├── ICD-PFMC-ADC-001.pdf       # Interface Control Document - Air Data Computer
                    │   │   └── ICD-PFMC-GPS-001.pdf       # Interface Control Document - GPS Receiver
                    │   ├── High-Level-Requirements/       # Software Requirements Specifications (SRS)
                    │   │   ├── SRS-PFMC-Navigation.docx
                    │   │   ├── SRS-PFMC-Guidance.docx
                    │   │   └── SRS-PFMC-Performance.docx
                    │   ├── Low-Level-Requirements/        # Detailed functional and non-functional requirements (Module-level)
                    │   │   ├── LLR-PFMC-FlightPlanMgmt.docx
                    │   │   ├── LLR-PFMC-WaypointCalc.docx
                    │   │   └── LLR-PFMC-DisplayOutput.docx
                    │   └── Requirements-Traceability/     # Traceability matrices (e.g., DOORS exports, custom tools)
                    │       ├── RTM-SystemToHighLevel.xlsx
                    │       └── RTM-HighToLowLevel.xlsx
                    │
                    ├── 02-Design/                         # Architectural and Detailed Design
                    │   ├── Software-Architecture/         # Top-level design, module decomposition, high-level data flow
                    │   │   ├── SAD-PFMC-Overview.pdf      # Software Architecture Document
                    │   │   └── ModuleDecomposition.vsdx   # Visual diagrams of modules and their relationships
                    │   ├── Detailed-Design/               # Module-level design, algorithm descriptions, data structures
                    │   │   ├── DDD-PFMC-NavigationCore.pdf # Detailed Design Document for Navigation Core
                    │   │   ├── DDD-PFMC-GuidancePath.pdf
                    │   │   └── DataDictionary.xlsx        # Definition of all major data types and structures
                    │   └── Interface-Design-Documents/    # Detailed design of internal and external interfaces
                    │       └── IDD-PFMC-InternalModules.pdf
                    │
                    ├── 03-SourceCode/                     # Actual Code (Under Configuration Control)
                    │   ├── src/
                    │   │   ├── modules/                   # e.g., Navigation, Guidance, Performance, FMS Core
                    │   │   │   ├── Navigation/
                    │   │   │   │   ├── nav_data_mgr.c
                    │   │   │   │   └── position_calc.c
                    │   │   │   ├── Guidance/
                    │   │   │   │   ├── path_generator.c
                    │   │   │   │   └── flight_director.c
                    │   │   │   └── Core/
                    │   │   │       ├── fms_main.c
                    │   │   │       └── io_manager.c
                    │   │   └── common/                    # Reusable components
                    │   │       └── utilities.c
                    │   ├── inc/                           # Header files
                    │   │   ├── modules/
                    │   │   │   ├── Navigation/
                    │   │   │   │   └── nav_data_mgr.h
                    │   │   │   └── Guidance/
                    │   │   │       └── path_generator.h
                    │   │   └── common/
                    │   │       └── utilities.h
                    │   ├── lib/                           # Pre-compiled, internally-developed library modules
                    │   │   └── fms_math_lib.a             # Example: Optimized FMS Math Library
                    │   ├── build_scripts/                 # Compilation scripts (Makefiles, CMake, automation scripts)
                    │   │   ├── Makefile_PFMC
                    │   │   ├── CMakeLists.txt
                    │   │   └── build_toolchain_env.sh     # Script to setup certified build environment paths
                    │   └── README.md                      # Project level README
                    │
                    ├── 04-Executables/                    # Built and certified binary outputs
                    │   ├── Releases/                      # Released versions for testing/installation
                    │   │   ├── V1.0.0/
                    │   │   │   ├── pfmc_app_v1.0.0.bin    # Certified binary
                    │   │   │   ├── pfmc_app_v1.0.0.md5    # Checksum
                    │   │   │   └── ReleaseNotes_v1.0.0.txt
                    │   │   └── V1.0.1/
                    │   ├── Debug/                         # Debug builds for development
                    │   │   └── pfmc_app_debug.elf
                    │   └── Build_Logs/                    # Logs generated during the build process
                    │       ├── build_log_V1.0.0.txt
                    │       └── build_config_V1.0.0.txt    # Configuration used for the build
                    │
                    ├── 05-Tests/                          # Verification Artifacts (Extremely Important for DO-178C)
                    │   ├── UnitTests/                     # Verification of Low-Level Requirements (LLRs)
                    │   │   ├── Test_Plans/                # Unit Test Plan (UTP)
                    │   │   │   └── UTP-PFMC-NavigationCore.pdf
                    │   │   ├── Test_Cases/                # Unit Test Cases (UTC)
                    │   │   │   └── UTC-PFMC-WaypointCalc.xlsx
                    │   │   ├── Test_Procedures/           # Unit Test Procedures (UTP)
                    │   │   │   └── UTP_Procedure_PositionCalc.pdf
                    │   │   ├── Test_Results/              # Unit Test Results, Logs, Execution Records
                    │   │   │   └── UnitTestReport_NavigationCore_20231025.xml
                    │   │   └── Coverage_Reports/          # Structural Coverage for unit level (Statement, Decision)
                    │   │       └── UnitCoverage_NavigationCore_20231025.html
                    │   ├── IntegrationTests/              # Verification of High-Level Requirements (HLRs) and module interfaces
                    │   │   ├── Test_Plans/                # Software Integration Test Plan (SITP)
                    │   │   │   └── SITP-PFMC-Modules.pdf
                    │   │   ├── Test_Cases/                # Integration Test Cases (ITC)
                    │   │   │   └── ITC-PFMC-FMSCore_IO.xlsx
                    │   │   ├── Test_Procedures/           # Integration Test Procedures (ITP)
                    │   │   │   └── ITP_Procedure_FlightPlanLoad.pdf
                    │   │   ├── Test_Results/              # Integration Test Results, Logs
                    │   │   │   └── IntegrationTestReport_20231101.pdf
                    │   │   └── Environment/               # Test environment setup for integration testing
                    │   │       └── SIT_TestHarness_Config.xml
                    │   ├── SystemTests/                   # Verification of System Requirements on simulated or target environment
                    │   │   ├── Test_Plans/                # Software Test Plan (STP)
                    │   │   │   └── STP-PFMC-System.pdf
                    │   │   ├── Test_Cases/                # System Test Cases (STC)
                    │   │   │   └── STC-PFMC-FullFlightPath.xlsx
                    │   │   ├── Test_Procedures/           # System Test Procedures (STP)
                    │   │   │   └── STP_Procedure_AutoFlight_Scenario1.pdf
                    │   │   ├── Test_Results/              # System Test Results, Logs, Evidence
                    │   │   │   └── SystemTestReport_Run_20231115.pdf
                    │   │   └── Environment/               # Simulator/Test Bench configuration for system tests
                    │   │       └── FullFlightSim_Setup.docx
                    │   └── HardwareSoftwareIntegrationTests/ # Verification on actual target hardware (PFMC box)
                    │       ├── Test_Plans/                # Hardware-Software Integration Test Plan (HSITP)
                    │       │   └── HSITP-PFMC-Hardware.pdf
                    │       ├── Test_Cases/                # HSIT Test Cases (HSITC)
                    │       │   └── HSITC-PFMC-ARINC429_Comm.xlsx
                    │       ├── Test_Procedures/           # HSIT Test Procedures (HSITP)
                    │       │   └── HSITP_Procedure_SensorInputValidation.pdf
                    │       ├── Test_Results/              # HSIT Test Results, Logs, Evidence
                    │       │   └── HSITReport_20231201.pdf
                    │       └── Environment/               # Hardware-in-the-Loop (HIL) setup
                    │           └── HIL_TestBed_Diagram.vsdx
                    │
                    ├── 06-Documentation/                  # Lifecycle Data for Certification (DO-178C)
                    │   ├── Plans/                         # Mandatory plans for DO-178C
                    │   │   ├── PSAC-PFMC.pdf              # Plan for Software Aspects of Certification
                    │   │   ├── SDP-PFMC.pdf               # Software Development Plan
                    │   │   ├── SCMP-PFMC.pdf              # Software Configuration Management Plan
                    │   │   ├── SQAP-PFMC.pdf              # Software Quality Assurance Plan
                    │   │   └── SVVP-PFMC.pdf              # Software Verification and Validation Plan
                    │   ├── Design-Docs/                   # References/copies to documents from 02-Design
                    │   │   ├── SAD-PFMC-Overview.pdf
                    │   │   └── DDD-PFMC-NavigationCore.pdf
                    │   ├── Review-Records/                # Records of formal reviews (e.g., PDR, CDR, TRRs)
                    │   │   ├── RequirementReview_Minutes_20230115.pdf
                    │   │   └── DesignReview_Checklist_ModuleX.xlsx
                    │   ├── Reports/                       # Summary reports from various lifecycle processes
                    │   │   ├── VerificationSummaryReport.pdf
                    │   │   ├── ConfigurationAuditReport.pdf
                    │   │   └── QualityAssuranceReport.pdf
                    │   ├── Certification-Logs/            # Compliance matrices for DO-178C, SOI audit records
                    │   │   ├── RACM-PFMC.xlsx             # Requirements Traceability and Compliance Matrix
                    │   │   ├── DACM-PFMC.xlsx             # Design and Code Traceability Matrix
                    │   │   ├── SOI1_AuditReport.pdf       # Stage of Involvement 1 Audit Report
                    │   │   └── ProblemReport_Log.xlsx     # Software Anomaly/Problem Report Log
                    │   └── User-Maintenance-Manuals/      # Operational and maintenance documentation
                    │       ├── PFMC_User_Manual.pdf
                    │       └── PFMC_Maintenance_Manual.pdf
                    │
                    ├── 07-Tools/                          # Qualified & Non-Qualified Tooling Documentation & Configuration
                    │   ├── Compiler/                      # Compiler version documentation and qualification data
                    │   │   ├── Compiler_TQAR.pdf          # Tool Qualification Accomplishment Summary (e.g., for GCC ARM)
                    │   │   └── Compiler_Configuration.txt # Specific compiler flags and settings
                    │   ├── Test-Framework/                # Automated test environment qualification data and setup scripts
                    │   │   ├── TestHarness_TQAR.pdf
                    │   │   └── TestHarness_SetupScripts/  # Scripts to configure the test harness environment
                    │   ├── Coverage-Analyzer/             # Code coverage tool qualification and configuration
                    │   │   ├── CoverageAnalyzer_TQAR.pdf  # E.g., for VectorCAST or similar
                    │   │   └── CoverageTool_Settings.xml
                    │   ├── Static-Analysis/               # Static code analysis tool details and qualification
                    │   │   └── StaticAnalyzer_TQAR.pdf    # E.g., for Polyspace or similar
                    │   └── Version-Control/               # Version control system details (e.g., Git, SVN)
                    │       └── VCS_Configuration.txt      # Configuration for the chosen VCS (e.g., git hooks, repo structure rules)
                    │   # Note: Actual multi-gigabyte tool installations are typically managed externally on controlled build servers,
                    │   # with their usage dictated by scripts and configurations within this directory and 03-SourceCode/build_scripts.
                    │
                    ├── 08-ThirdParty/                     # Managed external components (COTS/SOUP)
                    │   ├── RTOS/                          # Real-Time Operating System
                    │   │   ├── VxWorks_vX.Y_License.pdf   # License and usage terms
                    │   │   ├── VxWorks_vX.Y_Binary/       # Pre-compiled RTOS components
                    │   │   ├── VxWorks_CertificationSupplement.pdf # RTOS certification artifacts/data
                    │   │   └── RTOS_Interface_Spec.pdf    # How PFMC interfaces with the RTOS
                    │   ├── Drivers/                       # Hardware-specific drivers (often SOUP)
                    │   │   ├── ADC_Driver_v1.0/
                    │   │   │   ├── src/                   # If source is available and auditable
                    │   │   │   ├── bin/
                    │   │   │   └── docs/                  # Driver specification, test reports
                    │   │   └── Ethernet_Driver_v2.1/
                    │   └── Libraries/                     # COTS (Commercial Off-The-Shelf) libraries (must be qualified/analyzed as SOUP)
                    │       ├── MathLibrary_v3.0/          # E.g., specific floating-point math libraries
                    │       │   ├── libmath.a
                    │       │   ├── MathLib_SOUP_Analysis.pdf # SOUP analysis report for the math library
                    │       │   └── MathLib_Interface.h
                    │       └── CryptoLib_v1.5/            # If cryptographic functions are used (often highly scrutinized)
                    │           └── CryptoLib_SOUP_Analysis.pdf
                    │
                    └── 09-Ops-Maintenance/                # Deliverables for Airline Operations & Maintenance
                        │
                        ├── 01-Flight-Deck-Manuals/        # Documents for Pilots
                        │   ├── FCOM/                      # Flight Crew Operating Manual
                        │   │   └── PFMC_FCOM_Suppliment.pdf
                        │   └── QRH/                       # Quick Reference Handbook
                        │       └── PFMC_QRH_Procedures.pdf
                        │
                        ├── 02-Maintenance-Manuals/        # Documents for Mechanics & Engineers
                        │   ├── AMM/                       # Aircraft Maintenance Manual
                        │   │   └── PFMC_AMM_Chapter.pdf
                        │   ├── CMM/                       # Component Maintenance Manual (for the LRU itself)
                        │   │   └── CI-AD001_CMM.pdf
                        │   ├── FIM/                       # Fault Isolation Manual
                        │   │   └── PFMC_FIM_Chapters.pdf
                        │   └── IPC/                       # Illustrated Parts Catalog
                        │       └── PFMC_IPC.pdf
                        │
                        ├── 03-Installation-Data/          # Data for installing the LRU/Software on aircraft
                        │   ├── Software-Loading-Instructions.pdf
                        │   ├── Aircraft-Wiring-Diagrams.pdf
                        │   └── Connector-Pinouts.pdf
                        │
                        ├── 04-Digital-Twin/               # Digital Thread/Digital Twin Artifacts
                        │   ├── As-Maintained-Configuration/  # Golden record of SW config per aircraft tail #
                        │   │   ├── Tail_N12345_ConfigRecord.json
                        │   │   └── Tail_N67890_ConfigRecord.json
                        │   ├── Performance-Models/         # Models for predicting performance/degradation
                        │   │   └── PFMC_Performance_Model.m
                        │   ├── Prognostics-Health-Mgmt/    # PHM data & algorithms
                        │   │   ├── PHM_Algorithms/
                        │   │   └── Usage-Monitoring-Parameters.xml
                        │   └── Simulation-Models/          # High-fidelity models for ground-based troubleshooting
                        │       └── PFMC_Emulator_vX.Y.zip
                        │
                        ├── 05-Training-Materials/         # For airline maintenance training
                        │   ├── PFMC_Training_Slides.pptx
                        │   └── Troubleshooting_Labs.zip
                        │
                        ├── 06-Service-Bulletins/          # Released service information
                        │   ├── SB-PFMC-2023-001.pdf       # E.g., Mandatory software update
                        │   └── SL-PFMC-2023-005.pdf       # Service Letter (recommendation)
                        │
                        └── 07-Troubleshooting-Logs/       # Example logs & data for maintenance
                            └── Example_Fault_Scenario_Log.bin
