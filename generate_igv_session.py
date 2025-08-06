#!/usr/bin/env python3
"""
Script to generate IGV session XML files from a template.

This script takes a template XML file with Mustache-style variables and generates
instantiated XML files by replacing the variables with actual values for a family trio.

Usage:
    python generate_igv_session.py <father_id> <mother_id> <child_id> [--include-bam-tracks]

Examples:
    python generate_igv_session.py NA12877 NA12878 NA12881
    python generate_igv_session.py NA12877 NA12878 NA12881 --include-bam-tracks
"""

import sys
import argparse
import pystache


def generate_igv_session(father_id, mother_id, child_id, template_file="igv_session_template.xml", include_bam_tracks=False):
    """
    Generate an IGV session XML file from a template for a family trio.
    
    Args:
        father_id (str): The father's sample ID to substitute in the template
        mother_id (str): The mother's sample ID to substitute in the template
        child_id (str): The child's sample ID to substitute in the template
        template_file (str): Path to the template XML file
        include_bam_tracks (bool): Whether to include BAM tracks for each member
    
    Returns:
        str: Path to the generated XML file
    """
    # Generate output filename using the standard format
    output_file = f"{father_id}.{mother_id}.{child_id}.igv.xml"
    
    # Read the template file
    try:
        with open(template_file, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)
    
    # Prepare the context data for template rendering
    context = {
        'father_id': father_id,
        'mother_id': mother_id,
        'child_id': child_id,
        'include_bam_tracks': include_bam_tracks
    }
    
    # Render the template
    try:
        rendered_content = pystache.render(template_content, context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)
    
    # Write the output file
    try:
        with open(output_file, 'w') as f:
            f.write(rendered_content)
        print(f"Successfully generated IGV session file: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description="Generate IGV session XML files from a template for a family trio.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s NA12877 NA12878 NA12881
  %(prog)s NA12877 NA12878 NA12881 --include-bam-tracks
        """
    )
    
    parser.add_argument('father_id', help='The father\'s sample ID')
    parser.add_argument('mother_id', help='The mother\'s sample ID')
    parser.add_argument('child_id', help='The child\'s sample ID')
    parser.add_argument('--include-bam-tracks', action='store_true',
                       help='Include BAM tracks for each member of the trio')
    parser.add_argument('--template', default='igv_session_template.xml',
                       help='Path to the template XML file (default: igv_session_template.xml)')
    
    args = parser.parse_args()
    
    # Generate the IGV session file
    generated_file = generate_igv_session(
        args.father_id, 
        args.mother_id, 
        args.child_id, 
        template_file=args.template,
        include_bam_tracks=args.include_bam_tracks
    )
    
    # Print a summary
    print(f"\nSummary:")
    print(f"  Father ID: {args.father_id}")
    print(f"  Mother ID: {args.mother_id}")
    print(f"  Child ID: {args.child_id}")
    print(f"  Include BAM tracks: {args.include_bam_tracks}")
    print(f"  Output file: {generated_file}")
    print(f"  Template used: {args.template}")


if __name__ == "__main__":
    main() 