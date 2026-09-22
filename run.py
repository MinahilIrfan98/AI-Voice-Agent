"""Ek command se agent (backend) aur web server (frontend) dono chalata hai.

Use: uv run run.py
Band karne ke liye Ctrl+C dabao.
"""
import subprocess
import sys

procs = [
    subprocess.Popen([sys.executable, "agent.py", "dev"]),
    subprocess.Popen([sys.executable, "server.py"]),
]

print("\nAgent aur server chal rahe hain.")
print("Browser mein kholo: http://127.0.0.1:8000")
print("Band karne ke liye Ctrl+C dabao.\n")

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    pass
finally:
    for p in procs:
        if p.poll() is None:
            p.terminate()