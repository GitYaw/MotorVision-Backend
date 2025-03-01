import numpy as np
import pygame
import random
import csv
import os
import time

# Proximity sensor simulation including screen boundaries
def get_proximity_readings(player_x, player_y, total_angle, ai_bikes):
    sensor1_angle = np.radians(total_angle + 135)  # Left back side
    sensor2_angle = np.radians(total_angle - 135)  # Right back side

    sensor1_distance = sensor_max_range
    sensor2_distance = sensor_max_range
    sensor1_target = (player_x + sensor_max_range * np.cos(sensor1_angle), player_y + sensor_max_range * np.sin(sensor1_angle))
    sensor2_target = (player_x + sensor_max_range * np.cos(sensor2_angle), player_y + sensor_max_range * np.sin(sensor2_angle))

    # Check against AI bikes
    for ai_bike in ai_bikes:
        ai_rect = pygame.Rect(ai_bike["x"] - bike_length // 2, ai_bike["y"] - bike_width // 2, bike_length, bike_width)

        for distance in range(1, sensor_max_range + 1):
            test_x1 = int(player_x + distance * np.cos(sensor1_angle))
            test_y1 = int(player_y + distance * np.sin(sensor1_angle))
            test_x2 = int(player_x + distance * np.cos(sensor2_angle))
            test_y2 = int(player_y + distance * np.sin(sensor2_angle))

            if ai_rect.collidepoint(test_x1, test_y1):
                sensor1_distance = distance
                sensor1_target = (test_x1, test_y1)
                break

            if ai_rect.collidepoint(test_x2, test_y2):
                sensor2_distance = distance
                sensor2_target = (test_x2, test_y2)
                break

    # Check against screen boundaries
    def check_boundary(sensor_angle, sensor_distance, sensor_target):
        for distance in range(1, sensor_max_range + 1):
            test_x = int(player_x + distance * np.cos(sensor_angle))
            test_y = int(player_y + distance * np.sin(sensor_angle))

            # Check if out of screen bounds
            if test_x < 0 or test_x >= WIDTH or test_y < 0 or test_y >= HEIGHT:
                if distance < sensor_distance:
                    # print("SCREEN BOUND")
                    return distance, (test_x, test_y)
                break
        return sensor_distance, sensor_target

    # Update sensor readings with screen boundary checks
    sensor1_distance, sensor1_target = check_boundary(sensor1_angle, sensor1_distance, sensor1_target)
    sensor2_distance, sensor2_target = check_boundary(sensor2_angle, sensor2_distance, sensor2_target)

    return sensor1_distance, sensor2_distance, sensor1_target, sensor2_target

def findUnusedFilename():
    for i in range(0,int(1e5)):
        potentialFilename = "sim" + str(i) + ".csv"
        if (not os.path.exists(potentialFilename)):
            return potentialFilename
    return "BACKUP.csv"

def removeAllFilesOfExtensionIn(path, extension):
    for file in os.listdir(path):
        if file.endswith(extension):
            os.remove(os.path.join(path, file))

def saveMatrixToCsv(data, columns):
    filename = findUnusedFilename()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)

def estimateAccelerometerReading(x, y, angle, velocity, dt, prev_state):
    # param prev_state: Tuple containing (prev_x, prev_y, prev_angle, prev_velocity)
    
    if not prev_state or dt == 0:
        return 0, 0, 0  # Not enough data to estimate acceleration
    
    prev_x, prev_y, prev_angle, prev_velocity = prev_state
    
    # Compute acceleration in x and y using finite difference method
    ax = (velocity * np.cos(np.radians(angle)) - prev_velocity * np.cos(np.radians(prev_angle))) / dt
    ay = (velocity * np.sin(np.radians(angle)) - prev_velocity * np.sin(np.radians(prev_angle))) / dt
    
    # Approximate vertical acceleration with a small oscillation heuristic
    az = 0.1 * (ax**2 + ay**2) ** 0.5  # Simulating minor road bumps and vertical movement
    
    return [ax, ay, az]


# DRIVER CODE BELOW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Starting tasks
print()
# removeAllFilesOfExtensionIn(os.getcwd(), ".csv")

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Bike params
x, y = WIDTH // 2, HEIGHT // 2  # Initial position
velocity = 0  # Initial velocity
angle = 0  # Initial orientation
max_velocity = 16
acceleration = 0.3
deceleration = 0.15
drift_factor = 0.2
turning_speed = 10
# Helmet parameters
helmet_angle = 0  # Initial orientation relative to the bike
max_helmet_turn = 80  # Maximum deviation in degrees
helmet_turn_speed = 2
# Proximity sensor params
sensor_max_range = 150  # Max distance sensors can detect obstacles

# AI Motorcycle parameters
num_ai_bikes = 5
bike_length, bike_width = 20, 7
ai_bikes = []
for _ in range(num_ai_bikes):
    ai_bikes.append({
        "x": x + np.random.randint(-100, 100),
        "y": y + np.random.randint(-100, 100),
        "velocity": np.random.uniform(2, 4),
        "angle": np.random.uniform(0, 360)
    })

# Recording setup
recording = False
trajectory = []
recordingDataCols = ["t", "x", "y", "yaw (deg)", "v", "d_s1", "d_s2", "ax", "ay", "az"]
for i in range(len(ai_bikes)):
    recordingDataCols += [f"x_car{i}", f"y_car{i}", f"yaw_car{i}", f"v_car{i}"]

