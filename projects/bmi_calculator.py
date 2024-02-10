class BMICalc:

    def __init__(self, height, weight, age):
        self.height = height
        self.weight = weight
        self.age = age

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height <= 0:
            raise ValueError('Height can not be zero or a negative number.')
        else:
            self.__height = height

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age <= 0:
            raise ValueError('Age can not be a negative number')
        elif age < 2:
            raise ValueError(
                'This calculator is not valid for children under 2 years old.')
        else:
            self.__age = age

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        if weight <= 0:
            raise ValueError('Weight can not be zero or a negative number.')
        else:
            self.__weight = weight

    def bmi_value(self):
        # The height is stored as an integer in cm. Here we convert it to
        # meters (m).
        bmi_value = self.weight / ((self.height / 100.0) ** 2)
        return bmi_value

    def classify_bmi_teens_and_children(self):
        if self.age < 2 or self.age > 19:
            raise ValueError(
                'Invalid age. The children and teen BMI classification ' +
                'only works for ages between 2 and 19.')

        bmi_value = self.bmi_value()
        if self.age <= 4:
            if bmi_value <= 14:
                return "Underweight"
            elif bmi_value <= 17.5:
                return "Normal weight"
            elif bmi_value <= 18.5:
                return "Overweight"
            else:
                return "Obese"

        elif self.age <= 7:
            if bmi_value <= 13.5:
                return "Underweight"
            elif bmi_value <= 14:
                return "Normal weight"
            elif bmi_value <= 20:
                return "Overweight"
            else:
                return "Obese"

        elif self.age <= 10:
            if bmi_value <= 14:
                return "Underweight"
            elif bmi_value <= 20:
                return "Normal weight"
            elif bmi_value <= 22:
                return "Overweight"
            else:
                return "Obese"

        elif self.age <= 13:
            if bmi_value <= 15:
                return "Underweight"
            elif bmi_value <= 22:
                return "Normal weight"
            elif bmi_value <= 26.5:
                return "Overweight"
            else:
                return "Obese"

        elif self.age <= 16:
            if bmi_value <= 16.5:
                return "Underweight"
            elif bmi_value <= 24.5:
                return "Normal weight"
            elif bmi_value <= 29:
                return "Overweight"
            else:
                return "Obese"

        elif self.age <= 19:
            if bmi_value <= 17.5:
                return "Underweight"
            elif bmi_value <= 26.5:
                return "Normal weight"
            elif bmi_value <= 31:
                return "Overweight"
            else:
                return "Obese"

    def classify_bmi_adults(self):
        if self.age > 19:
            bmi_value = self.bmi_value()
            if bmi_value < 18.5:
                return "Underweight"
            elif bmi_value < 25.0:
                return "Normal weight"
            elif bmi_value < 30.0:
                return "Overweight"
            elif bmi_value < 40.0:
                return "Obese"
            else:
                return "Severely Obese"

        else:
            raise ValueError(
                "Invalid age. The adult BMI classification requires an age "
                "older than 19.")
