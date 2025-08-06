# IGV Session XML Template Generator for Family Trios

This project provides a template-based approach to generate IGV session XML files for family trios (father, mother, child) with customizable sample IDs. The generator supports both basic methylation and haplotype tracks, as well as optional BAM alignment tracks for each family member.

## Files

- `igv_session_template.xml` - Template XML file using Mustache notation with `{{father_id}}`, `{{mother_id}}`, and `{{child_id}}` variables
- `generate_igv_session.py` - Python script to generate instantiated XML files for family trios
- `requirements.txt` - Python dependencies

## Installation

1. Install the required Python package:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Generate an IGV session file for a family trio with methylation and haplotype tracks only:
```bash
python generate_igv_session.py NA12877 NA12878 NA12881
```

### With BAM Tracks

Generate an IGV session file that includes BAM alignment tracks for each member of the trio:
```bash
python generate_igv_session.py NA12877 NA12878 NA12881 --include-bam-tracks
```

### Custom Template

Use a custom template file:
```bash
python generate_igv_session.py NA12877 NA12878 NA12881 --template my_custom_template.xml
```

### Output File Naming

The script automatically generates output files using the format `father_id.mother_id.child_id.igv.xml`. For example, the command above will create `NA12877.NA12878.NA12881.igv.xml`.

### Programmatic Usage

You can also use the script programmatically:

```python
from generate_igv_session import generate_igv_session

# Generate session file for a family trio (methylation and haplotype tracks only)
generate_igv_session("NA12877", "NA12878", "NA12881")

# Generate session file with BAM tracks included
generate_igv_session("NA12877", "NA12878", "NA12881", include_bam_tracks=True)
```

## Template Variables

The template uses the following Mustache-style variables:

- `{{father_id}}` - The father's sample identifier (e.g., NA12891)
- `{{mother_id}}` - The mother's sample identifier (e.g., NA12892)
- `{{child_id}}` - The child's sample identifier (e.g., NA12878)
- `{{include_bam_tracks}}` - Boolean flag to conditionally include BAM tracks

## XML Structure

The generated IGV session includes:

### Resources Section
- **Basic tracks (always included):**
  - 4 resources per sample (12 total):
    - DNA methylation founder-phased paternal bigWig
    - DNA methylation founder-phased maternal bigWig
    - Haplotype map blocks paternal BED (with index)
    - Haplotype map blocks maternal BED (with index)

- **BAM tracks (optional, when --include-bam-tracks is used):**
  - 3 additional resources (1 per sample):
    - Haplotagged BAM file with index for each family member

### Data Panel
- **Basic tracks (always included):**
  - 6 tracks total (2 per sample):
    - DNA methylation founder-phased paternal bigWig for each family member
    - DNA methylation founder-phased maternal bigWig for each family member

### BAM Panels (optional)
- **When --include-bam-tracks is used:**
  - 2 panels (1 per family member), each containing:
    - Coverage track
    - Alignment track with haplotype-aware rendering options

### Feature Panel
- **Basic tracks (always included):**
  - 8 tracks total (2 per sample + 2 reference tracks):
    - Reference sequence track
    - Refseq Select track
    - Haplotype map blocks paternal BED for each family member
    - Haplotype map blocks maternal BED for each family member

## BAM Track Features

When BAM tracks are included, each family member gets their own panel with:

- **Coverage visualization** with auto-scaling
- **Alignment visualization** with haplotype-aware features:
  - Color coding by phase set (PS tag)
  - Grouping by haplotype (HP tag)
  - Filter read duplicates
  - Small indel filtering

## Dependencies

- Python 3.6+
- pystache>=0.6.0 