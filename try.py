import tkinter as tk
from tkinter import ttk
from reportlab.pdfgen import canvas
import itertools
from tkinter import messagebox
from ttkthemes import ThemedTk

class Tire:
    def __init__(self, length, symbol, color):
        self.length = length
        self.symbol = symbol
        self.color = color

class Container:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.filled_space = 0
        self.container = [['-' for _ in range(cols)] for _ in range(rows)]

    def place_tire(self, tire, row, col):
        for i in range(tire.length):
            for j in range(tire.length):
                self.container[row + i][col + j] = tire.symbol
        self.filled_space += tire.length * tire.length

    def can_place_tire(self, tire, row, col):
        for i in range(tire.length):
            for j in range(tire.length):
                r, c = row + i, col + j
                if r >= self.rows or c >= self.cols or self.container[r][c] != '-':
                    return False
        return True

    def is_occupied(self, row, col):
        return self.container[row][col] != '-'

    def get_container(self):
        return self.container

    def get_percentage_filled(self):
        return (self.filled_space / (self.rows * self.cols)) * 100.0

    def get_container(self):
        return [[Tire(1, self.container[i][j], "") if self.container[i][j] != '-' else '-' for j in range(self.cols)] for i in range(self.rows)]


    def calculateAdditionalLength(self, targetPercentage, tireLength):
        targetSpace = (targetPercentage / 100.0) * (self.rows * self.cols)
        remainingEmptySpace = max(targetSpace - self.filled_space, 0.0)
        additionalTires = max(int(remainingEmptySpace / (tireLength * tireLength)), 0)
        return additionalTires
