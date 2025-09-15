# Step-by-Step Guide: Importing CSV Data to TiDB Cloud

This guide provides detailed instructions for importing the rent hunting CSV data to TiDB Cloud using the web console interface.

## Prerequisites

Before starting the import process, ensure you have:

✅ **TiDB Cloud Account**: Active TiDB Cloud subscription  
✅ **CSV File**: Access to `rents.csv` file (9,139 records, ~2.1 MB)  
✅ **Database Access**: Appropriate permissions to create tables and import data  
✅ **Internet Connection**: Stable connection for file upload  

## Step 1: Access TiDB Cloud Console

### 1.1 Login to TiDB Cloud
1. Navigate to [https://tidbcloud.com](https://tidbcloud.com)
2. Click **"Sign In"** in the top right corner
3. Enter your credentials and authenticate
4. You'll be redirected to the TiDB Cloud dashboard

### 1.2 Select Your Cluster
1. From the dashboard, locate your target cluster
2. Click on the **cluster name** to access cluster details (Create a new cluster if one doesn't already exist.)
3. Ensure the cluster status shows **"Active"** (green indicator)
4. Note the cluster connection details for reference

## Step 2: Prepare for Data Import

### 2.1 Access Import Interface
1. In your cluster dashboard, click **"Connect"** to get connection details (save these for later application setup)
2. Navigate to the **"Data Import"** or **"Import Data"** section
3. Choose **"Import your own data"** option
4. Select **"Upload a local file"** option

## Step 3: Upload and Configure CSV File

### 3.1 Select and Upload File
1. Click **"Choose File"** or **"Browse"** button  
2. Navigate to your project's `database` folder
3. Select the `rents.csv` file (should show ~2.1 MB size, 9,139 records)
4. Click **"Open"** to select the file
5. Wait for the file upload to complete

### 3.2 Configure Database and Table
1. **Database Name**: Create or select database (e.g., `hackathon_rent_db`)
2. **Table Name**: Enter table name (e.g., `rent`)
3. **Import Mode**: Select "Create new table" if table doesn't exist

## Step 4: Define Table Schema

### 4.1 Column Mapping and Data Types
Configure the following column definitions based on your CSV structure:

| CSV Column | Database Column | Data Type | Constraints | Notes |
|------------|----------------|-----------|-------------|--------|
| `city` | `city` | VARCHAR(512) | NOT NULL, INDEXED | State identifier (contains state names) |
| `name` | `name` | VARCHAR(512) | NOT NULL | Property name or description |
| `address` | `address` | VARCHAR(512) | NOT NULL | Full property address |
| `price` | `price` | VARCHAR(512) | NOT NULL | Price as text (handles ranges/formats) |
| `bed_info` | `bed_info` | VARCHAR(512) | NULLABLE | Bedroom/bathroom/sqft information |
| `phone` | `phone` | VARCHAR(512) | NULLABLE | Contact phone number |
| `low_price` | `low_price` | BIGINT(20) | NULLABLE, INDEXED | Minimum price (numeric) |
| `high_price` | `high_price` | BIGINT(20) | NULLABLE, INDEXED | Maximum price (numeric) |

### 4.2 Advanced Configuration
1. **Character Set**: UTF-8 (default)
2. **Field Delimiter**: Comma (,)
3. **Text Qualifier**: Double quotes (")
4. **Header Row**: Yes (first row contains column names)

## Step 5: Execute Import

### 5.1 Preview and Validate
1. Click **"Preview Data"** to review the first 10-20 rows
2. Verify column mapping is correct
3. Check data formatting and types
4. Ensure no critical data appears truncated

### 5.2 Start Import Process
1. Review all settings one final time
2. Click **"Start Import"** or **"Import Data"**
3. Monitor the import progress bar
4. Wait for completion confirmation from TiDB

## Step 6: Verify Import Success

### 6.1 Check Import Status
1. Wait for the import completion message
2. Review any warnings or error messages
3. Note the number of records successfully imported (should be 9,139)
4. Check for any failed or skipped records

### 6.2 Data Validation
Execute these validation checks in the TiDB console:

```sql
-- Check total record count
SELECT COUNT(*) FROM rent;

-- Verify data distribution by state
SELECT city, COUNT(*) as property_count 
FROM rent 
GROUP BY city 
ORDER BY property_count DESC 
LIMIT 10;

-- Check price range validity
SELECT MIN(low_price), MAX(high_price), AVG(low_price) 
FROM rent 
WHERE low_price IS NOT NULL;

-- Sample data review
SELECT * FROM rent LIMIT 5;
```

### 6.3 Data Quality Verification
Verify the following in your imported data:
- ✅ **Record Count**: Exactly 9,139 records imported
- ✅ **State Data**: State names appear in `city` column (Alabama, Colorado, Florida, etc.)
- ✅ **Property Names**: Complete property names/addresses in `name` column  
- ✅ **Addresses**: Full addresses in `address` column
- ✅ **Price Data**: Price information in both text and numeric formats
- ✅ **Property Details**: Bedroom/bathroom info formatted properly
- ✅ **Contact Info**: Phone numbers present where available (some may be empty)
- ✅ **Numeric Prices**: Valid price ranges in `low_price` and `high_price` columns

## Step 7: Post-Import Configuration

### Get Connection Information
1. Navigate to your cluster's **"Connect"** section
2. Copy the connection string, hostname, port, and credentials
3. Note the database name you created
4. Save these details for application configuration