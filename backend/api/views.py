from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
import base64
import logging
from .bluetooth_reader_sim import BluetoothReaderSimulation
from .trajectoryImgGenerator import image_generator, image_generator_live_start

# Initialize logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def home_page(request):
    return Response({"message": "This is the home page!"})

@api_view(['GET'])
def print_message(request):
    name = request.GET.get('name', 'World')
    team = request.GET.get('favorite-team', 'unknown team')
    return Response({"message": f"Hello, {name}, your favorite basketball team is {team}!"})

@api_view(['GET'])
def connect(request):
    try:
        bt_reader = BluetoothReaderSimulation(port="COM5", file_name=".sim13.csv")  # Adjust for deployment
        res = bt_reader.connect_sim()
        message = "Connected to Smart Helmet!" if res else "Connection not successful. Please try again."
        return Response({"message": message, "res": res})
    except Exception as e:
        logger.error(f"Error in Bluetooth connection: {e}")
        return Response({"error": "Connection failed"}, status=500)

@api_view(['GET'])
def traj_image(request):
    try:
        res = image_generator("Motorcyclist_Trajectory.csv", "motorcyclist_trajectory_map.html", 
                              "motorcyclist_trajectory_map_screenshot.png", 10, 5)
        with open(res, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        return Response({'image_data': img_data})
    except Exception as e:
        logger.error(f"Error generating trajectory image: {e}")
        return Response({"error": "Failed to generate image"}, status=500)

@api_view(['POST'])
def traj_image_live(request):
    data = request.data
    locations_array = data.get("locations", [])

    if not locations_array:
        return Response({"message": "No location data provided"}, status=400)

    try:
        latitudes = [loc["latitude"] for loc in locations_array]
        longitudes = [loc["longitude"] for loc in locations_array]
        timestamps = [loc["timestamp"] for loc in locations_array]

        timestamp = timestamps[0].replace(":", "-").replace(".", "_")
        csv_name = f"Motorcyclist_Trajectory_{timestamp}.csv"
        html_name = f"motorcyclist_trajectory_map_{timestamp}.html"
        screenshot_name = f"motorcyclist_trajectory_map_screenshot_{timestamp}.png"

        if len(locations_array) < 3 or (latitudes[0] == latitudes[-1] and longitudes[0] == longitudes[-1]):
            logger.info("Generating mock simulation due to insufficient movement")
            res = image_generator_live_start(csv_name, html_name, screenshot_name, 10, 5, latitudes[0], longitudes[0])
        else:
            logger.info("Generating real trajectory image")
            res = image_generator(csv_name, html_name, screenshot_name, 10, 5)

        with open(res, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        return Response({'image_data': img_data})

    except Exception as e:
        logger.error(f"Error processing trajectory image: {e}")
        return Response({"error": "Failed to process trajectory"}, status=500)

@api_view(['POST'])
def crash_prediction(request):
    try:
        data = request.data
        latitude = data.get("latitude")

        if not latitude:
            return Response({"error": "Missing latitude data"}, status=400)

        logger.info(f"Received location: {latitude}")
        return Response({"message": "Data received"}, status=200)

    except Exception as e:
        logger.error(f"Crash prediction error: {e}")
        return Response({"error": "Internal server error"}, status=500)
