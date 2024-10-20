import sys
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def bin2logisim(in_filename, out_filename):
    """ convert binary file to RLE-compressed logisim data file """
    with open(in_filename, 'rb') as infile, open(out_filename, 'wt') as outfile:
        outfile.write('v2.0 raw\n')
        count = 0
        byte = infile.read(1)
        old_byte = byte
        while byte != b'':
            if byte != old_byte:
                if count == 1:
                    outfile.write('{:x}\n'.format(int.from_bytes(old_byte, byteorder='little')))
                else:
                    outfile.write('{:d}*{:x}\n'.format(count, int.from_bytes(old_byte, byteorder='little')))
                count = 1
            else:
                count += 1
            old_byte = byte
            byte = infile.read(1)
        if count == 1:
            outfile.write('{:x}\n'.format(int.from_bytes(old_byte, byteorder='little')))
        else:
            outfile.write('{:d}*{:x}\n'.format(count, int.from_bytes(old_byte, byteorder='little')))

def logisim2bin(in_filename, out_filename):
    """ Convert logisim data file to binary """
    with open(in_filename, 'rt') as infile, open(out_filename, 'wb') as outfile:
        line = infile.readline().strip()
        if line != 'v2.0 raw':
            sys.stderr.write('Unrecognized file format.\n')
            sys.exit(-1)
        for line in infile:
            for val in line.split():
                parts = val.split('*')
                if len(parts) == 2:
                    for _ in range(int(parts[0])):
                        outfile.write(bytes([int(parts[1], 16),]))
                else:
                    outfile.write(bytes([int(val, 16),]))

if __name__ == '__main__':
    # Initialize Tkinter (for file dialog)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Ask user to select the input file
    in_filename = askopenfilename(title="Select input file")

    # Ask user to select where to save the output file
    out_filename = asksaveasfilename(title="Select output file")

    # Ask what type of conversion to perform
    conversion_type = input("Enter '1' for bin to logisim or '2' for logisim to bin: ").strip()

    if conversion_type == '1':
        bin2logisim(in_filename, out_filename)
    elif conversion_type == '2':
        logisim2bin(in_filename, out_filename)
    else:
        print("Unknown option. Exiting.")
        sys.exit(-1)
