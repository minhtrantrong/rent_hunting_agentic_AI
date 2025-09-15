#!/usr/bin/env python3
"""
Quick Database Connection Test
==============================

A simple, lightweight program to quickly test database connectivity
and run basic queries.
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

def quick_test():
    """Quick database connection and query test."""
    print("🚀 Quick Database Connection Test")
    print("=" * 40)
    
    # Connection config
    config = {
        'host': os.getenv("TIDB_HOST"),
        'user': os.getenv("TIDB_USER"),
        'password': os.getenv("TIDB_PASSWORD"),
        'database': os.getenv("TIDB_DATABASE"),
        'autocommit': True
    }
    
    # Check environment variables
    if not all(config.values()):
        print("❌ Missing database configuration in environment variables")
        return False
    
    connection = None
    cursor = None
    
    try:
        # Test connection
        print("🔄 Connecting...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        print("✅ Connected successfully!")
        
        # Test basic query
        print("\n📊 Testing basic query...")
        cursor.execute("SELECT COUNT(*) FROM rents")
        count = cursor.fetchone()[0]
        print(f"✅ Found {count:,} records in rents table")
        
        # Test search query
        print("\n🔍 Testing search query...")
        cursor.execute("SELECT city, name, price FROM rents WHERE city LIKE '%California%' LIMIT 2")
        results = cursor.fetchall()
        
        if results:
            print(f"✅ Search test successful - found {len(results)} results:")
            for city, name, price in results:
                print(f"   • {name} - ${price}")
        else:
            print("⚠️  No California results, trying another state...")
            cursor.execute("SELECT city, name, price FROM rents LIMIT 2")
            results = cursor.fetchall()
            if results:
                city, name, price = results[0]
                print(f"✅ Alternative search successful: {name} in {city} - ${price}")
        
        print("\n🎉 All tests passed! Database is working correctly.")
        return True
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        # Clean up
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("🔒 Connection closed.")

if __name__ == "__main__":
    success = quick_test()
    exit(0 if success else 1)