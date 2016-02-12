import cc_data
import cc_dat_utils
import cc_json_utils
import sys

default_input_json_file = "data/example_data.json"
default_output_dat_file = "data/example_dat.dat"

#Check if both input and output file have been specified
if len(sys.argv) == 3:
    input_json_file = sys.argv[1]
    output_dat_file = sys.argv[2]
    print("Using command line args:", input_json_file, output_dat_file)
else:
    input_json_file = default_input_json_file
    output_dat_file = default_output_dat_file
    print("Unknown command line options. Using default values:", input_json_file, output_dat_file)

#Gets json file from input or the default
cc_data_file = cc_json_utils.make_cc_data_from_json(input_json_file)
#Write created dat file to output file
cc_dat_utils.write_cc_data_to_dat(cc_data_file, output_dat_file)
print(output_dat_file+" Created")
