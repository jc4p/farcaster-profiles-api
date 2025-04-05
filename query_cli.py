#!/usr/bin/env python3
import sys
import argparse
import duckdb
import csv

def query_profile(fid=None, location=None, outfile=None):
    """
    Query the DuckDB database for user profiles and save to CSV.
    
    Args:
        fid (str): Optional FID to query by
        location (str): Optional location to query by
        outfile (str): Path to save CSV output
    """
    # Database path
    db_path = 'data/user_profiles.duckdb'
    
    # Connect to DuckDB
    conn = duckdb.connect(db_path, read_only=True)
    
    # Get column names for any query
    columns = conn.execute("SELECT * FROM user_profiles LIMIT 0").description
    column_names = [desc[0] for desc in columns]
    
    # Prepare result
    result = []
    
    if fid:
        # Query by FID (using the index)
        result = conn.execute("""
            SELECT * FROM user_profiles 
            WHERE Fid = ?
        """, [fid]).fetchall()
        
        if not result:
            print(f"No profile found with FID: {fid}")
            return
        
        # Print summary
        print(f"Found profile with FID: {fid}")
            
    elif location:
        # Query by location (using the index)
        result = conn.execute("""
            SELECT * FROM user_profiles 
            WHERE Location = ?
        """, [location]).fetchall()
        
        print(f"Found {len(result)} profiles in location: {location}")
        
    else:
        # Get all profiles (with limit for safety)
        result = conn.execute("""
            SELECT * FROM user_profiles
            LIMIT 10000
        """).fetchall()
        
        print(f"Exporting {len(result)} profiles (max 10000)")
    
    # Save to CSV
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(column_names)
        # Write data
        for row in result:
            writer.writerow(row)
    
    print(f"Data exported to {outfile}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query user profiles from DuckDB")
    parser.add_argument("--fid", type=str, help="FID to look up")
    parser.add_argument("--location", type=str, help="Location to filter by")
    parser.add_argument("--outfile", type=str, required=True, 
                        help="Output CSV file path (required)")
    
    args = parser.parse_args()
    
    if not (args.fid or args.location) and len(sys.argv) <= 2:
        parser.print_help()
    else:
        query_profile(args.fid, args.location, args.outfile)