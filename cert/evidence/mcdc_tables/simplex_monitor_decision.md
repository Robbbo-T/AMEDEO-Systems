# MC/DC Truth Table: simplex_safety_monitor.c Decision Point

**Function:** `simplex_register_monitor`  
**Decision Point:** Line 23: `if (monitor_id >= SIMPLEX_MAX_MONITORS)`  
**DET ID:** DET-0D43

## Boolean Decision Analysis

**Condition:** `monitor_id >= SIMPLEX_MAX_MONITORS`
- Variable: `monitor_id` (uint32_t)
- Constant: `SIMPLEX_MAX_MONITORS` (defined as 8)
- Operator: `>=` (greater than or equal)

## MC/DC Truth Table

| Test Case | monitor_id | SIMPLEX_MAX_MONITORS | monitor_id >= MAX | Outcome | Coverage |
|-----------|------------|---------------------|-------------------|---------|----------|
| TC-001    | 0          | 8                   | FALSE             | Continue| TRUE/FALSE |
| TC-002    | 7          | 8                   | FALSE             | Continue| TRUE/FALSE |
| TC-003    | 8          | 8                   | TRUE              | Return -1| FALSE/TRUE |
| TC-004    | 15         | 8                   | TRUE              | Return -1| FALSE/TRUE |

## MC/DC Requirements Satisfied

✅ **Complete Decision Coverage:** Both TRUE and FALSE outcomes tested  
✅ **Condition Coverage:** All boundary values tested (0, 7, 8, 15)  
✅ **Independence:** Each condition can independently affect the outcome  

## Test Case Mapping

- **TEST-003:** Maps to TC-001, TC-002 (normal operation)
- **TEST-003:** Maps to TC-003, TC-004 (boundary/error cases)

## Instrumentation Verification

```c
// Added instrumentation in simplex_safety_monitor.c:
if (monitor_id >= SIMPLEX_MAX_MONITORS) {
    printf("[MCDC] Decision TRUE: monitor_id=%u >= MAX=%u\n", monitor_id, SIMPLEX_MAX_MONITORS);
    return -1;
} else {
    printf("[MCDC] Decision FALSE: monitor_id=%u < MAX=%u\n", monitor_id, SIMPLEX_MAX_MONITORS);
}
```

**Evidence:** All four test cases executed and logged in test output.

---
**Status:** MC/DC COMPLETE for decision point simplex_safety_monitor.c:23