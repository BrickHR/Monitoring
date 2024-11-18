import psutil
import time
import os
import platform
import GPUtil
from tabulate import tabulate as tabulate_func
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialisiere colorama für Windows-Kompatibilität
init()


class SystemMonitor:
    def __init__(self):
        self.system = platform.system()
        self.processor = platform.processor()
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())

    def get_size(self, bytes):
        """Konvertiert Bytes in lesbare Einheiten"""
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024

    def get_gpu_info(self):
        """Sammelt GPU Informationen"""
        try:
            gpus = GPUtil.getGPUs()
            gpu_data = []
            for gpu in gpus:
                load_color = Fore.GREEN if gpu.load * 100 < 80 else Fore.RED
                temp_color = Fore.GREEN if gpu.temperature < 75 else Fore.RED
                gpu_data.append([
                    f"{Fore.CYAN}{gpu.name}{Style.RESET_ALL}",
                    f"{load_color}{gpu.load * 100:.1f}%{Style.RESET_ALL}",
                    f"{temp_color}{gpu.temperature}°C{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{gpu.memoryUsed}MB{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{gpu.memoryTotal}MB{Style.RESET_ALL}",
                    f"{Fore.BLUE}{gpu.driver}{Style.RESET_ALL}"
                ])
            return gpu_data
        except:
            return []

    def get_cpu_info(self):
        """Sammelt CPU Informationen"""
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        try:
            cpu_temp = psutil.sensors_temperatures().get('coretemp', [])
        except:
            cpu_temp = []

        cpu_data = []
        for i, percentage in enumerate(cpu_percent):
            usage_color = Fore.GREEN if percentage < 80 else Fore.RED
            freq_color = Fore.BLUE
            temp_str = "N/A"

            if cpu_temp and i < len(cpu_temp):
                temp = cpu_temp[i].current
                temp_color = Fore.GREEN if temp < 75 else Fore.RED
                temp_str = f"{temp_color}{temp}°C{Style.RESET_ALL}"

            cpu_data.append([
                f"{Fore.CYAN}Core {i}{Style.RESET_ALL}",
                f"{usage_color}{percentage}%{Style.RESET_ALL}",
                f"{freq_color}{cpu_freq.current:.2f}MHz{Style.RESET_ALL}",
                temp_str
            ])
        return cpu_data

    def get_memory_info(self):
        """Sammelt RAM Informationen"""
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        usage_color = Fore.GREEN if ram.percent < 80 else Fore.RED
        swap_color = Fore.GREEN if swap.percent < 80 else Fore.RED

        ram_data = [[
            f"{usage_color}{ram.percent}%{Style.RESET_ALL}",
            f"{Fore.YELLOW}{self.get_size(ram.used)}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{self.get_size(ram.total)}{Style.RESET_ALL}",
            f"{swap_color}{swap.percent}%{Style.RESET_ALL}",
            f"{Fore.YELLOW}{self.get_size(swap.used)}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{self.get_size(swap.total)}{Style.RESET_ALL}"
        ]]
        return ram_data

    def get_disk_info(self):
        """Sammelt Festplatten Informationen"""
        disk_data = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_color = Fore.GREEN if usage.percent < 80 else Fore.RED
                disk_data.append([
                    f"{Fore.CYAN}{partition.device}{Style.RESET_ALL}",
                    f"{Fore.BLUE}{partition.mountpoint}{Style.RESET_ALL}",
                    f"{usage_color}{usage.percent}%{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{self.get_size(usage.used)}{Style.RESET_ALL}",
                    f"{Fore.YELLOW}{self.get_size(usage.total)}{Style.RESET_ALL}"
                ])
            except:
                continue
        return disk_data

    def get_network_info(self):
        """Sammelt Netzwerk Informationen"""
        net_io = psutil.net_io_counters()
        return [[
            f"{Fore.YELLOW}{self.get_size(net_io.bytes_sent)}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{self.get_size(net_io.bytes_recv)}{Style.RESET_ALL}",
            f"{Fore.CYAN}{net_io.packets_sent}{Style.RESET_ALL}",
            f"{Fore.CYAN}{net_io.packets_recv}{Style.RESET_ALL}"
        ]]

    def display_info(self):
        """Zeigt alle Systeminformationen an"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            # System Information Header
            print(f"\n{Fore.MAGENTA}=== System Information ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}OS:{Style.RESET_ALL} {self.system}")
            print(f"{Fore.CYAN}CPU Model:{Style.RESET_ALL} {self.processor}")
            print(f"{Fore.CYAN}System Uptime:{Style.RESET_ALL} {datetime.now() - self.boot_time}")

            # GPU Information
            gpu_data = self.get_gpu_info()
            if gpu_data:
                print(f"\n{Fore.MAGENTA}=== GPU Information ==={Style.RESET_ALL}")
                print(tabulate_func(gpu_data,
                                    headers=[f"{Fore.WHITE}Name{Style.RESET_ALL}",
                                             f"{Fore.WHITE}Usage{Style.RESET_ALL}",
                                             f"{Fore.WHITE}Temp{Style.RESET_ALL}",
                                             f"{Fore.WHITE}Memory Used{Style.RESET_ALL}",
                                             f"{Fore.WHITE}Memory Total{Style.RESET_ALL}",
                                             f"{Fore.WHITE}Driver{Style.RESET_ALL}"],
                                    tablefmt='grid'))

            # CPU Information
            print(f"\n{Fore.MAGENTA}=== CPU Information ==={Style.RESET_ALL}")
            print(tabulate_func(self.get_cpu_info(),
                                headers=[f"{Fore.WHITE}Core{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Usage{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Frequency{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Temperature{Style.RESET_ALL}"],
                                tablefmt='grid'))

            # Memory Information
            print(f"\n{Fore.MAGENTA}=== Memory Information ==={Style.RESET_ALL}")
            print(tabulate_func(self.get_memory_info(),
                                headers=[f"{Fore.WHITE}RAM Usage{Style.RESET_ALL}",
                                         f"{Fore.WHITE}RAM Used{Style.RESET_ALL}",
                                         f"{Fore.WHITE}RAM Total{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Swap Usage{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Swap Used{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Swap Total{Style.RESET_ALL}"],
                                tablefmt='grid'))

            # Disk Information
            print(f"\n{Fore.MAGENTA}=== Disk Information ==={Style.RESET_ALL}")
            print(tabulate_func(self.get_disk_info(),
                                headers=[f"{Fore.WHITE}Device{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Mountpoint{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Usage{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Used{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Total{Style.RESET_ALL}"],
                                tablefmt='grid'))

            # Network Information
            print(f"\n{Fore.MAGENTA}=== Network Information ==={Style.RESET_ALL}")
            print(tabulate_func(self.get_network_info(),
                                headers=[f"{Fore.WHITE}Bytes Sent{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Bytes Received{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Packets Sent{Style.RESET_ALL}",
                                         f"{Fore.WHITE}Packets Received{Style.RESET_ALL}"],
                                tablefmt='grid'))

            print(f"\n{Fore.CYAN}Last updated:{Style.RESET_ALL} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"\n{Fore.YELLOW}Drücken Sie Strg+C zum Beenden{Style.RESET_ALL}")
            time.sleep(2)


if __name__ == "__main__":
    try:
        # Überprüfe benötigte Module
        required_modules = {
            'psutil': 'psutil',
            'tabulate': 'tabulate',
            'colorama': 'colorama',
            'GPUtil': 'GPUtil'
        }

        for module, package in required_modules.items():
            try:
                __import__(module)
            except ImportError:
                print(f"Das Modul '{module}' ist nicht installiert.")
                print(f"Bitte installieren Sie es mit: pip install {package}")
                exit(1)

        monitor = SystemMonitor()
        monitor.display_info()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Monitoring beendet.{Style.RESET_ALL}")