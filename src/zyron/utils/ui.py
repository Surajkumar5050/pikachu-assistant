import os

# ANSI Color Codes
class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.BOLD}{Colors.CYAN}" + "="*60)
    print(f"   ⚡ ZYRON DESKTOP ASSISTANT v1.4 ⚡")
    print(f"   [ Status: ONLINE | Mode: HYBRID | Privacy: 100% ]")
    print("="*60 + f"{Colors.END}\n")

def print_status(icon, message, color=Colors.CYAN):
    print(f"{color}{icon} {message}{Colors.END}")

def print_command(user_query):
    print(f"\n{Colors.YELLOW}🎤 Command received: {Colors.BOLD}'{user_query}'{Colors.END}")

def print_research(query):
    print(f"{Colors.BLUE}🕵️ Researching: {Colors.BOLD}{query}{Colors.END}")

def print_zyron(text):
    print(f"\n{Colors.GREEN}{Colors.BOLD}⚡ Zyron: {Colors.END}{Colors.GREEN}{text}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ Error: {msg}{Colors.END}")

def print_divider():
    print(f"{Colors.CYAN}" + "-"*40 + f"{Colors.END}")
