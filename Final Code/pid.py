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

    def __init__(self, Kp=0., Kd=0., Ki=0.1, uc=0.):
        self.Kp = Kp # proportional gain
        self.Kd = Kd # derivative time
        self.Ki = Ki # integration time

        self.y = 0. # input signal
        self.error = 0. # current error
        self.prev_error = 0. # previous error
        self.uc = uc # setpoint
        self.u = 0. # output

        self.P = 0. # proportional action
        self.D = 0. # derivative action
        self.I = 0. # integral action

        self.Imax = 2. # integral action limitter to prevent windup
        self.Imin = -2.

        self.umax = 1. # actuator range is [0., 1.0]
        self.umin = -1.

    def __str__(self):
        return f'P: {self.P}\nD: {self.D}\nI: {self.I}\nOutput: {self.u}\n'


    def write(self, data, dt):
        self.y = data
        self.prev_error = self.error
        self.error = self.uc - self.y

        self.P = self.Kp * self.error

        self.D = self.Kd * (self.error - self.prev_error)/dt

        if abs(self.error) < 3: # only integrate if the error is small
            self.I += self.Ki * self.error
        else:
            self.I = 0

        self.I = self.Imax if self.I > self.Imax else self.I
        self.I = self.Imin if self.I < self.Imin else self.I

    def read(self):
        output = self.P + self.D + self.I
        if output > self.umax:
            output = self.umax
        if output < self.umin:
            output = self.umin
        self.u = output
        return self.u

