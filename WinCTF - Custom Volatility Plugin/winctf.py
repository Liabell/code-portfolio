### Volatility 3 Framework 2.9.0 winctf plugin for Windows
### Authors: Liam Dumbell, Joshua Hartzfeld, Logan Klaproth
### Place Inside: volatility3/volatility3/framework/plugins/windows

### currently finds flags within multiple specified processes in the process_names[] array, needs to check netscan, malfind, apihooks, etc. in the future
### needs to maybe also work with autoVolatility.py later on for efficiency

import os
import contextlib
import logging
import subprocess
import os
import re
from volatility3.framework import interfaces, exceptions, renderers
from volatility3.framework.configuration import requirements
from volatility3.framework.renderers import format_hints
from volatility3.plugins.windows import pslist, hashdump
from volatility3.plugins.windows import pslist, hashdump, malfind

from volatility3.plugins.windows.registry import hivescan, hivelist

vollog = logging.getLogger(__name__)


class ProcessDump(interfaces.plugins.PluginInterface):
    """Finds specified processes and dumps their memory into individual files, searching for flags."""

    _required_framework_version = (2, 0, 0)

    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(name="kernel", description="Windows kernel",
                                           architectures=["Intel32", "Intel64"]),
            requirements.StringRequirement(name="dump_dir", description="Directory to dump memory", optional=False),
        ]

    def _generator(self):
        # Prompt user for the flag format string
        flag_format = input("\nEnter the flag format string, Example: 'SKY-', 'flag{', 'ctf(', 'secret': ")

        # Process names to look for
        malfindings = self.get_suspicious_processes()
        process_names = ["ruby.exe", "notepad.exe","firefox.exe", "chrome.exe", "msedge.exe","MicrosoftEdge.exe"]
        browser_names = ["firefox.exe", "chrome.exe", "msedge.exe","MicrosoftEdge.exe"]
        
        # add process names of processes found in malfind, comment this out to skip memory dumps of these processes
        for i in malfindings: 
            process_names.append(i[1])

        kernel = self.context.modules[self.config["kernel"]]

        # Iterate over each process name and search for it in the process list
        for process_name in process_names:
            process_pid = None

            # Locate the process by its name
            for proc in pslist.PsList.list_processes(self.context, kernel.layer_name, kernel.symbol_table_name):
                proc_name = proc.ImageFileName.cast("string", max_length=proc.ImageFileName.vol.count, errors="replace")
                if proc_name.lower() == process_name.lower():
                    process_pid = proc.UniqueProcessId
                    vollog.info(f"Found {process_name} with PID: {process_pid}")
                    print(f"\nFound {process_name} with PID: \033[92m{process_pid}\033[92m")
                    break

            if not process_pid:
                vollog.warning(f"{process_name} process not found.")
                continue

            # Locate and map process memory segments
            with contextlib.ExitStack() as stack:
                print(f"\n\033[0mPreparing to write Memory Dump for {process_name} ...")
                # Prepare output file for the process memory dump
                dump_dir = self.config["dump_dir"]
                os.makedirs(dump_dir, exist_ok=True)
                file_path = os.path.join(dump_dir, f"{process_pid}_{process_name}_memory_dump.dmp")
                file_handle = stack.enter_context(open(file_path, "wb"))

                # Obtain the process layer for memory mapping
                try:
                    proc_layer_name = proc.add_process_layer()
                    proc_layer = self.context.layers[proc_layer_name]
                except exceptions.InvalidAddressException as excp:
                    vollog.error(f"Invalid address in layer {excp.layer_name} for PID {process_pid}")
                    continue

                # Calculate total memory size to write
                total_size = 0
                for _, size, _, _, _ in proc_layer.mapping(0x0, proc_layer.maximum_address, ignore_errors=True):
                    total_size += size

                written_size = 0

                print(f"\033[0mAttempting to write Memory Dump for {process_name} ...")
                # Iterate over memory mappings and write to file
                for offset, size, mapped_offset, mapped_size, maplayer in proc_layer.mapping(
                        0x0, proc_layer.maximum_address, ignore_errors=True
                ):
                    try:
                        # Read the memory content in the range of the process
                        data = proc_layer.read(offset, size, pad=True)
                        file_handle.write(data)

                        written_size += size

                        # Calculate and print percentage
                        percentage = (written_size / total_size) * 100
                        print(f"\rWriting Memory Dump for {process_name}: \033[96m{percentage:.2f}\033[0m% complete", end='',
                              flush=True)

                    except exceptions.InvalidAddressException as e:
                        vollog.debug(f"Failed to read segment at {offset:#x} for PID {process_pid}: {e}")

                print(f"\r\033[96mMemory Dump for {process_name} complete.\033[0m                      ")
                if process_name in browser_names:
                    self.strings_browser_dump(file_path,process_name)
                else:
                    self.execute_strings_command(file_path, flag_format)

            print("\r\n\033[96mMemory Dump complete.\033[0m                      ")
            print()
            print('-' * 60)

        # Obtain and print Windows hashes from the hashdump plugin
        self.get_and_print_hashes()

    def strings_browser_dump(self,file_path, proc_name):
        print("\nAnalyzing browser dump")
        url_regex = r'https?:\/\/[^\s]+' # regex pog
        browser_file_path = os.path.join(self.config["dump_dir"], f"dump_for_{proc_name}.txt")
        browser_output_log = open(browser_file_path, 'w')
        command = f"strings -e l {file_path}"
        try:
            output = subprocess.run(command, shell=True, capture_output=True, text=True)

            if output.stdout:
                urls = re.findall(url_regex,output.stdout)
                print(f"Found URLS prints 10 MAX:")
                max_urls = min(len(urls), 10)
                for i in range(max_urls):
                    print(f"\n\033[92m{urls[i]}\033[0m")
                browser_output_log.write(output.stdout.strip())
                print(f"\n\033[92mYes this is in a output log called dump_for_{proc_name}\033[0m")
            else:
                command = f"strings -e {file_path}"
                output2 = subprocess.run(command, shell=True, capture_output=True, text=True)
                if output2.stdout:
                    urls = re.findall(url_regex, output2.stdout)
                    print(f"Found URLS prints 10 MAX:")
                    max_urls = min(len(urls), 10)
                    for i in range(max_urls):
                        print(f"\n\033[92m{urls[i]}\033[0m")
                    browser_output_log.write(output.stdout.strip())
                    print(f"\n\033[92mYes this is in a output log called dump_for_{proc_name}\033[0m")
                else:
                    print("we found nothin :(")
        except Exception as e:
            vollog.error(f"Error executing strings command: {e}")

    def execute_strings_command(self, file_path, flag_format):
        command = f"strings -e l {file_path} | grep '{flag_format}'"  # little endian
        print("\nAttempting to look for potential flags ...")
        try:
            # Execute the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            # Print the output
            if result.stdout:
                print(f"Found potential flags: \n\033[92m{result.stdout.strip()}\033[0m")
            else:
                command = f"strings {file_path} | grep '{flag_format}'"  # big endian
                result2 = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result2.stdout:
                    print(f"Found potential flags: \n\033[92m{result2.stdout.strip()}\033[0m")
                else:
                    print(f"No potential flags found matching flag format: \033[91m{flag_format}\033[0m")

        except Exception as e:
            vollog.error(f"Error executing strings command: {e}")


    def get_and_print_hashes(self):
        """Executes the hashdump plugin and writes hashes to a file."""
        try:
            print("\nAttempting to retrieve Hashes from Memory Dump ...\n")
            # Extract SYSTEM and SAM hives (contains NTLM hashes) from memory
            syshive = None
            samhive = None

            # Assuming 'kernel' is already obtained from the context as it was in your earlier code
            kernel = self.context.modules[self.config["kernel"]]

            # Get the hives from the memory dump
            for hive in hivelist.HiveList.list_hives(
                    self.context,
                    self.config_path,
                    kernel.layer_name,
                    kernel.symbol_table_name,
            ):
                if hive.get_name().split("\\")[-1].upper() == "SYSTEM":
                    syshive = hive
                elif hive.get_name().split("\\")[-1].upper() == "SAM":
                    samhive = hive

            # Check if both hives are found
            if not syshive or not samhive:
                vollog.error("Could not find SYSTEM or SAM hives.")
                return

            # Now create the hashdump plugin and pass the hives into _generator
            hashdump_plugin = hashdump.Hashdump(context=self.context, config_path=self.config_path)

            # Generate hashes by calling _generator with the required hives
            hashes = hashdump_plugin._generator(syshive, samhive)

            # Log the raw hashes to inspect the returned data structure
            vollog.info(f"Raw hashdump output: {hashes}")

            hashes_file_path = os.path.join(self.config["dump_dir"], "hashes.txt")
            with open(hashes_file_path, "w") as hashes_file:
                # Write the hashes to the file
                if hashes:
                    print("Hashes Found:\n")
                    for entry in hashes:
                        # Unpack the first element, which is a tuple that contains the hash data
                        hash_data = entry[1]

                        # Now unpack the hash data tuple (user, rid, lmhash, nthash)
                        if len(hash_data) == 4:
                            user, _, _, nthash = hash_data  # Unpack to get user and nthash
                        else:
                            vollog.warning(f"Unexpected hash entry format: {hash_data}")
                            continue

                        # Ensure nthash is a string before printing and writing
                        if isinstance(nthash, str):
                            print(f"\033[92m{user}\033[0m:\033[96m{nthash.strip()}\033[0m")  # Print to console
                            hashes_file.write(nthash.strip() + "\n")  # Write to the file
                        else:
                            vollog.warning(f"NT hash is not a string: {nthash}")
                else:
                    vollog.warning("No hashes found.")

                hashes_file.flush()  # Ensure the file content is fully written
                print(f"Hashes have been written to: \033[92m{hashes_file_path}\033[0m")

            # Now execute hashcat with the hashes file after ensuring it is written
            self.execute_hashcat_command(hashes_file_path)
            print()
            print('-' * 60)

        except Exception as e:
            vollog.error(f"Error obtaining hashes: {e}")


    def execute_hashcat_command(self, hashes_file_path):
        """Executes the hashcat command after the hashes file is written."""
        # Construct the hashcat command
        hashcat_command = f"hashcat -m 1000 -a 0 {hashes_file_path} rockyou.txt --potfile-disable"  # you can customize the command here to use different wordlists you have installed if you want to

        print(f"\nAttempting to Crack Passwords ...\n\n{hashcat_command}")

        try:
            # Execute the hashcat command
            result = subprocess.run(hashcat_command, shell=True, capture_output=True, text=True)

            # Print only the lines containing hashes using regex
            hash_pattern = re.compile(r'^[a-fA-F0-9]{32}(:[^\n]+)?$')
            if result.returncode == 0:
                # Process the output and filter out lines containing hashes
                for line in result.stdout.splitlines():
                    if hash_pattern.match(line):
                        print(f'\033[96m{line.replace(":", "\033[0m:\033[92m")}\033[0m')
            else:
                print(f"Hashcat Error:\n{result.stderr}")

        except Exception as e:
            vollog.error(f"Error executing hashcat command: {e}")


    def get_suspicious_processes(self):
        """Match processes in PsList and Malfind to determine suspicious processes"""
        # list of processes
        kernel = self.context.modules[self.config["kernel"]]

        # output from malfind
        print("Running Malfind on memory dump...")
        malfinder = malfind.Malfind(self.context, self.config_path)
        malfind_list = list(
            malfinder._generator(pslist.PsList.list_processes(self.context, kernel.layer_name, kernel.symbol_table_name)))

        # retrieve process IDs from malfind
        malfindings = set()
        for i in malfind_list:
            # adds process name and pid
            st = str(i[1][1])
            if not st.endswith(".exe"):
                st = st.rstrip(".ex")
                st += ".exe"
            malfindings.add((i[1][0], st))

        if not malfindings:
            print("Nothing found with Malfind")
        else:
            print("Potential Suspicious Processes: ")
            for proc in malfindings:
                print(f"PID: {proc[0]} Process name: {proc[1]}")
        # returns a list of tuples
        return malfindings

    def run(self):
        return renderers.TreeGrid(
            [("PID", int), ("File Name", str)],
            self._generator()
        )