# Recording customizable params
survivalRecMode = True
recordingTimestepSecs = 0.5
maxRecordingDurationMins = 5
maxRecordingLength = int( int(60 / recordingTimestepSecs) * maxRecordingDurationMins)

# Main loop
running = True
lastRecSaveTime = time.time()
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                recording = True
                print("Recording vehicles' trajectories and proximity sensor values")
            elif event.key == pygame.K_BACKSPACE:
                recording = False
                # print("-------------------------\nRecorded Trajectory:\n", trajectory, "\n\n")
                # trajectory = addNoiseToRecording(trajectory, noiseRatio=0.1)
                saveMatrixToCsv(trajectory, recordingDataCols)
                trajectory = []

    # Get key inputs
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        velocity = min(max_velocity, velocity + acceleration)
    elif keys[pygame.K_DOWN]:
        velocity = max(-max_velocity, velocity - deceleration)
    
    if keys[pygame.K_RIGHT]:
        angle += turning_speed * (velocity / max_velocity)  # Turning scales with speed
    if keys[pygame.K_LEFT]:
        angle -= turning_speed * (velocity / max_velocity)
    
    if keys[pygame.K_a]:
        helmet_angle = min(max_helmet_turn, helmet_angle + helmet_turn_speed)
    if keys[pygame.K_s]:
        helmet_angle = max(-max_helmet_turn, helmet_angle - helmet_turn_speed)
    
    # add in friction
    if velocity > 0: velocity = velocity * 0.98 - 0.003
    else: velocity = velocity * 0.98 + 0.003

    # Calculate new position with drift
    rad_angle = np.radians(angle)
    drift_x = np.cos(rad_angle) * velocity + np.sin(rad_angle) * velocity * drift_factor
    drift_y = np.sin(rad_angle) * velocity - np.cos(rad_angle) * velocity * drift_factor
    
    x += drift_x
    y += drift_y

    # Keep within bounds
    x = max(0, min(WIDTH, x))
    y = max(0, min(HEIGHT, y))
    
    # Update AI motorcycles to chase the player
    for ai_bike in ai_bikes:
        dx = x - ai_bike["x"]
        dy = y - ai_bike["y"]
        ai_bike["angle"] = np.degrees(np.arctan2(dy, dx))
        rad_ai_angle = np.radians(ai_bike["angle"])
        ai_bike["x"] += np.cos(rad_ai_angle) * ai_bike["velocity"]
        ai_bike["y"] += np.sin(rad_ai_angle) * ai_bike["velocity"]
    
    # Get proximity sensor readings (helmet orientation affects sensors)
    total_angle = angle + helmet_angle
    sensor1_distance, sensor2_distance, sensor1_target, sensor2_target = get_proximity_readings(x, y, total_angle, ai_bikes)
    
    # add recording data
    if recording:
        # terminate recording upon a motorcycle collision
        if survivalRecMode and (x <= 0 or x >= WIDTH or y <= 0 or y >= HEIGHT or any(pygame.Rect(x, y, bike_width, bike_length).colliderect(pygame.Rect(bike["x"], bike["y"], bike_width, bike_length)) for bike in ai_bikes)):
            recording = False
            # trajectory = addNoiseToRecording(trajectory, noiseRatio=0.1)
            saveMatrixToCsv(trajectory, recordingDataCols)
            trajectory = []
        else:
            # display recording sign
            screen.blit(pygame.font.SysFont(None, 36).render("REC", True, (255, 0, 0)), (10, 10))
            # save recording data
            if time.time() - lastRecSaveTime > recordingTimestepSecs:
                # add to recording
                lastRecSaveTime = time.time()
                trajectory_row = [lastRecSaveTime, x, y, angle, velocity, sensor1_distance, sensor2_distance]
                # add accelerometer vals
                if len(trajectory) > 0:
                    trajectory_row += estimateAccelerometerReading(x, y, angle, velocity, recordingTimestepSecs, trajectory[-1][1:5])
                else:
                    trajectory_row += [0,0,0]
                # add other bikes' info
                for ai_bike in ai_bikes:
                    trajectory_row += [ai_bike['x'], ai_bike["y"], ai_bike["angle"], ai_bike["velocity"]]
                trajectory.append(trajectory_row)
                # # remove from recording
                # if len(trajectory) > maxRecordingLength:
                #     trajectory.pop(0)

                



    # Draw proximity sensor lines outward
    pygame.draw.line(screen, (0, 255, 0), (x, y), sensor1_target, 2)
    pygame.draw.line(screen, (0, 255, 0), (x, y), sensor2_target, 2)
    
    # Draw player motorcycle
    bike_rect = pygame.Surface((bike_length, bike_width), pygame.SRCALPHA)
    bike_rect.fill((0, 255, 0))
    rotated_bike = pygame.transform.rotate(bike_rect, -angle)
    rect_center = rotated_bike.get_rect(center=(x, y))
    screen.blit(rotated_bike, rect_center.topleft)
    
    # Draw AI motorcycles
    for ai_bike in ai_bikes:
        ai_bike_rect = pygame.Surface((bike_length, bike_width), pygame.SRCALPHA)
        ai_bike_rect.fill((255, 0, 0))
        rotated_ai_bike = pygame.transform.rotate(ai_bike_rect, -ai_bike["angle"])
        ai_rect_center = rotated_ai_bike.get_rect(center=(ai_bike["x"], ai_bike["y"]))
        screen.blit(rotated_ai_bike, ai_rect_center.topleft)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

# TODOS
# func. to open recording from csv (data stitching)
