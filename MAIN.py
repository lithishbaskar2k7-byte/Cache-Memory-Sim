import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from cache import Cache
from simulator import SimulationHistory


class CacheSimulatorApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Cache Memory Simulator")

        self.root.geometry("1200x750")

        self.cache = None

        self.history = SimulationHistory()

        self.create_variables()

        self.create_gui()

    # ==================================================
    # VARIABLES
    # ==================================================

    def create_variables(self):

        self.memory_size_var = tk.StringVar(value="64")

        self.cache_size_var = tk.StringVar(value="16")

        self.block_size_var = tk.StringVar(value="4")

        self.mapping_var = tk.StringVar(
            value="Direct Mapping"
        )

        self.replacement_var = tk.StringVar(
            value="LRU"
        )

        self.associativity_var = tk.StringVar(
            value="2"
        )

        self.address_var = tk.StringVar()

        self.result_var = tk.StringVar(
            value="Ready"
        )

        self.tag_var = tk.StringVar(value="-")

        self.index_var = tk.StringVar(value="-")

        self.offset_var = tk.StringVar(value="-")

        self.block_var = tk.StringVar(value="-")

        self.line_var = tk.StringVar(value="-")

        self.hits_var = tk.StringVar(value="0")

        self.misses_var = tk.StringVar(value="0")

        self.hit_rate_var = tk.StringVar(
            value="0.00%"
        )

        self.miss_rate_var = tk.StringVar(
            value="0.00%"
        )

    # ==================================================
    # CREATE GUI
    # ==================================================

    def create_gui(self):

        title = tk.Label(
            self.root,
            text="CACHE MEMORY SIMULATOR",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)

        main_frame = ttk.Frame(self.root)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=15
        )

        # ==================================================
        # CACHE CONFIGURATION
        # ==================================================

        config_frame = ttk.LabelFrame(
            main_frame,
            text="Cache Configuration"
        )

        config_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            config_frame,
            text="Main Memory:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        ttk.Entry(
            config_frame,
            textvariable=self.memory_size_var,
            width=10
        ).grid(
            row=0,
            column=1
        )

        ttk.Label(
            config_frame,
            text="Cache Size:"
        ).grid(
            row=0,
            column=2
        )

        ttk.Entry(
            config_frame,
            textvariable=self.cache_size_var,
            width=10
        ).grid(
            row=0,
            column=3
        )

        ttk.Label(
            config_frame,
            text="Block Size:"
        ).grid(
            row=0,
            column=4
        )

        ttk.Entry(
            config_frame,
            textvariable=self.block_size_var,
            width=10
        ).grid(
            row=0,
            column=5
        )

        # Mapping

        ttk.Label(
            config_frame,
            text="Mapping:"
        ).grid(
            row=1,
            column=0
        )

        mapping_combo = ttk.Combobox(
            config_frame,
            textvariable=self.mapping_var,
            values=[
                "Direct Mapping",
                "Fully Associative",
                "Set Associative"
            ],
            state="readonly",
            width=18
        )

        mapping_combo.grid(
            row=1,
            column=1
        )

        mapping_combo.bind(
            "<<ComboboxSelected>>",
            self.mapping_changed
        )

        # Replacement

        ttk.Label(
            config_frame,
            text="Replacement:"
        ).grid(
            row=1,
            column=2
        )

        ttk.Combobox(
            config_frame,
            textvariable=self.replacement_var,
            values=[
                "LRU",
                "FIFO",
                "Random"
            ],
            state="readonly",
            width=15
        ).grid(
            row=1,
            column=3
        )

        # Associativity

        ttk.Label(
            config_frame,
            text="Associativity:"
        ).grid(
            row=1,
            column=4
        )

        self.associativity_combo = ttk.Combobox(
            config_frame,
            textvariable=self.associativity_var,
            values=[
                "2",
                "4",
                "8"
            ],
            state="disabled",
            width=10
        )

        self.associativity_combo.grid(
            row=1,
            column=5
        )

        # Create cache button

        ttk.Button(
            config_frame,
            text="CREATE CACHE",
            command=self.create_cache
        ).grid(
            row=0,
            column=6,
            rowspan=2,
            padx=20
        )

        # ==================================================
        # MEMORY ACCESS
        # ==================================================

        access_frame = ttk.LabelFrame(
            main_frame,
            text="Memory Access"
        )

        access_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            access_frame,
            text="Memory Address:"
        ).pack(
            side="left",
            padx=10
        )

        ttk.Entry(
            access_frame,
            textvariable=self.address_var,
            width=20
        ).pack(
            side="left"
        )

        ttk.Button(
            access_frame,
            text="ACCESS MEMORY",
            command=self.access_memory
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            access_frame,
            text="RESET",
            command=self.reset_simulation
        ).pack(
            side="left"
        )

        # ==================================================
        # ADDRESS BREAKDOWN
        # ==================================================

        breakdown_frame = ttk.LabelFrame(
            main_frame,
            text="Address Breakdown"
        )

        breakdown_frame.pack(
            fill="x",
            pady=5
        )

        self.create_info_box(
            breakdown_frame,
            "TAG",
            self.tag_var,
            0
        )

        self.create_info_box(
            breakdown_frame,
            "INDEX",
            self.index_var,
            1
        )

        self.create_info_box(
            breakdown_frame,
            "OFFSET",
            self.offset_var,
            2
        )

        self.create_info_box(
            breakdown_frame,
            "BLOCK",
            self.block_var,
            3
        )

        self.create_info_box(
            breakdown_frame,
            "CACHE LINE",
            self.line_var,
            4
        )

        # ==================================================
        # RESULT
        # ==================================================

        result_frame = ttk.LabelFrame(
            main_frame,
            text="Result"
        )

        result_frame.pack(
            fill="x",
            pady=5
        )

        self.result_label = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 20, "bold"),
            pady=10
        )

        self.result_label.pack()

        # ==================================================
        # CACHE TABLE
        # ==================================================

        cache_frame = ttk.LabelFrame(
            main_frame,
            text="Cache Contents"
        )

        cache_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        columns = (
            "line",
            "valid",
            "tag",
            "block",
            "data",
            "last"
        )

        self.cache_table = ttk.Treeview(
            cache_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "line": "Line",
            "valid": "Valid",
            "tag": "Tag",
            "block": "Block",
            "data": "Data",
            "last": "Last Used"
        }

        for column in columns:

            self.cache_table.heading(
                column,
                text=headings[column]
            )

            self.cache_table.column(
                column,
                anchor="center",
                width=120
            )

        self.cache_table.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # STATISTICS
        # ==================================================

        stats_frame = ttk.LabelFrame(
            main_frame,
            text="Statistics"
        )

        stats_frame.pack(
            fill="x",
            pady=5
        )

        self.create_stat_box(
            stats_frame,
            "HITS",
            self.hits_var,
            0
        )

        self.create_stat_box(
            stats_frame,
            "MISSES",
            self.misses_var,
            1
        )

        self.create_stat_box(
            stats_frame,
            "HIT RATE",
            self.hit_rate_var,
            2
        )

        self.create_stat_box(
            stats_frame,
            "MISS RATE",
            self.miss_rate_var,
            3
        )

        ttk.Button(
            stats_frame,
            text="SHOW GRAPH",
            command=self.show_graph
        ).grid(
            row=0,
            column=4,
            padx=30
        )

    # ==================================================
    # INFO BOX
    # ==================================================

    def create_info_box(
        self,
        parent,
        title,
        variable,
        column
    ):

        frame = ttk.Frame(parent)

        frame.grid(
            row=0,
            column=column,
            padx=40,
            pady=10
        )

        ttk.Label(
            frame,
            text=title,
            font=("Arial", 10, "bold")
        ).pack()

        ttk.Label(
            frame,
            textvariable=variable,
            font=("Arial", 16)
        ).pack()

    # ==================================================
    # STATISTICS BOX
    # ==================================================

    def create_stat_box(
        self,
        parent,
        title,
        variable,
        column
    ):

        frame = ttk.Frame(parent)

        frame.grid(
            row=0,
            column=column,
            padx=35,
            pady=8
        )

        ttk.Label(
            frame,
            text=title
        ).pack()

        ttk.Label(
            frame,
            textvariable=variable,
            font=("Arial", 16, "bold")
        ).pack()

    # ==================================================
    # MAPPING CHANGE
    # ==================================================

    def mapping_changed(self, event=None):

        if self.mapping_var.get() == "Set Associative":

            self.associativity_combo.config(
                state="readonly"
            )

        else:

            self.associativity_combo.config(
                state="disabled"
            )

    # ==================================================
    # CREATE CACHE
    # ==================================================

    def create_cache(self):

        try:

            memory_size = int(
                self.memory_size_var.get()
            )

            cache_size = int(
                self.cache_size_var.get()
            )

            block_size = int(
                self.block_size_var.get()
            )

            mapping = self.mapping_var.get()

            replacement = self.replacement_var.get()

            associativity = int(
                self.associativity_var.get()
            )

            self.cache = Cache(
                memory_size,
                cache_size,
                block_size,
                mapping,
                replacement,
                associativity
            )

            self.history.clear()

            self.update_statistics()

            self.update_cache_table()

            self.result_var.set(
                "Cache created successfully"
            )

            self.result_label.config(
                fg="black"
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==================================================
    # ACCESS MEMORY
    # ==================================================

    def access_memory(self):

        if self.cache is None:

            messagebox.showwarning(
                "Warning",
                "Create the cache first."
            )

            return

        try:

            address = int(
                self.address_var.get()
            )

            result = self.cache.access(
                address
            )

            self.history.add(
                result
            )

            self.tag_var.set(
                str(result["tag"])
            )

            self.index_var.set(
                "-"
                if result["index"] is None
                else str(result["index"])
            )

            self.offset_var.set(
                str(result["offset"])
            )

            self.block_var.set(
                str(result["block"])
            )

            self.line_var.set(
                str(result["line"])
            )

            if result["result"] == "HIT":

                self.result_var.set(
                    f"CACHE HIT ✓   Data = {result['data']}"
                )

                self.result_label.config(
                    fg="green"
                )

            else:

                if result["replaced"]:

                    self.result_var.set(
                        f"CACHE MISS ✗   "
                        f"Block {result['block']} "
                        f"replaced Block "
                        f"{result['old_block']}"
                    )

                else:

                    self.result_var.set(
                        f"CACHE MISS ✗   "
                        f"Block {result['block']} loaded"
                    )

                self.result_label.config(
                    fg="red"
                )

            self.update_statistics()

            self.update_cache_table()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Address",
                str(error)
            )

    # ==================================================
    # UPDATE CACHE TABLE
    # ==================================================

    def update_cache_table(self):

        for item in self.cache_table.get_children():

            self.cache_table.delete(item)

        if self.cache is None:

            return

        for index, line in enumerate(
            self.cache.lines
        ):

            valid = (
                "1"
                if line.valid
                else "0"
            )

            tag = (
                str(line.tag)
                if line.valid
                else "-"
            )

            block = (
                str(line.block)
                if line.valid
                else "-"
            )

            data = (
                str(line.data)
                if line.valid
                else "-"
            )

            last = (
                str(line.last_used)
                if line.valid
                else "-"
            )

            self.cache_table.insert(
                "",
                "end",
                values=(
                    index,
                    valid,
                    tag,
                    block,
                    data,
                    last
                )
            )

    # ==================================================
    # UPDATE STATISTICS
    # ==================================================

    def update_statistics(self):

        if self.cache is None:

            return

        self.hits_var.set(
            str(self.cache.hits)
        )

        self.misses_var.set(
            str(self.cache.misses)
        )

        self.hit_rate_var.set(
            f"{self.cache.get_hit_rate():.2f}%"
        )

        self.miss_rate_var.set(
            f"{self.cache.get_miss_rate():.2f}%"
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset_simulation(self):

        if self.cache is not None:

            self.cache.reset()

        self.history.clear()

        self.address_var.set("")

        self.tag_var.set("-")

        self.index_var.set("-")

        self.offset_var.set("-")

        self.block_var.set("-")

        self.line_var.set("-")

        self.result_var.set("Ready")

        self.result_label.config(
            fg="black"
        )

        self.update_statistics()

        self.update_cache_table()

    # ==================================================
    # GRAPH
    # ==================================================

    def show_graph(self):

        if self.cache is None:

            messagebox.showwarning(
                "Warning",
                "Create the cache first."
            )

            return

        if (
            self.cache.hits
            + self.cache.misses
            == 0
        ):

            messagebox.showwarning(
                "Warning",
                "Access some addresses first."
            )

            return

        labels = [
            "Cache Hits",
            "Cache Misses"
        ]

        values = [
            self.cache.hits,
            self.cache.misses
        ]

        plt.figure(
            figsize=(7, 5)
        )

        plt.bar(
            labels,
            values
        )

        plt.title(
            "Cache Performance"
        )

        plt.ylabel(
            "Number of Accesses"
        )

        for i, value in enumerate(values):

            plt.text(
                i,
                value + 0.1,
                str(value),
                ha="center"
            )

        plt.tight_layout()

        plt.show()


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CacheSimulatorApp(root)

    root.mainloop()