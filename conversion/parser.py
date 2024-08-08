import re
import io

class DATParser():
    def __init__(self, dat_file) -> None:
        # Import the dat file.
        with open(dat_file, 'r') as file:
            self.dat_contents = file.read()
    
    def parse(self) -> io.StringIO:
        # Split the document at each RPM break
        data_by_rpm = re.split(r"PROP RPM =+", self.dat_contents)

        # Remove the first split, it has no data.
        data_by_rpm.pop(0)

        data = {}

        # Iterate through the RPM data and clean and prepare for pandas dataframe.
        for rpm_data in data_by_rpm:
            # Remove all of the empty lines
            rpm_data = re.sub(r"\s*/n", '', rpm_data)
            # print(rpm_data)

            # Format is now RPM \n column names \n units \n data
            # Split the data at each new line.
            split_rpm_data = re.split(r"\n", rpm_data)
            
            # Isolate the RPM.
            split_rpm_data[0] = re.sub(r"\s*", '', split_rpm_data[0])
            
            # Save the RPM for use later.
            rpm = split_rpm_data.pop(0)
            
            # Clean the row data and split at the whitespace.
            cleaned_rows = []
            for row in split_rpm_data:
                row = row.split()
                # Don't add rows with to little data.
                if len(row) < 3:
                    continue
                cleaned_rows.append(row)

            # Delete empty row.
            # cleaned_rows.pop(0)

            # Combine the first two rows (the column names and units) to remove column name duplicates.
            # Change Torque to something like Torque (N-m)
            col_name_row = []
            for name, unit in zip(cleaned_rows.pop(0), cleaned_rows.pop(0)):
                
                # Don't add unit if there is none.
                if unit == '-':
                    unit = ''
                
                # Format column name.
                new_col_name = name + ' ' + unit
                col_name_row.append(new_col_name)

            cleaned_rows.insert(0, col_name_row)
            
            csv_rows = []
            for row in cleaned_rows:
                new_row = ','.join(row)
                csv_rows.append(new_row)

            csv_string = '\n'.join(csv_rows)

            csv_file = io.StringIO(csv_string)

            data[rpm] = csv_file

        return data




if __name__ == "__main__":
    dat_file = '../dat_files/PER3_15x55MR.dat'
    parser = DATParser(dat_file)
    data = parser.parse()
