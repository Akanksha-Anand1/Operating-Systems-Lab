def get_processes():
    """Accept Process ID, Arrival Time and Burst Time from the user,
    with validation. Returns a list of process dictionaries."""
    processes = []
    used_pids = set()

    n = int(input("Enter number of processes: "))

    for i in range(n):
        print(f"\nProcess {i + 1}")

        # ---- Validate Process ID ----
        while True:
            pid = input("  Enter Process ID (e.g., P1): ").strip()
            if pid == "":
                print("  Error: Process ID cannot be empty. Try again.")
            elif pid in used_pids:
                print("  Error: Process ID already used. Try again.")
            else:
                used_pids.add(pid)
                break

        # ---- Validate Arrival Time ----
        while True:
            try:
                arrival = int(input("  Enter Arrival Time: "))
                if arrival < 0:
                    print("  Error: Arrival Time cannot be negative.")
                else:
                    break
            except ValueError:
                print("  Error: Please enter a whole number.")

        # ---- Validate Burst Time ----
        while True:
            try:
                burst = int(input("  Enter Burst Time: "))
                if burst <= 0:
                    print("  Error: Burst Time must be greater than 0.")
                else:
                    break
            except ValueError:
                print("  Error: Please enter a whole number.")

        processes.append({"pid": pid, "arrival": arrival, "burst": burst})

    return processes


def fcfs(process_list):
    current_time = 0
    intervals = []
    ordered = sorted(
        process_list,
        key=lambda p: (p["arrival"], p["pid"])
    )
    for process in ordered:
        if current_time < process["arrival"]:
            intervals.append(("IDLE", current_time, process["arrival"]))
            current_time = process["arrival"]
        start = current_time
        end = start + process["burst"]
        intervals.append((process["pid"], start, end))
        current_time = end
    return intervals


def sjf(process_list):
    remaining = process_list.copy()
    current_time = 0
    intervals = []
    while remaining:
        ready = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]
        if not ready:
            next_arrival = min(p["arrival"] for p in remaining)
            intervals.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = min(
            ready,
            key=lambda p: (p["burst"], p["arrival"], p["pid"])
        )
        start = current_time
        end = start + process["burst"]
        intervals.append((process["pid"], start, end))
        current_time = end
        remaining.remove(process)
    return intervals


def show_result(title, intervals):
    print("\n" + title)
    print("Process   Start   End")
    sequence = []
    for pid, start, end in intervals:
        print(f"{pid:<9} {start:<7} {end}")
        if pid != "IDLE":
            sequence.append(pid)
    print("Sequence:", " -> ".join(sequence))


def show_input_table(processes):
    print("\nINPUT PROCESSES")
    print("PID   AT    BT")
    for p in processes:
        print(f'{p["pid"]:<5} {p["arrival"]:<5} {p["burst"]}')


# ---- Main Program ----
original_processes = get_processes()   # original data, entered once

show_input_table(original_processes)

# Preserve original data: pass copies so scheduling functions
# never modify the original list/dictionaries
show_result("FCFS SCHEDULING", fcfs(original_processes.copy()))
show_result("SJF SCHEDULING", sjf(original_processes.copy()))