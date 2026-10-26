import tkinter as tk
from tkinter import ttk, messagebox


def detect_deadlock(allocation, request, available):
    """
    Detect deadlocks using the OS deadlock detection algorithm.
    Supports multiple instances of each resource type.
    """

    n = len(allocation)
    m = len(available)

    # A process holding no resources can be considered finished.
    finish = [all(value == 0 for value in row) for row in allocation]

    # Work represents currently available resources.
    work = available.copy()
    safe_sequence = []

    while True:
        found = False

        for i in range(n):
            if not finish[i]:
                # Check whether the outstanding request can be satisfied.
                if all(request[i][j] <= work[j] for j in range(m)):
                    # Assume the process completes and releases its resources.
                    work = [
                        work[j] + allocation[i][j]
                        for j in range(m)
                    ]

                    finish[i] = True
                    safe_sequence.append(f"P{i + 1}")
                    found = True

        if not found:
            break

    deadlocked_processes = [
        f"P{i + 1}" for i in range(n) if not finish[i]
    ]

    return safe_sequence, deadlocked_processes


def run_detection():
    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())

        if not (1 <= n <= 10 and 1 <= m <= 10):
            messagebox.showerror(
                "Invalid Input",
                "Enter between 1 and 10 processes and resource types."
            )
            return

        allocation = []
        request = []

        # Read allocation matrix.
        for i in range(n):
            row = [
                int(allocation_entries[i][j].get())
                for j in range(m)
            ]
            allocation.append(row)

        # Read outstanding request matrix.
        for i in range(n):
            row = [
                int(request_entries[i][j].get())
                for j in range(m)
            ]
            request.append(row)

        available = [
            int(available_entries[j].get())
            for j in range(m)
        ]

        # Validate resource counts.
        if any(x < 0 for row in allocation for x in row):
            raise ValueError("Resource values cannot be negative.")

        if any(x < 0 for row in request for x in row):
            raise ValueError("Resource values cannot be negative.")

        if any(x < 0 for x in available):
            raise ValueError("Available resources cannot be negative.")

        sequence, deadlocked = detect_deadlock(
            allocation, request, available
        )

        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        if deadlocked:
            result_box.insert(
                tk.END,
                "⚠ DEADLOCK DETECTED!\n\n"
            )
            result_box.insert(
                tk.END,
                "Processes unable to complete:\n"
                + ", ".join(deadlocked)
                + "\n\n"
            )
            result_box.insert(
                tk.END,
                "These processes cannot finish under the "
                "current resource state."
            )
        else:
            result_box.insert(
                tk.END,
                "✓ NO DEADLOCK DETECTED!\n\n"
            )
            result_box.insert(
                tk.END,
                "All processes can complete.\n\n"
            )
            result_box.insert(
                tk.END,
                "Completion order: "
                + " → ".join(sequence)
            )

        result_box.config(state="disabled")

    except ValueError as error:
        messagebox.showerror(
            "Invalid Input",
            f"Please enter valid non-negative integers.\n{error}"
        )

    except (IndexError, tk.TclError):
        messagebox.showerror(
            "Input Error",
            "Please check the process and resource entries."
        )


def clear_all():
    process_entry.delete(0, tk.END)
    resource_entry.delete(0, tk.END)

    for widget in matrix_frame.winfo_children():
        widget.destroy()

    allocation_entries.clear()
    request_entries.clear()
    available_entries.clear()

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.config(state="disabled")


