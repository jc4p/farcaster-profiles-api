#!/usr/bin/env python3
import os
import json
import re
import duckdb
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database path
DB_PATH = 'data/user_profiles.duckdb'

@app.route('/fid/<fid>', methods=['GET'])
def get_by_fid(fid):
    """Get profile by FID using URL path parameter"""
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    try:
        result = conn.execute("""
            SELECT * FROM user_profiles 
            WHERE Fid = ?
        """, [fid]).fetchall()
        
        if not result:
            return jsonify({"error": f"No profile found with FID: {fid}"}), 404
        
        # Get column names
        columns = [desc[0] for desc in conn.description]
        
        # Convert to dictionary
        profile = dict(zip(columns, result[0]))
        
        return jsonify(profile)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/location', methods=['GET'])
def get_by_location():
    """Get profiles by location using lat/lon parameters"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Missing 'lat' or 'lon' parameters"}), 400
    
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    try:
        # Convert to float and format with 2 decimal places to match database format
        lat_float = float(lat)
        lon_float = float(lon)
        formatted_lat = f"{lat_float:.2f}"
        formatted_lon = f"{lon_float:.2f}"
        
        # Format expected in database: geo:34.05,-118.24
        location_pattern = f"geo:{formatted_lat},{formatted_lon}"
        
        # Try exact match first
        result = conn.execute("""
            SELECT * FROM user_profiles 
            WHERE Location = ?
        """, [location_pattern]).fetchall()
        
        # If no exact match, try nearby locations
        if not result:
            # Query for locations near the specified coordinates
            result = conn.execute("""
                SELECT * FROM user_profiles 
                WHERE Location LIKE 'geo:%' 
                LIMIT 5
            """).fetchall()
            
            # Extract sample location to check format
            if result:
                columns = [desc[0] for desc in conn.description]
                sample = dict(zip(columns, result[0]))
                print(f"Sample location format: {sample.get('Location')}")
                
                # Try again with proper formatting based on sample
                if sample.get('Location'):
                    # Get more precise match using database formatting
                    result = conn.execute("""
                        SELECT * FROM user_profiles 
                        WHERE Location LIKE ?
                    """, [f"geo:{formatted_lat}%{formatted_lon}%"]).fetchall()
        
        if not result:
            return jsonify({"error": f"No profiles found with location near lat:{formatted_lat}, lon:{formatted_lon}"}), 404
        
        # Get column names
        columns = [desc[0] for desc in conn.description]
        
        # Convert all results to dictionaries
        profiles = []
        for row in result:
            profile = dict(zip(columns, row))
            profiles.append(profile)
        
        return jsonify(profiles)
        
    except ValueError:
        return jsonify({"error": "Invalid lat/lon format. Please provide numeric values."}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        conn.close()

@app.route('/', methods=['GET'])
def home():
    """API info"""
    return jsonify({
        "name": "User Profiles API",
        "endpoints": [
            {"path": "/fid/<fid>", "description": "Get profile by FID"},
            {"path": "/location", "params": ["lat", "lon"], "description": "Get profiles by location coordinates"}
        ],
        "examples": [
            {"url": "/fid/977233", "description": "Get profile with FID 977233"},
            {"url": "/location?lat=34.05&lon=-118.24", "description": "Get profiles near Los Angeles"}
        ]
    })

if __name__ == "__main__":
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        print("Run parse_parquet.py first to create the database")
        exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)