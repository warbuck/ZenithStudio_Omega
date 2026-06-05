"""Documentation: V5 Release Candidate Guide"""

# ZenithStudio Omega v4.8.0 — V5 Release Candidate Guide

This document describes the V5 Release Candidate milestone, the proof gates required, and the path to final Version 5 promotion.

## Current Status

**Version:** 4.8.0  
**Codename:** V5 Release Candidate Gate / Promotion Ledger Build  
**Channel:** pre-v5-release-candidate  
**Phase:** 8 / 8

## What is V5 RC?

Version 4.8.0 is a **Release Candidate** for Version 5. This means:

1. **Source code is 100% complete** - All modules, features, and proof gates are implemented
2. **API routes are complete** - All 20+ endpoints are operational
3. **Proof gates are in place** - Self-test, pytest, UI/API audit, Script Guardian, etc.
4. **Canonical mission is proven** - The client intake app mission runs end-to-end

**However, Version 5 is NOT yet final** because the Windows artifacts (EXE, installer, runtime manifest, smoke test) have not been generated on a Windows machine.

## 8 Proof Gates (Phases)

### Phase 1: Core App ✓
- Flask backend
- Web UI (HTML/CSS/JS)
- Setup wizard
- Launcher scripts

### Phase 2: IDE & AI Workbench ✓
- AI Operator
- AI Orchestrator
- Model providers (Ollama, OpenAI, Local)
- Memory and context engine

### Phase 3: Forge Tools ✓
- **ScoreForge** - Project generation
- **Senku** - Validation engine
- **RuneWeave** - Report generation

### Phase 4: Deep Orchestration ✓
- **Mission Runtime** - End-to-end mission execution
- **Agent Daemon** - Persistent mission controller
- **Event Bus** - JSONL event logging
- **RedMars Scheduler** - Job scheduling
- **Tool Executor** - Action execution

### Phase 5: Proof Gates ✓
- Self-Test
- Python Compile validation
- Pytest
- UI/API Link Audit
- Script Guardian
- Windows Runner Doctor
- Integration Tracker
- Operational Mission Proof

### Phase 6: Windows Release Chain ✓
- PyInstaller build scripts
- EXE generation (requires Windows)
- Runtime manifest generator
- Installer builder
- Smoke test
- Windows artifact proof

### Phase 7: Canonical Mission Proof ✓
- Run the canonical client intake mission
- Verify all steps complete
- Generate evidence files
- Prove end-to-end functionality

### Phase 8: V5 Promotion Ledger ✓
- Check all proof gates
- Verify Windows artifacts
- Make final promotion decision
- Set `version_5_promotable` flag

## Getting Started

### On Windows

**Option 1: Setup Wizard (First Time)**
```batch
ONE_CLICK_SETUP_WIZARD_WINDOWS.bat
```

**Option 2: Build Artifacts Only**
```batch
ONE_CLICK_BUILD_SINGLE_APP_WINDOWS.bat
```

**Option 3: Full Release (All 8 Phases)**
```batch
ONE_CLICK_FULL_RELEASE_WINDOWS.bat
```

### On Linux/macOS

```bash
chmod +x ONE_CLICK_START_LINUX_MAC.sh
./ONE_CLICK_START_LINUX_MAC.sh
```

Note: Windows artifacts cannot be built on Linux/macOS. Source will be complete but version_5_promotable will be false.

## Checking V5 Promotability

After running the full release, check:

```json
data/integration_tracker/v5_promotion_ledger.json
```

Look for:
```json
{
  "version_5_promotable": true,
  "blockers": []
}
```

- **true** = Ready for Version 5 final
- **false** = Blocked (check `blockers` array)

## What Blocks V5 Promotion?

These artifacts MUST exist and be valid:

1. `dist/ZenithStudio.exe` - Compiled Windows executable
2. `runtime/runtime_manifest.json` - Runtime configuration
3. `builds/installer/ZenithStudio_Setup.exe` - Windows installer
4. `logs/exe_smoke_test_report.json` - EXE functionality test

**Note:** These can only be generated on Windows with PyInstaller and NSIS installed.

## Evidence Files

The build process generates comprehensive evidence:

- `logs/canonical_mission_evidence.json` - Mission execution proof
- `logs/canonical_mission_report.md` - Human-readable mission report
- `logs/windows_artifact_proof.json` - Artifact existence proof
- `data/integration_tracker/tracker.json` - System completion tracking
- `data/integration_tracker/v5_promotion_ledger.json` - Final promotion decision

## Version 5 Final

Once `version_5_promotable` is true, the release can be named:

```
ZenithStudio Omega Version 5 Final
```

With no further changes or conditions.

## Key Design Principles

1. **No fake completion** - All proof gates are real
2. **Source vs. Artifact separation** - Source and Windows artifacts are tracked separately
3. **Honest promotion** - Version 5 is not declared unless all blockers are cleared
4. **Repeatable gates** - Every gate can be re-run from scratch
5. **Durable evidence** - All decisions are recorded in JSON/Markdown

## Next Steps

If running on Windows:

```batch
ONE_CLICK_FULL_RELEASE_WINDOWS.bat
```

Then check:

```
data/integration_tracker/v5_promotion_ledger.json
```

If all gates pass and `version_5_promotable` is true, Version 5 is ready.

---

**ZenithStudio Omega v4.8.0 — V5 Release Candidate**  
Source ready. Awaiting Windows artifact proof for Version 5 final.
