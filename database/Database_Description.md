# Rent Hunting Database Description

## Database Overview

The **Rent Hunting Database** is designed to store and manage rental property information across the United States. This database serves as the central repository for a rental property search system that helps users find apartments, houses, and other rental properties based on their location, budget, and property specifications.

## Database Purpose

The database is designed to support:
- **Property Search**: Enable users to search for rental properties by location, price range, and property features
- **Rental Analytics**: Provide insights into rental market trends and pricing
- **Property Management**: Store comprehensive property details for rental listings
- **Booking and Scheduling**: Support appointment scheduling and customer relationship management
- **Multi-state Coverage**: Handle rental data from various states across the US

## Schema Design

### Main Table: `rent`

The core table stores rental property information with the following structure:

#### Column Specifications

| Column Name | Data Type | Description | Constraints |
|-------------|-----------|-------------|-------------|
| `id` | INT | Auto-incrementing primary key | PRIMARY KEY, AUTO_INCREMENT |
| `city` | VARCHAR(512) | State/City identifier (Note: contains state names, not city names in current data) | NOT NULL, INDEXED |
| `name` | VARCHAR(512) | Property name or address description | NOT NULL |
| `address` | VARCHAR(512) | Full property address | NOT NULL |
| `price` | VARCHAR(512) | Rental price (stored as text to handle ranges and special formatting) | NOT NULL |
| `bed_info` | VARCHAR(512) | Bedroom and bathroom information (e.g., "3 Beds, 2 Baths, 1,500 sq ft") | NULLABLE |
| `phone` | VARCHAR(512) | Contact phone number for the property | NULLABLE |
| `low_price` | BIGINT(20) | Minimum rental price as integer | NULLABLE, INDEXED |
| `high_price` | BIGINT(20) | Maximum rental price as integer | NULLABLE, INDEXED |


## Data Characteristics

### Data Volume
- **Total Records**: ~9,139 rental properties
- **File Size**: Approximately 2.1 MB in CSV format
- **Geographic Distribution**: Heavy concentration in Colorado Springs, CO and Florida locations

### Property Types
Properties include:
- **Apartments**: Studio to 5+ bedroom units
- **Houses**: Single-family rental homes
- **Townhomes**: Multi-level rental properties
- **Condos**: Condominium rentals
- **Luxury Properties**: High-end rental units
