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
    '/TEF/device/g': {'lat': None, 'lon': None},  # Goal device with latitude/longitude
    '/TEF/application/last_touch': {'team': None, 'soccer_name': None}  # Last soccer player that touched the ball
}

d_tolerance = 1  # Distance tolerance in meters for goal detection

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

def parse_coordinates(position):
    """
    Parse coordinate data from MQTT payload.
    
    Args:
        position (str): String containing latitude and longitude coordinates
    
    Returns:
        tuple: Parsed latitude and longitude as floats
    
    Raises:
        ValueError: If coordinate format is invalid
    """
    # Clean the input string
    position = position.strip()
    position = position.replace('"', "").replace("'", '')
    position = position.replace('−', '-')  # Handle different minus sign characters

    # Split into parts and strip whitespace
    parts = [p.strip() for p in position.split(',')]

    # Validate format - must have exactly 2 parts (lat, lon)
    if len(parts) != 2 : 
        raise ValueError("Invalid coordinates format!")
    
    try: 
        # Extract and convert latitude and longitude
        lat_ref = float(parts[0].strip())
        lon_ref = float(parts[1].strip())
        return lat_ref, lon_ref
    except (ValueError, IndexError):
        print(f"[ERROR COORDINATES PARSE] Invalid Payload: {position}")
        return None

def parse_metadata(data):
    """
    Parse metadata from last_touch payload.
    
    Args:
        data (str): String containing team and player name
    
    Returns:
        tuple: Parsed team and player name
    
    Raises:
        ValueError: If metadata format is invalid
    """
    parts = data.split(',')

    # Validate format - must have exactly 2 parts (team, name)
    if len(parts) != 2 : 
        raise ValueError("Invalid metadata format!")

    try: 
        # Extract team and player name
        team = parts[0].strip()
        name = parts[1].strip()
    except (ValueError, IndexError):
        print(f"[ERROR METADATA PARSE] Invalid Payload: {data}")
        return None
    
    # Handle empty values
    if not team: team = None
    if not name: name = None

    return team, name

def on_connect(client, userdata, flags, rc):
    """
    Callback function executed when connecting to MQTT broker.
    
    Args:
        client: MQTT client instance
        userdata: User-defined data
        flags: Response flags from broker
        rc: Return code indicating connection status (0 = success)
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
    Update the current state dictionary with new position or metadata.
    
    Args:
        topic (str): MQTT topic that received the message
        payload (str): Message payload containing position data or metadata
    """
    global CURRENT_STATE

    # Handle coordinate updates for ball and goal devices
    if topic == '/TEF/device/b' or topic == '/TEF/device/g':
        lat, lon = parse_coordinates(payload)
        CURRENT_STATE[topic]['lat'] = lat
        CURRENT_STATE[topic]['lon'] = lon
        print(f"[{topic}] Update coordinates: '{lat}, {lon}'")

    # Handle last_touch metadata updates
    if topic == '/TEF/application/last_touch':
        team, name = parse_metadata(payload)
        CURRENT_STATE[topic]['team'] = team
        CURRENT_STATE[topic]['soccer_name'] = name
        print(f"[LAST TOUCH] Update last touch: {name} ({team})")

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

    # Extract current positions and metadata from state
    ball_lat = CURRENT_STATE['/TEF/device/b']['lat']
    ball_lon = CURRENT_STATE['/TEF/device/b']['lon']
    gol_lat = CURRENT_STATE['/TEF/device/g']['lat']
    gol_lon = CURRENT_STATE['/TEF/device/g']['lon']
    soccer_team = CURRENT_STATE['/TEF/application/last_touch']['team']
    soccer_name = CURRENT_STATE['/TEF/application/last_touch']['soccer_name']
    
    # Check if all required fields have valid data
    campos_check = [ball_lat, ball_lon, gol_lat, gol_lon, soccer_team, soccer_name]
    
    if all(campos_check):
        try:
            # Calculate distance between ball and goal
            distance = euclidiane_distance(ball_lat, ball_lon, gol_lat, gol_lon)

            # If ball is close enough to the goal, publish goal event
            if distance <= d_tolerance:
                payload = f"{soccer_team} ({soccer_name}) scored a goal" 
                client.publish(f"/TEF/application/goal", payload)
                print(f"[GOAL] {soccer_name} from {soccer_team} scored a goal")
        except (ValueError, TypeError) as e: 
            print(f"[MATH ERROR] Failed to convert or calculate distance: {e}")

# MQTT client setup and connection
client = mqtt.Client()
client.on_connect = on_connect  # Set connection callback
client.on_message = on_message  # Set message reception callback

try: 
    # Connect to broker and start listening loop
    print(f"[CONNECTION] Trying to connect to {BROKER_ADDRESS}:{BROKER_PORT}")
    client.connect(BROKER_ADDRESS, BROKER_PORT, KeepAliveBroker)
    print(f"[STATUS] Connected, starting loop...")
    client.loop_forever()  # Blocking call that processes network traffic
except Exception as e: 
    print(f"[CONNECTION ERROR] Error connecting to broker: {e}")
    exit()