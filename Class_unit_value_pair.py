class UnitValuePair:

    def __init__(self, value, unit):
        self.value = value
        self.unit = str(unit)
    
    def metric(self):
        if self.unit == 'in':
            return self.value * 0.0254
        if self.unit == 'lbf':
            return self.value * 4.44822
        if self.unit == 'lbs':
            return self.value / 2.20462
        if self.unit == 'lbf/in':
            return self.value* 4.44822 / 0.0254
        if self.unit == 'lbs*in^2':
            return self.value * (0.0254**2) / 2.20462
        else:
            pass