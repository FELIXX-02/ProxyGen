import asyncio
import socket
import random
import time
import os
import platform
import ipaddress
import threading
from concurrent.futures import ThreadPoolExecutor

class FelixProxyGen:
    def __init__(self):
        self.desktop_path = self.get_desktop_path()
        self.output_file = os.path.join(self.desktop_path, "FelixProxies.txt")
        print(f"File: {self.output_file}")
        
        self.ports = self.generate_elite_ports()
        self.ip_ranges = self.get_elite_ranges()
        
        self.stats = {
            'total_ips': 0,
            'scanned_ips': 0,
            'open_ports': 0,
            'start_time': time.time(),
            'ports_scanned': 0,
            'active_ips': set()
        }
        
        self.found_proxies = set()
        self.lock = threading.Lock()
        self.scanning = True

    def get_desktop_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return os.path.join(os.path.expanduser("~"), "Desktop")

    def generate_elite_ports(self):
        return [
            80, 8080, 443, 8443, 3128, 1080, 8081, 8000, 8888,
            9050, 8118, 9090, 8880, 10000, 8088, 9000, 8082,
            8090, 8181, 8008, 8089, 8889, 9999, 10001, 45000,
            50000, 55000, 8083, 8084, 8085, 1081, 1082, 3129,
            8123, 9001, 9051, 65432, 60000, 8086, 8087, 1083,
            1084, 3130, 9002, 9003, 9004, 10002, 10003, 2000 , 10004
        ]

    def get_elite_ranges(self):
        return [
            ipaddress.ip_network("104.16.0.0/12"),
            ipaddress.ip_network("108.0.0.0/8"),
            ipaddress.ip_network("172.64.0.0/13"),
            ipaddress.ip_network("141.101.0.0/16"),
            ipaddress.ip_network("198.41.128.0/17"),
            ipaddress.ip_network("162.158.0.0/15"),
            ipaddress.ip_network("131.0.72.0/22"),
            ipaddress.ip_network("172.217.0.0/16"),
            ipaddress.ip_network("142.250.0.0/15"),
            ipaddress.ip_network("216.58.0.0/15")
        ]

    def generate_ip(self):
        network = random.choice(self.ip_ranges)
        ip_int = random.randint(int(network[0]), int(network[-1]))
        return str(ipaddress.IPv4Address(ip_int))

    def check_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def save_proxy(self, proxy_str):
        try:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(f"{proxy_str}\n")
        except:
            pass

    async def scan_single_ip(self, ip):
        if ip in self.stats['active_ips']:
            return None
            
        for port in self.ports:
            try:
                if self.check_port(ip, port):
                    proxy_str = f"{ip}:{port}"
                    
                    with self.lock:
                        if ip not in self.stats['active_ips']:
                            self.stats['active_ips'].add(ip)
                            self.stats['open_ports'] += 1
                            self.found_proxies.add(proxy_str)
                            self.save_proxy(proxy_str)
                            print(f"Found: {proxy_str}")
                            return proxy_str
                            
            except:
                continue
        return None

    async def mass_scan_optimized(self, ip_batch):
        tasks = []
        for ip in ip_batch:
            task = asyncio.create_task(self.scan_single_ip(ip))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [result for result in results if result is not None]

    async def run_elite_scan(self, target_ips=5000):
        print (r"""



███████╗███████╗██╗     ██╗██╗  ██╗    ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗     ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██║     ██║╚██╗██╔╝    ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝    ██╔════╝ ██╔════╝████╗  ██║
█████╗  █████╗  ██║     ██║ ╚███╔╝     ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝     ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ██╔══╝  ██║     ██║ ██╔██╗     ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝      ██║   ██║██╔══╝  ██║╚██╗██║
██║     ███████╗███████╗██║██╔╝ ██╗    ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║       ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                                                                                
                                                                                                                                  


""")
        print("Dev : Felix")
        print("Felix Proxy Gen Starting......")
        print ("This Tool Scans More than 1M in One Hour !")
        print("Scanning for IPS...")
        print("-" * 40)
        
        ip_batch = []
        batch_size = 100
        
        try:
            while self.scanning and self.stats['scanned_ips'] < target_ips:
                while len(ip_batch) < batch_size:
                    ip = self.generate_ip()
                    if ip not in self.stats['active_ips']:
                        ip_batch.append(ip)
                        self.stats['total_ips'] += 1
                
                start_time = time.time()
                found_proxies = await self.mass_scan_optimized(ip_batch)
                scan_time = time.time() - start_time
                
                self.stats['scanned_ips'] += len(ip_batch)
                self.stats['ports_scanned'] += len(ip_batch) * len(self.ports)
                
                ip_batch = []
                
                self.show_progress(scan_time, len(found_proxies))
                await asyncio.sleep(0.001)
                
        except KeyboardInterrupt:
            print("\nScan stopped")
        finally:
            self.scanning = False
            self.show_final_stats()

    def show_progress(self, scan_time, found_count):
        elapsed = time.time() - self.stats['start_time']
        ports_per_sec = self.stats['ports_scanned'] / elapsed if elapsed > 0 else 0
        
        print(f"Speed: {ports_per_sec:,.0f} ports/s | IPs: {self.stats['scanned_ips']} | Found: {self.stats['open_ports']} | Time: {int(elapsed)}s")

    def show_final_stats(self):
        elapsed = time.time() - self.stats['start_time']
        ports_per_sec = self.stats['ports_scanned'] / elapsed if elapsed > 0 else 0
        
        print("\n" + "=" * 50)
        print (r"""

███████╗███████╗██╗     ██╗██╗  ██╗    ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗     ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██║     ██║╚██╗██╔╝    ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝    ██╔════╝ ██╔════╝████╗  ██║
█████╗  █████╗  ██║     ██║ ╚███╔╝     ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝     ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ██╔══╝  ██║     ██║ ██╔██╗     ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝      ██║   ██║██╔══╝  ██║╚██╗██║
██║     ███████╗███████╗██║██╔╝ ██╗    ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║       ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                                                                                
                                                                                                                                
 """)
        print("Scan Completed")
        print("=" * 50)
        print(f"Total proxies: {len(self.found_proxies)}")
        print(f"Total IPs scanned: {self.stats['scanned_ips']}")
        print(f"Total Ports scanned: {self.stats['ports_scanned']:,}")
        print(f"Speed: {ports_per_sec:,.0f} ports/s")
        print(f"Time: {elapsed:.1f}s")
        print("=" * 50)

async def main():
    try:
        scanner = FelixProxyGen()
        await scanner.run_elite_scan(target_ips=3000)
    except KeyboardInterrupt:
        print("\nScan Stopped")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
