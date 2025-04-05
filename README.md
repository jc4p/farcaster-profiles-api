# FC Profiles Data

A Python toolkit for processing, querying, and serving Farcaster user profile data.

## Overview

This repository contains tools for working with Farcaster user profile data:

- **Data Processing**: Convert Parquet data to indexed DuckDB (faster queries)
- **CLI Query Tool**: Look up profiles by FID or location
- **REST API**: Serve profile data via HTTP endpoints

## Data Source and Usage Restrictions

This repository contains **PUBLIC** data from the Farcaster protocol, collected as of April 5, 2025. 

**Important Usage Notes**:
- All data included is already publicly available through the Farcaster protocol
- This data should only be used for legitimate, non-harmful purposes
- Do NOT use this data for spam, harassment, surveillance, or any malicious activities
- Be respectful of users' privacy despite the public nature of this data
- The data is provided as-is with no guarantees of accuracy or completeness

## Project Structure

```
fc-profiles-data/
├── data/
│   ├── user_profiles_04_05_2025.parquet  # Original data (update instructions below)
│   └── user_profiles.duckdb              # Generated database (update with parse_parquet.py)
├── parse_parquet.py    # Data conversion script (already run)
├── query_cli.py        # CLI tool for queries
├── api.py              # REST API server
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

## Files Description

### parse_parquet.py

**Purpose**: Converts Parquet data to indexed DuckDB format  
**Note**: This script has already been run. You don't need to run it again unless you receive updated data files.

```python
# If you need to re-process data:
python parse_parquet.py
```

The script:
1. Loads the Parquet file from `data/user_profiles_04_05_2025.parquet`
2. Creates a DuckDB database with the same data
3. Adds indexes on `Fid` and `Location` fields for faster queries
4. Applies compression for smaller file size
5. Saves to `data/user_profiles.duckdb`

### query_cli.py

**Purpose**: Command-line tool to query profile data

```python
# Query by FID
python query_cli.py --fid 977233 --outfile results.csv

# Query by location
python query_cli.py --location --lat 34.05 --lon -118.24 --outfile results.csv
```

Key features:
- Exports results to CSV (UTF-8 encoded)
- Uses the indexed DuckDB database for fast queries
- Requires `--outfile` parameter to specify where to save the CSV

### api.py

**Purpose**: REST API server for profile data

```python
# Start the API server
python api.py
```

The server runs on http://0.0.0.0:5000/ and provides these endpoints:

- **GET /** - API information and documentation
- **GET /fid/{fid}** - Get profile by FID (e.g., `/fid/977233`)
- **GET /location?lat={lat}&lon={lon}** - Get profiles by location coordinates (e.g., `/location?lat=34.05&lon=-118.24`)

All responses are in JSON format.

## Data Schema

User profiles contain these fields:
- `Fid`: Unique identifier (string)
- `Username`: User handle
- `Display`: Display name
- `Location`: Geographic coordinates in format `geo:lat,lon`
- `Pfp`: Profile picture URL
- `Bio`: User biography text
- `Twitter`: Twitter/X handle

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage Examples

### CLI Query Tool

```bash
# Export a specific profile to CSV
python query_cli.py --fid 977233 --outfile user.csv

# Find profiles at a location
python query_cli.py --location --lat 34.05 --lon -118.24 --outfile la_users.csv
```

### REST API

Start the server:
```bash
python api.py
```

Example API requests:

```bash
# Get API information
curl http://localhost:5000/

# Get profile by FID
curl http://localhost:5000/fid/977233

# Get profiles by location
curl http://localhost:5000/location?lat=34.05&lon=-118.24
```

## Dependencies

- duckdb==1.2.1
- flask>=2.0.0

## Notes

- The DuckDB database is optimized for read operations with indexes
- All CSV exports are UTF-8 encoded to preserve special characters
- The API caches database connections for performance

## Updating the Data

The profile data included in this repository is a snapshot from April 5, 2025. If you want to update with fresh data:

1. Set up a Farcaster Hub (follow Farcaster documentation)
2. Use [fast-hub-client](https://github.com/jc4p/fast-hub-client/) to fetch current data:
   ```bash
   git clone https://github.com/jc4p/fast-hub-client.git
   cd fast-hub-client/HubClient/HubClient.Production
   dotnet run --profiles
   ```
3. Generate a new Parquet file:
   ```bash
   cd ../../scripts
   ./export_cleaned_profiles.sql
   ```
4. Replace the existing Parquet file in the `data` directory
5. Run `parse_parquet.py` to update the DuckDB database:
   ```bash
   python parse_parquet.py
   ```

This will provide you with the most current Farcaster user profile data available.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The code and software in this repository are MIT licensed, but please note that:
1. The Farcaster user data itself is subject to Farcaster's terms and protocols
2. This is not an official Farcaster project
3. Using this data in a way that violates Farcaster's terms of service may result in action from Farcaster
4. Please please please don't use this for any unethical purposes