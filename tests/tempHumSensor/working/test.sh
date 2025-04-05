# Wake up the sensor (SLA+W)
echo "Waking up sensor..."
sudo i2cset -y 1 0x5c 0x00 c

# Small delay
sleep 0.001

# Send read command: Function code 0x03, start address 0x00, number of registers 0x04
echo "Sending read command..."
sudo i2cset -y 1 0x5c 0x03 0x00 0x04 i

# Small delay
sleep 0.002

# Read the response and convert to readable values
echo "Reading sensor data..."
RAW_DATA=$(sudo i2cget -y 1 0x5c 0x00 i 8)
echo "Raw data: $RAW_DATA"

# Extract bytes from raw data
FUNCTION_CODE=$(echo $RAW_DATA | cut -d' ' -f1 | sed 's/0x//')
DATA_LEN=$(echo $RAW_DATA | cut -d' ' -f2 | sed 's/0x//')
HUMIDITY_HIGH=$(echo $RAW_DATA | cut -d' ' -f3 | sed 's/0x//')
HUMIDITY_LOW=$(echo $RAW_DATA | cut -d' ' -f4 | sed 's/0x//')
TEMP_HIGH=$(echo $RAW_DATA | cut -d' ' -f5 | sed 's/0x//')
TEMP_LOW=$(echo $RAW_DATA | cut -d' ' -f6 | sed 's/0x//')

#echo "Function code: $FUNCTION_CODE"
#echo "Data length: $DATA_LEN"
#echo "Humidity high byte: $HUMIDITY_HIGH"
#echo "Humidity low byte: $HUMIDITY_LOW"
#echo "Temperature high byte: $TEMP_HIGH"
#echo "Temperature low byte: $TEMP_LOW"

# Convert hex to decimal using printf
HUMIDITY_HIGH_DEC=$(printf "%d" "0x$HUMIDITY_HIGH")
HUMIDITY_LOW_DEC=$(printf "%d" "0x$HUMIDITY_LOW")
TEMP_HIGH_DEC=$(printf "%d" "0x$TEMP_HIGH")
TEMP_LOW_DEC=$(printf "%d" "0x$TEMP_LOW")

HUMIDITY_DEC=$((HUMIDITY_HIGH_DEC * 256 + HUMIDITY_LOW_DEC))
TEMP_DEC=$((TEMP_HIGH_DEC * 256 + TEMP_LOW_DEC))

# Calculate actual values (divide by 10 using awk since bc may not be available)
HUMIDITY=$(awk "BEGIN {printf \"%.1f\", $HUMIDITY_DEC/10}")
TEMPERATURE=$(awk "BEGIN {printf \"%.1f\", $TEMP_DEC/10}")

echo "Temperature: ${TEMPERATURE}°C"
echo "Humidity: ${HUMIDITY}%"