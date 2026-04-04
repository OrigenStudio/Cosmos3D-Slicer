# Cosmos3D Changelog

## v2.9.0 (2026-04-04)

### Fix wizard reopening every launch and printer not persisting (#23)

Fix two related bugs: the setup wizard opens every time the app launches, and the default printer selection is never saved.
### Root cause
`apply_config()` in `WebGuideDialog.cpp` sets vendor/printer/filament data into `app_config` in memory, but neither the wizard dialog nor the caller (`GUI_App::run_wizard()`) ever called `app_config->save()` afterward. On next launch, the config loaded without printer data → `only_default_printers()` returned true → wizard reopened.
### Fix
Add `app_config->save()` in two places:
- `WebGuideDialog::run()` — after `apply_config()` completes (belt)
- `GUI_App::run_wizard()` — after `wizard.run()` returns successfully (suspenders)

**Author:** @PolGuixe


## v2.8.0 (2026-04-03)

### Fix default printer selection and rename profile to 50 nozzle (#22)

Fix Cosmos3D printer not being selected as default on fresh install.
### Root cause
Two bugs in `PresetBundle.cpp`:
1. `ORCA_DEFAULT_PRINTER_MODEL` was `"Cosmos3D X1 60 nozzle"` (preset name) instead of `"Cosmos3D X1"` (printer_model field) — `find_system_preset_by_model_and_variant()` never matched
2. `ORCA_DEFAULT_PRINTER_VARIANT` was `"50"` but `printer_variant` was `"60"` — variant comparison also failed
### Fix
- Set `ORCA_DEFAULT_PRINTER_MODEL = "Cosmos3D X1"` and `ORCA_DEFAULT_PRINTER_VARIANT = "50"`
- Rename all profile references from "60 nozzle" to "50 nozzle" to match actual nozzle diameter
- Rename JSON files: `Cosmos3D X1 60 nozzle.json` → `Cosmos3D X1 50 nozzle.json`
- Update `printer_variant` from `"60"` to `"50"`

**Author:** @PolGuixe


## v2.7.0 (2026-04-02)

### Rebrand setup wizard: logos, text, and HTML fallbacks (#21)

- **Replace wizard logos**: `resources/web/image/logo.png` and `logo2.png` now show Cosmos3D icon instead of OrcaSlicer octopus
- **Fix wizard text**: Replace all "Orca Slicer" / "OrcaSlicer" references in `resources/web/data/text.js` across all 12+ languages (112 occurrences)
- **Fix HTML fallbacks**: Update hardcoded fallback text in wizard pages 1, 5, and 6
- **Classic wall generator**: Set default to "classic" instead of "arachne" for concrete printing

**Author:** @PolGuixe


## v2.6.0 (2026-04-02)

### Display weight in kg, classic wall generator, nozzle 50mm (#20)

- **Weight display in kg**: Convert material weight from grams to kilograms in all UI display points (sidebar, popup, plate data). Internal calculations and G-code comments remain in grams for backward compatibility
- **Classic wall generator**: Set default wall generator to "classic" instead of "arachne" — constant extrusion width is more suitable for concrete printing
- **Nozzle 50mm**: Default nozzle diameter changed from 60mm to 50mm
- **Force profile update**: Bumped vendor profile version to 02.02.00.00 with force_update to overwrite cached presets

**Author:** @PolGuixe


## v2.5.0 (2026-04-02)

### Config: default nozzle size 50mm (#19)

- Change default nozzle diameter from 60mm to 50mm across all Cosmos3D machine profiles
- Sync version bump (2.4.0) from main

**Author:** @PolGuixe


## v2.4.0 (2026-04-01)

### Cosmos3D: scarf joint defaults, UI renaming, and auto version bump (#18)

- **Scarf joint as default**: Added 150mm scarf joint seam settings to `fdm_process_common.json` (base) and concrete printing profile — all Cosmos3D process profiles inherit it
- **Rename Filament → Material**: All user-visible "Filament" labels replaced with "Material" (tab name, sidebar, preset type, G-code sections, object grid, AMS settings)
- **Rename bed type**: "Smooth High Temp Plate" → "Ground"
- **Auto version bump**: GitHub Action to bump minor version and generate changelog on every PR merge
### Scarf joint settings
| Setting | Value |
|---|---|
| `seam_slope_type` | `external` (contour) |
| `seam_slope_min_length` | `150` mm |
| `seam_slope_steps` | `10` |

**Author:** @PolGuixe

