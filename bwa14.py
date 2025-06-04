# MALICIOUS TAMPERING WITH THIS PROGRAM'S SOURCE CODE WILL RESULT IN IMMEDIATE TERMINATION AND LEGAL ACTION.

import time
import random
import string
import sys
import msvcrt  # For Windows non-blocking keyboard input
from errorcodes import *
import configparser  # For reading options.cfg

def draw_badge(subtitle="Nuclear Resources"):
    badge = f'''
 ██████╗ ██╗    ██╗██╗     ████████╗███████╗ ██████╗██╗  ██╗
██╔═══██╗██║    ██║██║     ╚══██╔══╝██╔════╝██╔════╝██║  ██║
██║   ██║██║ █╗ ██║██║        ██║   █████╗  ██║     ███████║ 
██║   ██║██║███╗██║██║        ██║   ██╔══╝  ██║     ██╔══██║ 
╚██████╔╝╚███╔███╔╝███████╗   ██║   ███████╗╚██████╗██║  ██║
 ╚═════╝  ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝
                    {subtitle}
'''
    print(badge)

def get_command_partial(timeout=1.0, prompt=""):
    """
    Get keyboard input from user with a timeout, non-blocking.
    Returns the buffer if Enter pressed, or None if timeout.
    Keeps track of what user types.
    """
    start = time.time()
    buffer = ''
    while time.time() - start < timeout:
        while msvcrt.kbhit():
            char = msvcrt.getwche()
            if char == '\r':  # Enter key
                print()
                return buffer.strip().lower()
            elif char == '\b':
                if len(buffer) > 0:
                    buffer = buffer[:-1]
                    # Erase last char on console
                    print('\b \b', end='', flush=True)
            else:
                buffer += char
        time.sleep(0.02)
    # Timeout
    return buffer if buffer else None

if sys.platform == "win32":
    import winsound
    def beep(frequency=1000, duration=100):
        try:
            winsound.Beep(frequency, duration)
        except RuntimeError:
            print("\a", end='')
else:
    def beep(frequency=1000, duration=100):
        print("\a", end='')

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def format_temperature(temp):
    return f"{temp:.1f}°C"

def glitch_text(text, glitchiness=0.01):
    return ''.join(random.choice("#$%&@!?~") if random.random() < glitchiness else c for c in text)

def draw_pressure_gauge(pressure_percent):
    bar_length = 40
    filled_length = int(bar_length * pressure_percent / 100)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\nPressure: |{bar}| {pressure_percent:6.2f}%\n")

def draw_temperature_gauge(temperature_percent, inaccuracy):
    bar_length = 40
    filled_length = int(bar_length * temperature_percent / 1000)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\nTEMP: |{bar}| {format_temperature(temperature_percent+random.randrange(-(inaccuracy),(inaccuracy+1)))}\n")

def draw_airflow_gauge(airflow_percent):
    bar_length = 40
    filled_length = int(bar_length * airflow_percent / 100)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\nAirflow: |{bar}| {airflow_percent:6.2f}%\n")

def clear_screen():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def draw_screen(time_left, reset_allowed, active_errors, reset_threshold,
                show_pressure=False, show_temperature=True, pressure=0.0, temperature=64, inaccuracy=0, flash_on=True,
                maintenance_mode=False, fixing_error=None, fix_progress=0, glitchiness=0.01, fix_message="FIXING",
                show_airflow=True, airflow=50.0):
    reset_color = "\033[0m"
    red_bg = "\033[41m"
    yellow_bg = "\033[43;30m"

    clear_screen()
    draw_badge(glitch_text("Nuclear Resources", glitchiness))

    print("\n--- REACTOR STATUS REPORT ---")
    if show_temperature:
        draw_temperature_gauge(temperature, inaccuracy)
    if show_airflow:
        draw_airflow_gauge(airflow)
    for err_id, error_text, *_ in active_errors:
        is_red = any(tag in error_text for tag in ["[WARN]", "[ERR]"])
        display_text = f"{error_text}"
        if is_red:
            if maintenance_mode or flash_on:
                print(red_bg + glitch_text(display_text, glitchiness) + reset_color)
            else:
                print(" " * len(display_text))
        else:
            print(glitch_text(display_text, glitchiness))

    print("\n" + glitch_text("Reactor Shutdown In: ", glitchiness) + format_time(time_left))

    if reset_allowed:
        print(f"\n{red_bg}" + "#" * 50 + reset_color)
        print(glitch_text(f"{red_bg}!!! EMERGENCY OVERRIDE REQUIRED !!!{reset_color}", glitchiness))
        print(glitch_text(f"{red_bg}Input the sequence to RESET reactor pressure{reset_color}", glitchiness))
        print(glitch_text(f"{red_bg}Failure to reset will result in MELTDOWN{reset_color}", glitchiness))
        print(f"{red_bg}" + "#" * 50 + reset_color + "\n")
    else:
        print(f"\n{yellow_bg}[Reactor must be reset below: {format_time(reset_threshold)}]{reset_color}")

    if show_pressure:
        draw_pressure_gauge(pressure)

    if maintenance_mode and fixing_error:
        bar_length = 30
        filled_length = int(bar_length * fix_progress)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        print(f"\n\033[44m{fix_message}: |{bar}| {fix_progress*100:6.2f}%\033[0m\n")

