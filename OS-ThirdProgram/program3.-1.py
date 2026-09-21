from collections import deque

processes = [
    {"pid":"P1", "arrival":0, "burst":7, "priority":2},
    {"pid":"P2", "arrival":2, "burst":4, "priority":1},
    {"pid":"P3", "arrival":4, "burst":1, "priority":3},
    {"pid":"P4", "arrival":5, "burst":4, "priority":2}
]

def priority_scheduling(processes):
    current_time = 0
    completed = set()
    result = []

    while len(completed) < len(processes):
        ready = [
            p for p in processes
            if p["arrival"] <= current_time and p["pid"] not in completed
        ]

        if not ready:
            next_time = min(
                p["arrival"] for p in processes
                if p["pid"] not in completed
            )

            result.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        p = min(ready, key=lambda x: x["priority"])
        start = current_time
        current_time += p["burst"]
        result.append((p["pid"], start, current_time))
        completed.add(p["pid"])

    return result


def round_robin(processes, quantum):
    # remaining burst time for each process
    remaining = {p["pid"]: p["burst"] for p in processes}
    procs = sorted(processes, key=lambda x: x["arrival"])

    current_time = 0
    queue = deque()
    result = []
    i = 0  # pointer into procs, for adding new arrivals

    while i < len(procs) and procs[i]["arrival"] <= current_time:
        queue.append(procs[i])
        i += 1

    while queue:
        p = queue.popleft()

        # if it hasn't arrived yet, fast-forward time (shouldn't normally happen)
        if p["arrival"] > current_time:
            current_time = p["arrival"]

        run_time = min(quantum, remaining[p["pid"]])
        start = current_time
        current_time += run_time
        remaining[p["pid"]] -= run_time
        result.append((p["pid"], start, current_time))

        # add any processes that arrived during this run
        while i < len(procs) and procs[i]["arrival"] <= current_time:
            queue.append(procs[i])
            i += 1

        # if this process still has time left, put it back at the end
        if remaining[p["pid"]] > 0:
            queue.append(p)

    return result


if __name__ == "__main__":
    print("Priority Scheduling:")
    for entry in priority_scheduling(processes):
        print(entry)

    print("\nRound Robin (quantum=2):")
    for entry in round_robin(processes, quantum=2):
        print(entry)