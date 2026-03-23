#!/usr/bin/python3

# INET4031
# Abdikani Abdi
# Date Created: 2026-03-23
# Date Last Modified: 2026-03-23

# os is used to run Linux system commands.
# re is used to check whether a line starts with #.
# sys is used to read the input file line by line.
import os
import re
import sys

def main():
    # Ask the user whether to do a dry run or a normal run.
    mode = input("Run in dry-run mode? Enter Y for yes or N for no: ").strip().upper()

    # If user enters Y, commands will only be printed.
    # If user enters N, commands will actually run.
    dry_run = (mode == "Y")

    # Read each line from standard input.
    for line in sys.stdin:
        original_line = line.strip()

        # Check if line starts with # so it can be skipped.
        match = re.match("^#", line)

        # Split the input line into colon-separated fields.
        fields = line.strip().split(':')

        # In dry-run mode, show if a line is skipped because it is commented out.
        if match:
            if dry_run:
                print(f"Skipping commented line: {original_line}")
            continue

        # In dry-run mode, show if a line has the wrong number of fields.
        if len(fields) != 5:
            if dry_run:
                print(f"Error: invalid line with wrong number of fields: {original_line}")
            continue

        # Store account information from the input line.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Split groups into a list in case there are multiple groups.
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % username)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        if dry_run:
            print(cmd)
        else:
            os.system(cmd)

        print("==> Setting the password for %s..." % username)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        if dry_run:
            print(cmd)
        else:
            os.system(cmd)

        for group in groups:
            # A dash means the user should not be added to extra groups.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)

                if dry_run:
                    print(cmd)
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()
