# Airtime Allocation System (AAS)

## Overview
This directory contains stub files and specifications for InquiryCircle's Airtime Allocation System - a comprehensive framework for managing speaking time in virtual meetings.

## System Components

### Domain Layer (Pure Python)
- **airtime.py** - Core domain models for time tracking and allocation
- **allocation_rules.py** - Different rule implementations (equal share, progressive stack, etc.)
- **token_economy.py** - Token-based system integrating reactions with airtime (depends on reactions)
- **airtime_policy.py** - Policy enforcement and validation

### Infrastructure Layer
- **jitsi_tracker.py** - Adapter for tracking Jitsi dominant speaker events

### Tests
- **airtime_test.py** - Comprehensive unit test stubs

## Airtime Allocation Concepts

### Time Tracking (Hourglass System)
- Monitor dominant speaker via Jitsi API
- Track cumulative speaking time per participant
- Display visual indicators and warnings
- **Enforcement**: Advisory only (stats and warnings)

### Allocation Rules
Different algorithms for distributing speaking time:

1. **Equal Share**: `duration / num_participants`
2. **Custom Allocation**: Facilitator-defined (e.g., invited speaker gets more)
3. **Progressive Stack**: Less spoken = higher priority/more time
4. **Round-Robin**: Fixed time slots in rotation
5. **Reaction-Based**: Positive reactions add time, negative subtract
6. **Advisory Only**: Track and report, no enforcement

### Token Economy
Complete token-based system where:
- Speaking costs tokens (1 token = 30 seconds)
- Sending reactions costs tokens
- Receiving positive reactions earns tokens
- Receiving negative reactions reduces tokens
- **Dependencies**: Requires reaction system to be implemented first

### Enforcement Levels
- **ADVISORY**: Stats only, no control
- **SOFT**: Warnings and prompts
- **HARD**: Auto-mute when time expires

## Integration Points

### Reactions System Dependency
The token economy directly integrates with the reaction system:
```python
# Token costs/rewards
Sending "love": -2 tokens
Receiving "love": +2 tokens
Sending "like": -1 token
Receiving "like": +1 token
Sending "dislike": -1 token (target loses 1 token)
Sending "hate": -2 tokens (target loses 2 tokens)
```

### Jitsi Integration
- Listens for `dominantSpeakerChanged` events
- Tracks speaking sessions automatically
- Can send mute/unmute commands (hard enforcement)

### Backend Architecture
Fits into `/backend/interactions/` app:
```
backend/interactions/
├── domain/
│   ├── reactions.py         # Implemented first
│   ├── airtime.py           # AAS core
│   ├── allocation_rules.py  # Rule implementations
│   └── token_economy.py     # Depends on reactions
├── infrastructure/
│   ├── jitsi_tracker.py     # Speaker tracking
│   └── ...
```

## Development Strategy

### Phase 1: Basic Time Tracking
- Implement airtime.py domain models
- Track speaking time (no enforcement)
- Display stats to participants
- **UI**: Simple timer display

### Phase 2: Allocation Rules
- Implement rule algorithms
- Add warning system
- Soft enforcement (warnings only)
- **UI**: Time allocation displays, warning indicators

### Phase 3: Policy Enforcement
- Implement policy layer
- Add hard enforcement (auto-mute)
- Facilitator override controls
- **UI**: Enforcement controls for facilitators

### Phase 4: Token Economy
- Integrate with reaction system
- Implement token transactions
- Full economic model
- **UI**: Token balance displays, transaction history

## Facilitator Controls
Facilitators can:
- ✅ Choose allocation rule for meeting
- ✅ Set enforcement level (advisory/soft/hard)
- ✅ Override rules (bypass, reallocate, pause)
- ✅ View real-time usage statistics
- ✅ Manually grant time bonuses/penalties

## Workorder Planning

Planned workorders (similar to reactions):
1. **workorder-airtime-domain.yml** - Core domain models and services
2. **workorder-allocation-rules.yml** - Rule implementations
3. **workorder-airtime-tests.yml** - Comprehensive unit tests
4. **workorder-token-economy.yml** - Token system (after reactions complete)
5. **workorder-jitsi-tracker.yml** - Infrastructure adapter

## File Status

All files are **stubs only** - no implementation logic:
- ✅ Classes defined
- ✅ Methods outlined
- ✅ Interfaces specified
- ✅ Comments show intended logic
- ❌ No actual implementation

## Related Documentation
- **Parent Discussion**: [airtimeAllocationSystems.md](../airtimeAllocationSystems.md)
- **Reaction Stubs**: [2025-09-22-jitsi-api-python](../2025-09-22-jitsi-api-python/)
- **Project Spec**: See project-spec.md in InquiryCircle documentation

---

**Created**: 2025-10-04
**Status**: Stub files ready for workorder creation
**Dependencies**: Reaction system (for token economy)
