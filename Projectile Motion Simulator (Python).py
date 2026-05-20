import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Input gathering
velocity = float(input("Enter initial velocity (m/s): "))
angle = float(input("Enter launch angle (degrees): "))
g = 9.8

theta = np.radians(angle)
time_of_flight = (2 * velocity * np.sin(theta)) / g
t = np.linspace(0, time_of_flight, 200)

item = velocity * np.cos(theta) * t
buffer = velocity * np.sin(theta) * t - 0.5 * g * t**2

vx = velocity * np.cos(theta)
vy = velocity * np.sin(theta) - g * t

# Compute range (horizontal distance traveled)
range_distance = (velocity**2 * np.sin(2 * theta)) / g
print(f"Range: {range_distance:.2f} m")

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, np.max(item) * 1.1)
ax.set_ylim(0, np.max(buffer) * 1.1)
ax.set_xlabel("Horizontal Distance (m)")
ax.set_ylabel("Vertical Height (m)")
ax.set_title("Projectile Motion: Components & Pause (Click to Toggle)")
ax.grid(True)

line, = ax.plot([], [], 'b-', lw=2, label="Path")
point, = ax.plot([], [], 'ko', ms=6)

# FIXED: Removed linestyle='--' from quiver to completely stop the ValueError
v_total = ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='r', label='Resultant V')
v_x_vec = ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='g', label='Vx')
v_y_vec = ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='b', label='Vy')

coord_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.legend(loc='upper right')

# Pause logic
is_paused = False
def toggle_pause(event):
    global is_paused
    if event.canvas.figure == fig:
        if is_paused: 
            ani.resume()
            is_paused = False
        else: 
            ani.pause()
            is_paused = True

fig.canvas.mpl_connect('button_press_event', toggle_pause)

def init():
    line.set_data([], [])
    point.set_data([], [])
    v_total.set_UVC([0], [0])
    v_x_vec.set_UVC([0], [0])
    v_y_vec.set_UVC([0], [0])
    coord_text.set_text(f'Time: 0.00s\nVx: {vx:.1f} m/s\nVy: {vy[0]:.1f} m/s\nRange: {range_distance:.2f} m')
    return line, point, v_total, v_x_vec, v_y_vec, coord_text

def update(frame):
    if frame >= len(t):
        frame = len(t) - 1

    line.set_data(item[:frame], buffer[:frame])
    point.set_data([item[frame]], [buffer[frame]])
    
    current_pos = [[item[frame], buffer[frame]]]
    
    # Update positions and lengths
    v_total.set_offsets(current_pos)
    v_total.set_UVC([vx], [vy[frame]])
    
    v_x_vec.set_offsets(current_pos)
    v_x_vec.set_UVC([vx], [0])
    
    v_y_vec.set_offsets(current_pos)
    v_y_vec.set_UVC([0], [vy[frame]])
    
    coord_text.set_text(f'Time: {t[frame]:.2f}s\nVx: {vx:.1f} m/s\nVy: {vy[frame]:.1f} m/s\nRange: {range_distance:.2f} m')
    return line, point, v_total, v_x_vec, v_y_vec, coord_text

ani = animation.FuncAnimation(
    fig, update, frames=len(t), init_func=init, blit=False, interval=20, repeat=True
)

plt.show()