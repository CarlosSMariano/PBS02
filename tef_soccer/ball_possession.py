import paho.mqtt.client as mqtt
import os
from math import radians, cos, sqrt

# MQTT Broker configuration parameters
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", 'mosquitto')  # Broker IP/hostname with fallback to 'mosquitto'
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))    # Broker port number with fallback to 1883
KeepAliveBroker = 60  # Keep-alive interval in seconds for broker connection

# Current state dictionary storing device positions and metadata
CURRENT_STATE = {
    '/TEF/device/b': {'lat': None, 'lon': None},  # Ball device with latitude/longitude
    '/TEF/device/sc': {'lat': None, 'lon': None, 'team': None, 'soccer_name': None}  # Soccer player device
}

d_tolerance = 2  # Distance tolerance in meters for proximity detection

def euclidiane_distance(lat_a, lon_a, lat_b, lon_b):
    """
    Calculate Euclidean distance between two geographic coordinates in meters.
    Uses approximation for converting latitude/longitude differences to meters.
    
    Args:
        lat_a (float): Latitude of point A
        lon_a (float): Longitude of point A  
        lat_b (float): Latitude of point B
        lon_b (float): Longitude of point B
    
    Returns:
        float: Distance between points in meters
    """
    
    # Constants and mean latitude calculation
    c_lat = 111320  # Latitude conversion constant (approximate value at equator)

    lat_media = (lat_a + lat_b) / 2  # Mean latitude
    lat_media_rad = radians(lat_media)  # Convert to radians
    cos_lat_media = cos(lat_media_rad)  # Cosine of mean latitude

    # Longitude calculation in meters
    d_lon = lon_b - lon_a  # Longitude difference
    c_lon = c_lat * cos_lat_media  # Longitude conversion factor
    m_lon = d_lon * c_lon  # East-West distance in meters

    # Latitude calculation in meters
    d_lat = lat_b - lat_a  # Latitude difference
    m_lat = d_lat * c_lat  # North-South distance in meters

    # Final distance calculation using Pythagorean theorem
    d_metros = sqrt((m_lat)**2 + (m_lon)**2)

    return d_metros

def split_payload(position):
    """
    Parse and split MQTT payload containing position data.
    
    Args:
        position (str): Comma-separated string with coordinates and optional metadata
    
    Returns:
        tuple: Parsed coordinates and optional team/name data
    
    Raises:
        ValueError: If position format is invalid or coordinates are not numeric
    """
    # Clean the input string
    position = position.strip()
    position = position.replace('"', '').replace("'", "") 
    position = position.replace('−', '-')  # Handle different minus sign characters
    
    # Split into parts and strip whitespace
    parts = [p.strip() for p in position.split(',')]

    try: 
        # Extract and convert latitude and longitude
        lat_ref = float(parts[0])
        lon_ref = float(parts[1])
    except (ValueError, IndexError):
        print(f"[ERROR PARSE] Invalid Payload (coordinate numbers): {position}")
        return None
    
    # Handle soccer player payload (4 parts: lat, lon, team, name)
    if len(parts) == 4: 
        team_ref = parts[2]
        soccer_name_ref = parts[3]

        # Handle empty team or name values
        if not team_ref:
            team_ref = None
        if not soccer_name_ref: 
            soccer_name_ref = None

        return lat_ref, lon_ref, team_ref, soccer_name_ref
    
    # Handle ball payload (2 parts: lat, lon only)
    elif len(parts) == 2: 
        return lat_ref, lon_ref
    
    else: 
        print(f"[ERROR PARSE] Invalid number of parts ({len(parts)}) in '{position}'")
        return None

def on_connect(client, userdata, flags, rc):
    """
    Callback function executed when connecting to the MQTT broker.
    
    Args:
        client: MQTT client instance
        userdata: User-defined data
        flags: Response flags from broker
        rc: Result code (0 = success)
    """
    if rc == 0:
        print("[STATUS] Successfully connected to BROKER")
        # Subscribe to all topics defined in CURRENT_STATE
        for topics in CURRENT_STATE.keys():
            client.subscribe(topics)
    else: 
        print(f"[STATUS] Connection failed: {rc}")

def update_state(topic, payload):
    """
    Update the current state dictionary with new position data.
    
    Args:
        topic (str): MQTT topic that received the message
        payload (str): Message payload containing position data
    """
    global CURRENT_STATE

    data = split_payload(payload)

    if data is None: 
        return
    
    # Update ball position
    if topic == '/TEF/device/b' and len(data) == 2:
        CURRENT_STATE[topic]['lat'] = data[0]
        CURRENT_STATE[topic]['lon'] = data[1]
        print(f"[BALL] Update position: '{data[0]}, {data[1]}'")
    # Update soccer player position and metadata
    elif topic == '/TEF/device/sc' and len(data) == 4: 
        CURRENT_STATE[topic]['lat'] = data[0]
        CURRENT_STATE[topic]['lon'] = data[1]
        CURRENT_STATE[topic]['team'] = data[2]
        CURRENT_STATE[topic]['soccer_name'] = data[3]
        print(f"[SOCCER] Update position: '{data[0]},{data[1]}'")

def on_message(client, userdata, msg):
    """
    Callback function executed when a message is received from subscribed topics.
    
    Args:
        client: MQTT client instance
        userdata: User-defined data
        msg: Message object containing topic and payload
    """
    
    topic = msg.topic
    try: 
        # Update system state with new message data
        update_state(topic, msg.payload.decode('utf8'))
    except Exception as e:
        print(f"[GENERAL ERROR] Failed to process message payload: {topic}: {e}")
        return

    # Extract current positions from state
    ball_lat = CURRENT_STATE['/TEF/device/b']['lat']
    ball_lon = CURRENT_STATE['/TEF/device/b']['lon']
    soccer_lat = CURRENT_STATE['/TEF/device/sc']['lat']
    soccer_lon = CURRENT_STATE['/TEF/device/sc']['lon']
    soccer_team = CURRENT_STATE['/TEF/device/sc']['team']
    soccer_name = CURRENT_STATE['/TEF/device/sc']['soccer_name']
    
    # Check if all required fields have valid data
    campos_check = [ball_lat, ball_lon, soccer_lat, soccer_lon, soccer_team, soccer_name]
    
    if all(campos_check):
        try:
            # Calculate distance between ball and soccer player
            distance = euclidiane_distance(ball_lat, ball_lon, soccer_lat, soccer_lon)

            # If player is close enough to the ball, publish event
            if distance <= d_tolerance:
                payload = f"{soccer_team}, {soccer_name}"
                client.publish(f"/TEF/application/last_touch", payload)
                print(f"[DETECTED POSSESSION] Soccer player: {soccer_name} from {soccer_team}")
        except (ValueError, TypeError) as e: 
            print(f"[MATH ERROR] Failed to convert or calculate distance: {e}")

# Create MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect  
client.on_message = on_message  

try:
    # Connect to broker and start listening
    print(f"[CONNECTION] Trying to connect to {BROKER_ADDRESS}:{BROKER_PORT}...")
    client.connect(BROKER_ADDRESS, BROKER_PORT, KeepAliveBroker)
    print("[STATUS] Connection established. Starting loop...")
    client.loop_forever()  # Start infinite loop to process messages
    
except Exception as e: 
    # Handle critical connection errors
    print(f"[CRITICAL CONNECTION ERROR] Failed to connect: {e}")
    exit()