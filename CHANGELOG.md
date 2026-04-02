# Cosmos3D Changelog

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

