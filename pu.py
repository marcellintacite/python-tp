import pynmea2

# Example GPGGA sentence (replace with your actual GPGGA sentence)
gpgga_sentence = "$GPGGA,075322.157,0230.399,S,02851.549,E,1,12,1.0,0.0,M,0.0,M,,*75"

# Parse the GPGGA sentence
gpgga_data = pynmea2.parse(gpgga_sentence)

# Extract relevant data
latitude = gpgga_data.latitude
longitude = gpgga_data.longitude
altitude = gpgga_data.altitude
fix_quality = gpgga_data.gps_qual

# Construct a custom GPSA sentence
gpsa_sentence = f"$GPSA,{latitude},{longitude},{altitude},{fix_quality}*checksum"

# Calculate the checksum for the new sentence (replace with actual checksum calculation)
checksum = 0x47  # Replace with the correct checksum value

# Add the checksum to the GPSA sentence
gpsa_sentence = f"{gpsa_sentence},{checksum:02X}"

print(gpsa_sentence)
