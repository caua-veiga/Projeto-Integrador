class PID():
    """
    Implements an incremental PID controller
    Attributes Kp, Td, Ti require tuning
    Attributes N, b should not be considered during tuning
    The default actuator range is [0., 1.].
    This PID's output is meant to be used together with
    our PWM generating code in order to control the motors. Each motor PWM value must be
    updated symmetrically: new = old +-0.5 x output
    Therefore, it may be the case that the updated duty cycle is not in the actuator range.
    This case must be corrected externally.
    """

    def __init__(self, uc=0.):
        self.Kp = 0. # proportional gain
        self.Td = 0. # derivative time
        self.Ti = 0. # integration time
        self.N = 3. # derivative action limitter
        self.b = 0.8 # setpoint limitter for proportional action

        self.y = 0. # input signal
        self.yold = 0. # previous input
        self.uc = uc # setpoint
        self.u = 0. # output

        self.P = 0. # proportional action
        self.D = 0. # derivative action
        self.I = 0. # integral action

        self.Imax = 100. # integral action limitter to prevent windup

        self.umax = 1. # actuator range is [0., 1.0]
        self.umin = -1.

    def write(self, data, dt):
        self.P = self.Kp * (self.b * self.uc - self.y)

        self.D *= self.Td/(self.Td + self.N*dt)
        temp = (self.Kp * self.Td * self.N / (self.Td + self.N*dt))
        self.D -= temp * (self.y - self.yold)

        self.I += self.Kp * dt * (self.uc - self.y) / self.Ti
        if self.I > self.Imax: # prevent windup
            self.I = self.Imax

    def read(self):
        output = self.P + sel;f.D + self.I
        if output > self.umax:
            output = self.umax
        if output < self.umin:
            output = self.umin
        self.u = output
        return self.u

