class GUI:

    def __init__(self, root):
        self.root = ThemedTk(theme="arc")  # Apply a different theme (you can choose a theme of your preference)
        self.root.title("Tire Packing Optimizer")

        self.container_frame = ttk.Frame(self.root)
        self.container_frame.grid(row=0, column=0, padx=20, pady=20)

        self.setup()

    def generate_tire_combinations(self, all_tires):
        # Generate combinations of additional tires to suggest
        additional_combinations = []

        for r in range(1, min(len(all_tires), 4) + 1):  # Consider combinations of 1 to 3 additional tires
            additional_combinations.extend(itertools.combinations(all_tires, r))

        return additional_combinations

    def setup(self):
        self.canvas = tk.Canvas(self.container_frame, bg="white", width=600, height=600)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        self.button_frame = ttk.Frame(self.container_frame)
        self.button_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        ttk.Label(self.button_frame, text="Enter the number of rows of the container:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_entry = ttk.Entry(self.button_frame)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.button_frame, text="Enter the number of columns of the container:").grid(row=1, column=0, padx=5, pady=5)
        self.cols_entry = ttk.Entry(self.button_frame)
        self.cols_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.button_frame, text="Enter the number of tires:").grid(row=2, column=0, padx=5, pady=5)
        self.num_tires_entry = ttk.Entry(self.button_frame)
        self.num_tires_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.button_frame, text="Run Optimizer", command=self.run_optimizer).grid(row=3, column=0, columnspan=2, pady=10)
        self.tires = []

    def run_optimizer(self):
        container_rows = self.rows_entry.get()
        container_cols = self.cols_entry.get()
        num_tires = self.num_tires_entry.get()

        if not container_rows.isdigit() or not container_cols.isdigit() or not num_tires.isdigit():
            print("Invalid input. Please enter valid numbers.")
            return

        container_rows = int(container_rows)
        container_cols = int(container_cols)
        num_tires = int(num_tires)

        self.tires = []  # Initialize the list of tires

        for i in range(num_tires):
            length, symbol, color = self.get_tire_info(i + 1)
            try:
                length = int(length)
            except ValueError:
                print(f"Invalid length entered for tire {i + 1}. Please enter a valid number.")
                return
            self.tires.append(Tire(length, symbol, color))  # Save the tires to self.tires

        self.tires.sort(key=lambda x: x.length, reverse=True)

        container = Container(container_rows, container_cols)

        for tire in self.tires:  # Iterate over self.tires instead of tires
            placed = False
            for i in range(container.rows):
                for j in range(container.cols):
                    if container.can_place_tire(tire, i, j):
                        container.place_tire(tire, i, j)
                        placed = True
                        break
                if placed:
                    break

            if not placed:
                print("Cannot fit all tires into the container.")
                return 1

        # Generate recommendations for additional tires
        additional_tires_recommendations = {}
        target_percentage = 90.0
        for tire in self.tires:
            if container.get_percentage_filled() < target_percentage:
                additional_tires = container.calculateAdditionalLength(target_percentage, tire.length)  # Use correct method name
                additional_tires_recommendations[tire.length] = additional_tires
            else:
                break

        # Call save_to_pdf method with recommendations
        self.display_container(container)
        self.save_to_pdf(container, additional_tires_recommendations, "tire_arrangement.pdf")

        print("Tire arrangement and PDF saved.")





    def get_tire_info(self, tire_num):
        while True:
            length = input(f"Enter the length of tire {tire_num}: ")
            symbol = input(f"Enter the symbol of tire {tire_num}: ")
            color = input(f"Enter the color of tire {tire_num}: ")

            if length.isdigit():
                return length, symbol, color
            else:
                print("Invalid input for tire length. Please enter a valid number.")

    def generate_tire_combinations(self, all_tires):
        # Generate combinations of additional tires to suggest
        additional_combinations = []

        for r in range(1, min(len(all_tires), 4) + 1):  # Consider combinations of 1 to 3 additional tires
            additional_combinations.extend(itertools.combinations(all_tires, r))

        return additional_combinations

    def display_container(self, container):
        self.canvas.delete("all")

        cell_size = 40

        # Draw the container outline
        for i in range(container.rows):
            for j in range(container.cols):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

        # Draw the tires inside the container
        for i in range(container.rows):
            for j in range(container.cols):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

                if container.is_occupied(i, j):
                    color = self.rgb_to_hex(container.container[i][j])
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
                    label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.canvas.create_text(label_x, label_y, text=container.container[i][j],
                                            font=("Helvetica", 12, "bold"), fill="white")

    def save_to_pdf(self, container, additional_tires_recommendations, pdf_filename):
        cell_size = 40
        pdf = canvas.Canvas(pdf_filename)

        # Add Title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(300, 800, "Tire Packing Optimizer Report")
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 750, "Container Information:")
        pdf.drawString(50, 650, "Remaining Space:")

        pdf.line(50, 770, 550, 770)

        # Add information about the container at the top of the first page
        pdf.setFont("Helvetica", 14)

        pdf.drawString(50, 730, f"Length of Container: {container.rows}")
        pdf.drawString(50, 710, f"Breadth of Container: {container.cols}")
        pdf.drawString(50, 690, f"The Percentage of container filled: {container.get_percentage_filled():.2f}%")

        # Draw the container outline and tires on the first page
        for i in range(container.rows):
            for j in range(container.cols):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

                # Draw the container outline
                pdf.setStrokeColor("black")
                pdf.setLineWidth(2)
                pdf.rect(x1, y1, cell_size, cell_size)


                # Draw the tires inside the container
                if container.is_occupied(i, j):
                    color = self.rgb_to_hex(container.container[i][j])
                    pdf.setFillColor(color)
                    pdf.rect(x1, y1, cell_size, cell_size, fill=True)
                    label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
                    pdf.setFont("Helvetica", 12)
                    pdf.setFillColor("white")
                    pdf.drawCentredString(label_x, label_y, container.container[i][j])

        # Add information about the remaining empty space in the container on the first page
        remaining_space = (container.rows * container.cols) - container.filled_space
        remaining_percentage = (remaining_space / (container.rows * container.cols)) * 100.0
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor("black")

        pdf.drawString(50, 630, f"Percentage Remaining: {remaining_percentage:.2f}%")

        # Draw a line to separate the tire information and container information
        pdf.line(50, 600, 550, 600)

        # Add information about the tires on the second page
        pdf.showPage()
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 770, "Tire Information:")

        pdf.setFont("Helvetica", 14)


        y_position = 750
        for i, tire in enumerate(self.tires):
            y_position -= 20
            pdf.drawString(50, y_position, f"Tire {i + 1} - Length: {tire.length}, Symbol: {tire.symbol}, Color: {tire.color}")

        # Draw a line to separate the tire information and additional tires recommendations
        pdf.line(50, y_position - 20, 550, y_position - 20)

        # Add recommendations and percentage of container filled after adding each recommended tire on the second page
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position - 40, "Recommended Additional Tires:")

        pdf.setFont("Helvetica", 14)

        y_position -= 60
        for length, count in additional_tires_recommendations.items():
            filled_after_recommendations = (container.filled_space + count * length * length) / (container.rows * container.cols) * 100.0
            pdf.drawString(50, y_position, f"Tire Length: {length}, Count: {count}, Percentage Filled after Recommendation: {filled_after_recommendations:.2f}%")
            y_position -= 20

        # Save the PDF
        pdf.save()







    @staticmethod
    def rgb_to_hex(color):
        color_mapping = {"A": "#FF5E5E", "B": "#5EFF5E", "C": "#5E5EFF", "D": "#FFD700", "E": "#BF3EFF", "F": "#FF69B4"}
        return color_mapping.get(color, "white")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