def startup_sequence():
    clear_screen()
    cyan = "\033[96m"
    reset = "\033[0m"
    print(cyan + "INITIALIZING REACTOR CORE SYSTEMS...\n" + reset)

    def progress_bar(duration, length=30):
        start = time.time()
        while True:
            elapsed = time.time() - start
            progress = min(1.0, elapsed / duration)
            filled = int(length * progress)
            bar = "█" * filled + "-" * (length - filled)
            print(f"\r|{bar}| {progress*100:6.2f}%", end='', flush=True)
            if progress >= 1.0:
                break
            time.sleep(0.05)
        print()

    steps = [
        "Powering up mainframe...",
        "Running diagnostics...",
        "Calibrating sensors...",
        "Activating coolant systems...",
        "Stabilizing control rods...",
        "Initializing safety protocols...",
        "Final system checks..."
    ]
    for step in steps:
        print(step)
        beep(800, 150)
        progress_bar(random.uniform(2, 5))

    print(cyan + "\nREACTOR ONLINE. Standby for countdown...\n" + reset)
    pressure = 0.0
    for _ in range(100):
        clear_screen()
        print(cyan + "REACTOR ONLINE. Standby for countdown...\n" + reset)
        draw_pressure_gauge(pressure)
        pressure += 0.5
        time.sleep(0.05)

def password_protection(password):
    print("\033[31mUNAUTHORIZED ACCESS IS PROHIBITED! \033[0m")
    print()
    attempts = 0
    max_attempts = 3
    print("Unlock manual override for Terminal A-2...")
    while attempts < max_attempts:
        user_input = input("Access Code: ").strip().upper()
        if user_input is None:
            print("\nInput timed out. Exiting...")
            time.sleep(4)
            sys.exit(1)
        if user_input == password:
            print("\033[32mManual override enabled by authorized user on Terminal A-2, logging session now... \033[0m")
            time.sleep(4)
            return True
        else:
            attempts += 1
            print("\033[31m[WARN] Failed authentication during manual override! " + str(max_attempts - attempts) + " attempts remaining. \033[0m")
            beep(500, 300)

def load_config():
    config = configparser.ConfigParser()
    try:
        config.read('options.cfg')
        settings = {
            'difficulty': config.getint('Settings', 'difficulty', fallback=12),
            'difficulty_increases': config.getboolean('Settings', 'difficulty_increases', fallback=True),
            'error_interval_min': config.getfloat('Settings', 'error_interval_min', fallback=20.0),
            'error_interval_max': config.getfloat('Settings', 'error_interval_max', fallback=80.0)
        }
        return settings
    except (configparser.Error, ValueError) as e:
        print(f"[WARN] Error reading options.cfg: {e}")
        print("Using default settings...")
        return {
            'difficulty': 12,
            'difficulty_increases': True,
            'error_interval_min': 20.0,
            'error_interval_max': 80.0
        }

def meltdown_sequence():
    # Placeholder for meltdown sequence logic
    return False

def airflow_check(airflow):
    if airflow < 50.0:
        return True
    return False

