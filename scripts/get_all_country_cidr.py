import mysql.connector
import os

# Database configuration
db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}

# Folder to save CIDR files
output_folder = 'cidr_country'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Define the query to get unique country names
query_unique_countries = "SELECT DISTINCT country_name FROM tbl_city_locations_en;"

# Execute the query to get unique country names
cursor.execute(query_unique_countries)
unique_country_names = cursor.fetchall()

# Loop through each unique country name
for country in unique_country_names:
    country_name = country[0]
    print(f" [+] Processing country: {country_name}")
    #
    # Define the query to get all network values for the current country
    query_networks = f"""
    SELECT network FROM tbl_city_blocks_ipv4 
    WHERE geoname_id IN (
        SELECT geoname_id FROM tbl_city_locations_en WHERE country_name = '{country_name}'
    );
    """
    #
    # Execute the query to get network values
    cursor.execute(query_networks)
    networks = cursor.fetchall()
    #
    # Prepare to write to the country-specific CIDR file
    sanitized_country_name = country_name.lower().replace(' ', '_')
    cidr_file_path = os.path.join(output_folder, f"{sanitized_country_name}.cidr")
    with open(cidr_file_path, 'w') as cidr_file:
        # Write each network value to the file
        for network in networks:
            cidr_file.write(f"{network[0]}\n")

# Close the cursor and connection
cursor.close()
conn.close()

print(" [+] Processing complete. CIDR files have been created.")
