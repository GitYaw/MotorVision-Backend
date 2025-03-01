import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

# Example: vehicle position estimates
# Replace these with your actual x and y coordinates
x = np.array([0, 1, 0.5, 1.5, 1, 2])
y = np.array([0, 2, 3, 2.5, 1, 0.5])

# Stack the coordinates for parametric spline (each row is a coordinate)
points = np.vstack((x, y))

# Calculate the spline representation of the curve.
# Set s=0 to interpolate through the points exactly.
# If you have a closed trajectory (circle-like path), add per=True.
tck, u = splprep(points, s=0, per=False)  

# Evaluate the spline over a set of points (increase the number for a smoother curve)
u_fine = np.linspace(0, 1, 1000)
x_smooth, y_smooth = splev(u_fine, tck)

# Plot the original points and the smooth trajectory
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'o', label='Vehicle Position Estimates')
plt.plot(x_smooth, y_smooth, '-', label='Smooth Interpolated Trajectory')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Smooth Trajectory Interpolation')
plt.legend()
plt.grid(True)
plt.show()
