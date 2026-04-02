# Cosmos3D Changelog

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

