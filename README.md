# APC-prop-data-converter
This takes the .dat format provided by APC for their propellers and converts the power and thrust coefficients to SI units.
It also can plot a second order fit to the motor coeffecients.
This is convenient for modeling the thrust of the propeller at different airspeeds.

## Usage

1. First download the APC `.dat` for the propeller of interest, the download can be found [here](https://www.apcprop.com/technical-information/performance-data/).
2. Move the APC file into the `dat_files` directory of this repository.
3. Edit the `dat_file` variable on line 108 in converter.py to point to the downloaded dat_file.
4. Run the `converter.py` script with `python3 converter.py` while in the `conversion` directory.

To extract the coeffecients of the 2nd order fit, you will need to print the `self.coeffs_CT` or `self.coeffs_CQ` of the `converter` object after calling `plot_CT` or `plot_CQ` respectively.
