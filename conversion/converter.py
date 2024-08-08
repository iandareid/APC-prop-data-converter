import parser
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

class Converter():
    def __init__(self, dat_file, desired_rpms=None) -> None:
        self.convert_all = False
        self.desired_rpms = set()

        if desired_rpms == None:
            self.convert_all = True
        else:
            self.desired_rpms.update(desired_rpms)

        self.parser = parser.DATParser(dat_file)

        self.coeffs = []

        self.J_data = np.array([])
        self.CTs = np.array([])

    def convert(self):

        data = self.parser.parse()

        for rpm, measurements in data.items():
            if not self.convert_all and int(rpm) not in self.desired_rpms:
                continue

            df = pd.read_csv(measurements)

            thrusts = df['Thrust (N)'].values
            self.J_data = np.append(self.J_data, df['J (Adv_Ratio)'].values)


            rho = 1.225 
            D = 15 * 0.0254

            omega = int(rpm) * 2 * np.pi / 60.

            self.CTs = np.append(self.CTs,thrusts / (rho * D**4 * omega**2) * 4 * np.pi**2)

    def plot(self):
        self.coeffs = np.polyfit(self.J_data, self.CTs, 2)
        self.second_order_fit = np.poly1d(self.coeffs)

        x_fit = np.linspace(min(self.J_data), max(self.J_data), 50)
        y_fit = self.second_order_fit(x_fit)

        plt.scatter(self.J_data, self.CTs, label='Empirical Data')
        plt.plot(x_fit, y_fit, color='r', label='Second Order Fit')

        plt.legend()
        plt.title('Thrust Coeffecient Versus Advance Ratio')
        plt.xlabel('Advance Ratio - J (1/rev)')
        plt.ylabel('Thrust Coeffecient - C_T')


        plt.show()

if __name__ == "__main__":
    dat_file = '../dat_files/PER3_15x55MR.dat'
    converter = Converter(dat_file, [5000, 6000, 7000, 8000, 9000])
    converter.convert()
    converter.plot()
