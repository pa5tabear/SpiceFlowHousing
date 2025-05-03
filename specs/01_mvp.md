# MVP – Ann Arbor Parcel-Screening CLI

## 1. Goal
Create a command-line tool that reads two raw GeoPackages—one for parcels, one for buildings—and produces:

* `desirable_parcels.kmz` (KMZ file ready for Google Earth)  
* `desirable_parcels.csv` (one row per parcel in the KMZ)

Filters such as zoning or lot-area will be added in future commits; v0 simply converts the data.

---

## 2. Inputs

* `--parcels`  <path>.gpkg  
  Raw Ann Arbor parcel polygons with attributes like owner name, street address, zoning, lot_area, etc.

* `--buildings`  <path>.gpkg  
  Raw Ann Arbor building footprints (passed through unchanged for now).

_No other inputs are handled in this version._

---

## 3. Outputs

1. **desirable_parcels.kmz**  
   * one folder called **“All Parcels (unfiltered)”**  
   * basic attributes exposed as Extended Data (parcel_id, lot_area, …)

2. **desirable_parcels.csv**  
   * one row for every parcel in the KMZ  
   * columns: parcel_id, owner_name, street_address, zoning, lot_area, plus any other fields copied verbatim from the parcel GeoPackage

_Note – filtering logic will be added in later commits once the core GeoPackage → KMZ + CSV workflow is stable._

---

## 4. User story
> *As an infill-development consultant I run a single command and instantly get a KMZ (for Google Earth) plus a CSV listing every parcel so I can review candidates offline.*

---

## 5. Acceptance Tests

| # | Scenario | Command (example) | Expected result |
|---|----------|-------------------|-----------------|
| 1 | **Basic run succeeds** | `python aa_parcel_cli.py --parcels sample_parcels.gpkg --buildings sample_buildings.gpkg --out desirable` | Exit code 0; files `desirable_parcels.kmz` and `desirable_parcels.csv` exist. |
| 2 | **CSV integrity** | (after test #1) | CSV has **≥ 1 row** and contains columns `parcel_id`, `owner_name`, `street_address`, `zoning`, `lot_area`. |
| 3 | **KMZ↔CSV consistency** | (after test #1) | Number of placemarks in KMZ equals number of rows in CSV. |
| 4 | **Idempotence** | Run the same command twice | Second run overwrites the two output files without error and produces identical file sizes (±1 byte). |

*(Tests 2 & 3 can be automated with `pytest`: unzip the KMZ with `zipfile`, count `<Placemark>` tags, and compare against `pandas.read_csv` row count.)*
