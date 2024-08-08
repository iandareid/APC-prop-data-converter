import parser
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

class Converter():
    def __init__(self, dat_file, prop_diameter, rho = 1.225, desired_rpms=None) -> None:
        self.convert_all = False
        self.desired_rpms = set()
        self.D = prop_diameter # inches
        self.rho = rho # kg/m^3

        if desired_rpms == None:
            self.convert_all = True
        else:
            self.desired_rpms.update(desired_rpms)

        self.parser = parser.DATParser(dat_file)

        self.coeffs = []

        self.J_data = np.array([])
        self.CTs = np.array([])
        self.CQs = np.array([])

    def convert_CT(self):

        data = self.parser.parse()

        for rpm, measurements in data.items():
            if not self.convert_all and int(rpm) not in self.desired_rpms:
                continue

            df = pd.read_csv(measurements)

            thrusts = df['Thrust (N)'].values


            rho = self.rho 
            D = self.D * 0.0254

            omega = int(rpm) * 2 * np.pi / 60.

            self.CTs = np.append(self.CTs,thrusts / (rho * D**4 * omega**2) * 4 * np.pi**2)

            if self.J_data.size != self.CTs.size:
                self.J_data = np.append(self.J_data, df['J (Adv_Ratio)'].values)
    
    def convert_CQ(self):

        data = self.parser.parse()

        for rpm, measurements in data.items():
            if not self.convert_all and int(rpm) not in self.desired_rpms:
                continue

            df = pd.read_csv(measurements)

            torques = df['Torque (N-m)'].values

            rho = self.rho 
            D = self.D * 0.0254

            omega = int(rpm) * 2 * np.pi / 60.

            self.CQs = np.append(self.CQs,torques / (rho * D**5 * omega**2) * 4 * np.pi**2)

            if self.J_data.size != self.CTs.size:
                self.J_data = np.append(self.J_data, df['J (Adv_Ratio)'].values)

    def plot_CT(self):
        self.coeffs_CT = np.polyfit(self.J_data, self.CTs, 2)
        self.second_order_fit_CT = np.poly1d(self.coeffs_CT)

        x_fit = np.linspace(min(self.J_data), max(self.J_data), 50)
        y_fit = self.second_order_fit_CT(x_fit)

        plt.scatter(self.J_data, self.CTs, label='Empirical Data')
        plt.plot(x_fit, y_fit, color='r', label='Second Order Fit')

        plt.legend()
        plt.title('Thrust Coeffecient Versus Advance Ratio')
        plt.xlabel('Advance Ratio - J (1/rev)')
        plt.ylabel('Thrust Coeffecient - C_T')


        plt.show()
    
    def plot_CQ(self):
        self.coeffs_CQ = np.polyfit(self.J_data, self.CQs, 2)
        self.second_order_fit_CQ = np.poly1d(self.coeffs_CQ)

        x_fit = np.linspace(min(self.J_data), max(self.J_data), 50)
        y_fit = self.second_order_fit_CQ(x_fit)

        plt.scatter(self.J_data, self.CQs, label='Empirical Data')
        plt.plot(x_fit, y_fit, color='r', label='Second Order Fit')

        plt.legend()
        plt.title('Torque Coeffecient Versus Advance Ratio')
        plt.xlabel('Advance Ratio - J (1/rev)')
        plt.ylabel('Torque Coeffecient - C_Q')


        plt.show()

if __name__ == "__main__":
    dat_file = '../dat_files/PER3_15x55MR.dat'
    # Give the converter the dat_file path, the Diameter of the prop in inches,
    # air density you want to use, and the desired RPMs to analyze.
    converter = Converter(dat_file, 15, 1.225, [5000, 6000, 7000, 8000, 9000])
    converter.convert_CT()
    converter.convert_CQ()
    converter.plot_CT()
    converter.plot_CQ()
