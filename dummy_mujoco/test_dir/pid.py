import numpy as np

class PID:
    def __init__(self, kp, ki, kd, ki_limit):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.ki_limit = ki_limit
        self.integral = 0
        self.prev_error = 0
        self.dout_limit = 5;
    def out(self,current_value,current_velocity,target_value):
        error = target_value - current_value
        self.integral += error
        if self.integral > self.ki_limit:
            self.integral = self.ki_limit
        elif self.integral < -self.ki_limit:
            self.integral = -self.ki_limit
        d_out = self.kd * current_velocity
        if d_out > self.dout_limit:
            d_out = self.dout_limit
        elif d_out < -self.dout_limit:
            d_out = -self.dout_limit
        output = self.kp * error + self.ki * self.integral - d_out
        self.prev_error = error
        return output
