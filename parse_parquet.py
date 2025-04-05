#!/usr/bin/env python3
import os
import duckdb

def parse_parquet_to_duckdb():
    """
    Load the parquet file and save as a compressed DuckDB file 
    with indexes on Fid and Location.
    """
    # Input and output paths
    parquet_path = 'data/user_profiles_04_05_2025.parquet'
    duckdb_path = 'data/user_profiles.duckdb'
    
    # Create connection to DuckDB
    conn = duckdb.connect(duckdb_path)
    
    # Create and load table from parquet
    conn.execute("""
        CREATE TABLE user_profiles AS 
        SELECT * FROM read_parquet(?)
    """, [parquet_path])
    
    # Create indexes to speed up queries
    conn.execute("CREATE INDEX idx_fid ON user_profiles(Fid)")
    conn.execute("CREATE INDEX idx_location ON user_profiles(Location)")
    
    # Enable compression for the database
    conn.execute("PRAGMA force_compression='zstd'")
    
    # Checkpoint to ensure data is saved with compression
    conn.execute("CHECKPOINT")
    
    # Close connection
    conn.close()
    
    # Print size info
    parquet_size = os.path.getsize(parquet_path) / (1024 * 1024)
    duckdb_size = os.path.getsize(duckdb_path) / (1024 * 1024)
    
    print(f"Parquet file size: {parquet_size:.2f} MB")
    print(f"DuckDB file size: {duckdb_size:.2f} MB")
    print(f"DuckDB created at {duckdb_path} with indexes on Fid and Location")

if __name__ == "__main__":
    parse_parquet_to_duckdb()