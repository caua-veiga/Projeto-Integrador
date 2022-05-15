# Sensors

We will use two sensors to determine the tilt angle from the horizontal plane.

The gyroscope usually senses the angular rate of change $\omega = \frac{d\theta}{dt}$. Therefore, we must integrate its output to obtain:

$$
\theta = \int \omega \,\, dt
$$

This means that any noise will be integrated together with the signal, contaminating our data. This is problematic when one also takes into account gyroscope drift due
to temperature fluctuations. 

The accelerometer allows us to acquire the angle by comparing the measured acceleration with gravity. The following analysis is valid for static measurents, which is 
the case.

Since $\vec{g}$ is approximately constant, using a 2-axis accelerometer we can infer tilt angle from measured acceleration:

$$
a_x = g\sin{\theta} \Leftrightarrow \theta = \arcsin{\frac{a_x}{g}}
$$

Note that since the $a_y$ measurement does not depends on direction of tilt, it will not be very useful. Also note that it is good practice to linearize this relation,
to save on processing time by avoinding calculation of trigonometric functions (at the cost of limitting measurable range)

# Combining the sensors

To integrate both sensor data, we use a technique called "complementary filter".

Accelerometer data $\rightarrow$ low-pass filter, to preserve only the constant gravitational acceleration

Gyroscope data $\rightarrow$ integrator $\rightarrow$ high-pass filter, to prevent drift integration

This gives two measurements for the tilt angle, that we can combine together to further average out noise.

# Note

We can also get the angular velocity directly from the gyroscope measurements. This means that when designing our PID controller, we must consider two options for the
differential control:

- Use data directly measured by the gyroscope
- Discard gyroscope data and numeracally differentiate the angle data
