from gpiozero import LED, PWMLED

class Motor():
    def __init__(self, dir_pin, pwm_pin):
        self.dir_input = LED(dir_pin)
        self.pwm_input = PWMLED(pwm_pin)
        self.pwm_input.value = 0
        self.dir_input.off()

    def forward(self, speed = 1.0):
        self.dir_input.on()
        self.pwm_input.value = speed

    def backward(self, speed = 1.0):
        self.dir_input.off()
        self.pwm_input.value = speed