def reactor_simulation():
    clear_screen()
    config = load_config()
    total_duration = random.randint(600, 1200)
    reset_threshold = random.randint(120, 230)
    reset_done = False
    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    active_errors = list()
    last_flash = time.time()
    flash_on = True
    temperature = 400.0
    target_temperature = 750.0
    inaccuracy = 0
    difficulty = config['difficulty']
    difficulty_increases = config['difficulty_increases']
    pressure = 0.0
    airflow = 90.0  # Initial airflow percentage
    lag = 0
    fix_message = "FIXING"
    fixing_error = None
    fix_progress = 0.0
    fix_duration = None
    fix_start_time = None
    maintenance_mode = False

    error_interval = random.uniform(config['error_interval_min'], config['error_interval_max'])
    last_error_time = time.time()

    start_time = time.time()
    next_challenge_time = time.time() + random.randint(180, 300)
    challenge_active = False
    challenge_sequence = ''
    challenge_start_time = 0

    if password_protection("OWLTECH123"):
        startup_sequence()
    else:
        return
    
    user_input_buffer = ''

    try:
        while True:
            now = time.time()
            elapsed = now - start_time
            time_left = max(0, int(total_duration - elapsed))

            if time_left == 0:
                break

            if now - last_flash > 0.5:
                flash_on = not flash_on
                last_flash = now

            reset_allowed = time_left <= reset_threshold and not reset_done

            # Timed Sequence Challenge
            if not challenge_active and now >= next_challenge_time:
                challenge_active = True
                challenge_sequence = ''.join(random.choices(string.ascii_uppercase, k=difficulty))
                challenge_start_time = time.time()

                clear_screen()
                beep(400, 200),beep(400, 200),beep(400, 200),
                print("\n\033[93m[OVERRIDE CHALLENGE DETECTED]\033[0m")
                print("Type the following sequence exactly as shown within 45 seconds to boost reactor stability:")
                print(f"\n>>> \033[96m{challenge_sequence}\033[0m <<<\n")
                print("Begin typing:")

                user_input = ''
                while time.time() - challenge_start_time < 45:
                    if msvcrt.kbhit():
                        char = msvcrt.getwche()
                        if char == '\r':
                            break
                        elif char == '\b':
                            if len(user_input) > 0:
                                user_input = user_input[:-1]
                                print('\b \b', end='', flush=True)
                        else:
                            user_input += char.upper()
                    time.sleep(0.01)

                if user_input.strip() == challenge_sequence:
                    print("\n\033[92mSequence correct. Reactor timer extended.\033[0m")
                    total_duration += 90
                    beep(1000, 200)
                    if difficulty_increases:
                        difficulty += 1
                else:
                    print("\n\033[91mIncorrect or incomplete sequence. Reactor time reduced.\033[0m")
                    total_duration -= 90
                    beep(400, 200)

                time.sleep(2)
                next_challenge_time = now + random.randint(180, 300)
                challenge_active = False
                user_input_buffer = ''
                continue  # Force redraw and resume

            # Draw screen
            draw_screen(
                time_left,
                reset_allowed,
                active_errors,
                reset_threshold,
                show_pressure=reset_allowed,
                show_temperature=True,
                pressure=pressure,
                temperature=temperature,
                inaccuracy=inaccuracy,
                flash_on=flash_on,
                maintenance_mode=maintenance_mode,
                fixing_error=fixing_error,
                fix_progress=fix_progress,
                glitchiness=0.01,
                fix_message=fix_message,
                show_airflow=airflow_check(airflow),
                airflow=airflow
            )

            print(f"\n[COMMAND] Type 'reset', 'fix <ID>', or 'exit': {user_input_buffer}", end='', flush=True)

            start_input_time = time.time()
            while time.time() - start_input_time < 1.0:
                while msvcrt.kbhit():
                    char = msvcrt.getwche()
                    if char == '\r':
                        print()
                        command = user_input_buffer.strip().lower()
                        user_input_buffer = ''

                        if command == 'exit':
                            print("Exiting reactor control system.")
                            return
                        elif command == 'reset' and reset_allowed and not reset_done:
                            print(f"Enter emergency override code: {reset_code}")
                            entered = input("Code: ").strip().upper()
                            if entered == reset_code:
                                reset_done = True
                                pressure = 0.0
                                print("Override accepted. Reactor pressure stabilized.")
                                beep(1000, 300)
                                time.sleep(1.0)
                            else:
                                print("Incorrect code.")
                                beep(500, 200)
                        elif command.startswith('fix'):
                            parts = command.split()
                            if len(parts) == 2:
                                error_id = parts[1].upper()
                                match = next((e for e in active_errors if e[0] == error_id), None)
                                if match:
                                    maintenance_mode = True
                                    fixing_error = match
                                    fix_progress = 0.0
                                    fix_duration = random.uniform(5.0, 15.0)
                                    fix_start_time = time.time()
                                    fix_message = match[2].get("fix_message", "FIXING")
                                    print(f"Initiating repair on error (estimated {fix_duration:.1f} seconds)...")
                                    beep(600, 150)
                                else:
                                    print("No such error ID.")
                            else:
                                print("Invalid fix command format. Use 'fix <ID>'.")
                        elif command != '':
                            print("Unknown command.")
                        break
                    elif char == '\b':
                        if len(user_input_buffer) > 0:
                            user_input_buffer = user_input_buffer[:-1]
                            print('\b \b', end='', flush=True)
                    else:
                        user_input_buffer += char
                time.sleep(0.01)

            # Reactor pressure logic
            if reset_allowed:
                pressure += random.uniform(2.0, 5.0)
                if pressure >= 100.0:
                    if not meltdown_sequence():
                        print("\n>>> CORE BREACH. MELTDOWN INEVITABLE. <<<\n")
                        return
                    else:
                        reset_done = True
                        pressure = 0.0
                        beep(1200, 300)
                        time.sleep(1.5)

            # Airflow logic: fluctuates naturally
            airflow += random.uniform(-0.05, 0.1)
            airflow = max(0.0, min(100.0, airflow))  # Clamp between 0% and 100%

            # Temperature logic: climbs if airflow < 25%
            temp_diff = target_temperature - temperature
            if airflow < 25.0:
                temperature += temp_diff * 0.01 + random.uniform(1.0, 3.0)  # Temperature climbs when airflow is low
            else:
                temperature += temp_diff * 0.04 + random.uniform(-0.5, 0.5)
            temperature = max(0.0, min(1200.0, temperature))  # Clamp for realism

            # Gauge-related error triggers
            if pressure > 90.0 and not any(e[0] == "P001" for e in active_errors):
                new_error = ("P001", "[ERR] Critical Pressure Overload", {"temperature": 2.0, "pressure": 5.0, "fix_message": "ADJUSTING PRESSURE VALVES"})
                active_errors.append(new_error)
                beep(700, 100)
            if temperature > 900.0 and not any(e[0] == "T001" for e in active_errors):
                new_error = ("T001", "[ERR] Temperature Exceeding Safe Limits", {"temperature": 5.0, "pressure": 1.0, "fix_message": "COOLING CORE"})
                active_errors.append(new_error)
                beep(700, 100)
            if airflow < 15.0 and not any(e[0] == "A001" for e in active_errors):
                new_error = ("A001", "[ERR] Ventilation Ducts Blockage", {"temperature": 3.0, "airflow": -2.0, "fix_message": "RESTARTING VENTILATION"})
                active_errors.append(new_error)
                beep(700, 100)

            # Apply active error effects
            for err in active_errors:
                if isinstance(err, tuple) and len(err) == 3:
                    _, _, effects = err
                    temperature += effects.get("temperature", 0)
                    pressure += effects.get("pressure", 0)
                    airflow += effects.get("airflow", 0)

            # Error fix progress logic
            if maintenance_mode and fixing_error:
                elapsed_fix = time.time() - fix_start_time
                fix_progress = min(1.0, elapsed_fix / fix_duration)
                if fix_progress >= 1.0:
                    active_errors = [e for e in active_errors if e != fixing_error]
                    fixing_error = None
                    fix_progress = 0.0
                    fix_duration = None
                    fix_start_time = None
                    maintenance_mode = False
                    total_duration += 30
                    beep(1000, 300)
            else:
                # Error cascade: more errors increase chance of new ones
                error_chance = random.uniform(0, 1)
                error_threshold = 0.3 + (len(active_errors) * 0.05)  # More errors, higher chance
                if now - last_error_time > error_interval and len(active_errors) < 10 and error_chance < error_threshold:
                    new_error = random.choice([e for e in ERRORS if e not in active_errors])
                    active_errors.append(new_error)
                    beep(700, 100)
                    last_error_time = now
                    error_interval = random.uniform(config['error_interval_min'], config['error_interval_max'])

    except KeyboardInterrupt:
        print("\nUser aborted simulation.")

    if not reset_done:
        print("\n[FAILURE] Reactor was not reset in time — core meltdown.")
    else:
        print("\n[MISSION SUCCESS] Reactor stabilized. All systems nominal.")

if __name__ == "__main__":
    reactor_simulation()