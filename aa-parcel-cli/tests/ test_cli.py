from pathlib import Path
import subprocess
import zipfile
import pandas as pd

FIXTURES = Path(__file__).parent / "fixtures"
PARCELS = FIXTURES / "parcels_mini.gpkg"
BUILDINGS = FIXTURES / "buildings_mini.gpkg"
OUT_DIR = Path(__file__).parent / "out"
OUT_DIR.mkdir(exist_ok=True)

def test_basic_run(tmp_path):
    kmz = tmp_path / "desirable_parcels.kmz"
    csv = tmp_path / "desirable_parcels.csv"

    # CLI call
    result = subprocess.run(
        [
            "python",
            "-m",
            "aa_parcel_cli.cli",
            "--parcels",
            str(PARCELS),
            "--buildings",
            str(BUILDINGS),
            "--out",
            str(tmp_path / "desirable"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    # files exist
    assert kmz.exists()
    assert csv.exists()

    # CSV has expected rows/columns
    df = pd.read_csv(csv)
    assert set(df.columns) >= {
        "parcel_id",
        "owner_name",
        "street_address",
        "zoning",
        "lot_area",
    }
    assert len(df) == 3  # same as fixture

    # KMZ has same number of placemarks
    with zipfile.ZipFile(kmz) as z:
        kml_text = z.read("doc.kml").decode()
    assert kml_text.count("<Placemark") == 3
