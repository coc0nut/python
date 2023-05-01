# This program can be run with python core packages. No module installation needed.
# Author Harald Trohne

import tkinter as tk

class IPForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg='#222222')
        self.title("Subnet Calculator")

        # Create the IP address label and text box
        self.ip_label = tk.Label(self, text="IP Address:", fg='white', bg='#222222')
        self.ip_label.pack()
        self.ip_edit = tk.Entry(self)
        self.ip_edit.pack()

        # Create the subnet prefix label and text box
        self.prefix_label = tk.Label(self, text="Subnet Prefix:", fg='white', bg='#222222')
        self.prefix_label.pack()
        self.prefix_edit = tk.Entry(self)
        self.prefix_edit.pack()

        options = []
        count = 16
        for num in range(16, 31):
            options.append(str(count))
            count += 1

        # Create the calculate button
        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate, fg='white', bg='#222222')
        self.calculate_button.pack()
        self.bind("<Return>", lambda event: self.calculate_button.invoke())
        # Create the output text box
        self.output_text = tk.Text(self, width=50, height=10, fg='white', bg='#222222')
        self.output_text.pack()

    def calculate(self):
        # clear text box
        self.output_text.delete("1.0", tk.END)
        ip = self.ip_edit.get()
        subnet = self.prefix_edit.get()
        subnets = {
        "30":"255.255.255.252", "29":"255.255.255.248", 
        "28":"255.255.255.240", "27":"255.255.255.224", 
        "26":"255.255.255.192", "25":"255.255.255.128",
        "24":"255.255.255.0",   "23":"255.255.254.0", 
        "22":"255.255.252.0",   "21":"255.255.248.0", 
        "20":"255.255.240.0",   "19":"255.255.224.0",
        "18":"255.255.192.0",   "17":"255.255.128.0", 
        "16":"255.255.0.0",
        }
        
        #  IP
        ip_mod = ip.split(".")
        ip_list = [int(i) for i in ip_mod]
        filled_list = []

        for e in ip_list:
            e = bin(e).replace("0b", "")
            if len(e) < 8:
                f = 8 - len(e)
                o = "0" * f
                result = str(o + e)
                filled_list.append(result)     
            else:
                filled_list.append(e)
        bin_ip_adr = ""
        for i in filled_list:
            bin_ip_adr += i + "."
        ip_bin = bin_ip_adr[:-1]
        self.output_text.insert("1.0", f"Host   : {ip_bin}\n")
        
        #  Subnet
        subnet_mod = subnets[subnet]
        subnet_str = subnet_mod.split(".")
        subnet_list = []
        subnet_complete = []
        for i in subnet_str:
            i = int(i)
            subnet_list.append(i)
        for e in subnet_list:
            e = bin(e).replace("0b", "")
            if len(e) < 8:
                f = 8 - len(e)
                o = "0" * f
                result = str(o+e)
                subnet_complete.append(result)
            else:
                subnet_complete.append(e)
        bin_subnet = ""
        for i in subnet_complete:
            bin_subnet += i + "."
        bin_subnet = bin_subnet[:-1]
        self.output_text.insert("2.0", f"Subnet : {bin_subnet}\n")
        
        #  Network identification
        NID = ""
        for i in range(len(bin_ip_adr) - 1):
            if bin_ip_adr[i] == "1" and bin_subnet[i] == "1":
                NID += "1"
            elif bin_ip_adr[i] == ".":
                NID += "."
            else:
                NID += "0"
        self.output_text.insert("3.0", f"NID    : {NID}\n")
        NID_dec = NID.split(".")
        NID_adr = ""
        for i in NID_dec:
            i = int(i, 2)
            NID_adr += str(i) + "."
        NID_adr = NID_adr[:-1]

        #  Broadcast Address
        BA = ""
        host_part = 32 - int(subnet)
        count = int(subnet)
        for i in range(len(bin_subnet)):  
            if bin_ip_adr[i] == "1" and bin_subnet[i] == "1":
                BA += "1"
            elif bin_ip_adr[i] == ".":
                BA += "."
            else:
                BA += "0"
        BA = BA[:-host_part] + "1" * host_part
        if BA[26] != ".":
            BA = BA[:26] + "." + "1" * 8
        else:
            BA = BA[:-host_part ] + "1" * host_part
        if host_part > 8:
            BA_mod = list(BA)
            for i in range(count + 2, len(bin_subnet) -9):
                BA_mod[i] = '1'
            BA_alt = ""    
            for e in BA_mod:
                BA_alt += e
            BA = BA_alt
        self.output_text.insert("4.0", f"BA     : {BA}\n")
        BA_dec = BA.split(".")
        BA_adr = ""
        for i in BA_dec:
            i = int(i, 2)
            BA_adr += str(i) + "."
        BA_adr = BA_adr[:-1]
        if ip == NID_adr:
            self.output_text.insert("1.0", "::WARNING:: Host address is the same as the NID! ::WARNING::\n")
        elif ip == BA_adr:
            self.output_text.insert("1.0", "::WARNING:: Host address is the same as the BA! ::WARNING::\n")
        self.output_text.insert("1.0", f"Host   : {ip}\n")
        self.output_text.insert("2.0", f"Subnet : {subnet_mod}\n")
        self.output_text.insert("3.0", f"NID:   : {NID_adr}\n")
        self.output_text.insert("4.0", f"BA:    : {BA_adr}\n")
        self.output_text.insert("5.0", f"Total adresses    : {str((2 ** host_part))}\n")
        self.output_text.insert("6.0", f"Available adresses: {str((2 ** host_part) - 2)}\n")

if __name__ == "__main__":
    form = IPForm()
    form.mainloop()
