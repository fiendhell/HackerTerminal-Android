import flet as ft
import random

def main(page: ft.Page):
    page.title = "HackerTerminal"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.padding = 20

    # Состояние игры
    trace = 0
    credits = 0
    targets = ["192.168.1.10", "10.0.0.55", "172.16.0.99"]
    current_target = ""
    firewall_down = False

    # UI элементы
    output = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    input_field = ft.TextField(
        hint_text="> enter command...",
        autofocus=True,
        bgcolor="#111111",
        color="#00ff00",
        border_color="#333333",
        on_submit=lambda e: process_command(e.control.value)
    )

    def log(msg, color="#00ff00"):
        output.controls.append(ft.Text(msg, color=color, font_family="monospace", size=14))
        page.update()

    def process_command(cmd):
        nonlocal trace, credits, targets, current_target, firewall_down
        cmd = cmd.strip().lower()
        input_field.value = ""
        log(f"> {cmd}", "#00ffff")

        if cmd == "help":
            log("Commands: scan, connect [IP], crack, download, clear", "#ffff00")
        elif cmd == "scan":
            log("Scanning network...", "#00ff00")
            log(f"Found: {targets}", "#00ff00")
        elif cmd.startswith("connect "):
            ip = cmd.replace("connect ", "")
            if ip in targets:
                current_target = ip
                firewall_down = False
                log(f"Connected to {ip}", "#00ff00")
            else:
                log("Target not found.", "#ff0000")
        elif cmd == "crack":
            if not current_target:
                log("No target connected.", "#ff0000")
            elif firewall_down:
                log("Firewall already down.", "#ffff00")
            else:
                if random.randint(0, 100) > 40:
                    firewall_down = True
                    log("Firewall breached!", "#00ff00")
                else:
                    trace += 20
                    log(f"Crack failed. Trace: {trace}%", "#ff0000")
                    if trace >= 100:
                        log("TRACE COMPLETE. BUSTED.", "#ff0000")
        elif cmd == "download":
            if firewall_down and current_target:
                loot = random.randint(50, 150)
                credits += loot
                log(f"Data stolen! +{loot} credits. Total: {credits}", "#00ff00")
                targets.remove(current_target)
                current_target = ""
                firewall_down = False
            else:
                log("Cannot download. Firewall up or no target.", "#ff0000")
        elif cmd == "clear":
            output.controls.clear()
        else:
            log("Unknown command.", "#ff0000")
        page.update()

    log("HACKER TERMINAL v1.0", "#00ff00")
    log("Type 'help' for commands.", "#888888")

    page.add(
        ft.Container(
            content=ft.Column([output, input_field], expand=True),
            expand=True
        )
    )

ft.app(target=main)