def create_input_fields():
    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())

        if not (1 <= n <= 10 and 1 <= m <= 10):
            raise ValueError

        for widget in matrix_frame.winfo_children():
            widget.destroy()

        allocation_entries.clear()
        request_entries.clear()
        available_entries.clear()

        tk.Label(
            matrix_frame,
            text="ALLOCATION MATRIX",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, columnspan=m + 1, pady=5)

        tk.Label(matrix_frame, text="Process").grid(
            row=1, column=0, padx=5
        )

        for j in range(m):
            tk.Label(
                matrix_frame,
                text=f"R{j + 1}"
            ).grid(row=1, column=j + 1, padx=5)

        for i in range(n):
            tk.Label(
                matrix_frame,
                text=f"P{i + 1}"
            ).grid(row=i + 2, column=0, padx=5)

            row_entries = []

            for j in range(m):
                entry = tk.Entry(matrix_frame, width=6)
                entry.grid(row=i + 2, column=j + 1, padx=4, pady=3)
                entry.insert(0, "0")
                row_entries.append(entry)

            allocation_entries.append(row_entries)

        start_row = n + 3

        tk.Label(
            matrix_frame,
            text="OUTSTANDING REQUEST MATRIX",
            font=("Arial", 11, "bold")
        ).grid(
            row=start_row,
            column=0,
            columnspan=m + 1,
            pady=(12, 5)
        )

        tk.Label(matrix_frame, text="Process").grid(
            row=start_row + 1, column=0, padx=5
        )

        for j in range(m):
            tk.Label(
                matrix_frame,
                text=f"R{j + 1}"
            ).grid(
                row=start_row + 1, column=j + 1, padx=5
            )

        for i in range(n):
            tk.Label(
                matrix_frame,
                text=f"P{i + 1}"
            ).grid(
                row=start_row + 2 + i,
                column=0,
                padx=5
            )

            row_entries = []

            for j in range(m):
                entry = tk.Entry(matrix_frame, width=6)
                entry.grid(
                    row=start_row + 2 + i,
                    column=j + 1,
                    padx=4,
                    pady=3
                )
                entry.insert(0, "0")
                row_entries.append(entry)

            request_entries.append(row_entries)

        available_row = start_row + n + 3

        tk.Label(
            matrix_frame,
            text="AVAILABLE RESOURCES",
            font=("Arial", 11, "bold")
        ).grid(
            row=available_row,
            column=0,
            columnspan=m + 1,
            pady=(12, 5)
        )

        tk.Label(matrix_frame, text="Available").grid(
            row=available_row + 1,
            column=0,
            padx=5
        )

        for j in range(m):
            entry = tk.Entry(matrix_frame, width=6)
            entry.grid(
                row=available_row + 1,
                column=j + 1,
                padx=4,
                pady=3
            )
            entry.insert(0, "0")
            available_entries.append(entry)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter a valid number of processes and resource types (1–10)."
        )


# Main window
root = tk.Tk()
root.title("Deadlock Detection System")
root.geometry("650x750")

tk.Label(
    root,
    text="DEADLOCK DETECTION SYSTEM",
    font=("Arial", 18, "bold"),
    fg="darkblue"
).pack(pady=10)

top_frame = tk.Frame(root)
top_frame.pack(pady=5)

tk.Label(top_frame, text="Number of Processes:").grid(
    row=0, column=0, padx=5, pady=5
)
process_entry = tk.Entry(top_frame, width=8)
process_entry.grid(row=0, column=1, padx=5)
process_entry.insert(0, "3")

tk.Label(top_frame, text="Resource Types:").grid(
    row=0, column=2, padx=5, pady=5
)
resource_entry = tk.Entry(top_frame, width=8)
resource_entry.grid(row=0, column=3, padx=5)
resource_entry.insert(0, "3")

tk.Button(
    top_frame,
    text="Create Input Fields",
    command=create_input_fields,
    bg="lightblue"
).grid(row=1, column=0, columnspan=4, pady=8)

# Scrollable input area
canvas = tk.Canvas(root, height=370)
scrollbar = ttk.Scrollbar(
    root, orient="vertical", command=canvas.yview
)
matrix_frame = tk.Frame(canvas)

matrix_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=matrix_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
scrollbar.pack(side="right", fill="y")

allocation_entries = []
request_entries = []
available_entries = []

# Controls and result area
controls = tk.Frame(root)
controls.pack(fill="x", pady=8)

tk.Button(
    controls,
    text="Detect Deadlock",
    command=run_detection,
    bg="lightgreen",
    font=("Arial", 11, "bold")
).pack(side="left", padx=20)

tk.Button(
    controls,
    text="Reset",
    command=clear_all,
    bg="lightcoral"
).pack(side="left", padx=10)

tk.Label(
    root,
    text="DETECTION RESULT",
    font=("Arial", 12, "bold")
).pack(pady=5)

result_box = tk.Text(root, height=6, width=65, state="disabled")
result_box.pack(padx=10, pady=(0, 10))

root.mainloop()