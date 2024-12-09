import os
import csv
from tkinter import (
    Tk, Label, Button, filedialog, StringVar, ttk, Canvas, PhotoImage, colorchooser, messagebox,Frame
)
from PIL import Image, ImageDraw, ImageFont, ImageTk

#we can create a function main and then import that in the other script
class FlyerGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flyer Generator")
        self.root.state("zoomed")  # Fullscreen mode

        # Variables for user inputs
        self.bg_image_path = StringVar()
        self.csv_path = StringVar()
        self.output_dir = StringVar()
        self.font_size = StringVar(value="36")
        self.text_color = StringVar(value="#000000")
        self.selected_font = StringVar()
        self.selected_graphic = StringVar()
        self.name_coords = StringVar(value="164,1437,817,1528")  # Default coordinates for name
        self.phone_coords = StringVar(value="161,1509,814,1597") # Default coordinates

        # Fonts and graphics options
        self.font_folder = r"font"  # Update with your fonts directory
        self.graphics_folder = r"graphics"  # Update with your graphics directory

        # Fonts and Graphics options
        self.font_options = [os.path.join(self.font_folder, f) for f in os.listdir(self.font_folder) if
                             f.endswith('.ttf')]
        self.graphic_options = [os.path.join(self.graphics_folder, f) for f in os.listdir(self.graphics_folder) if
                                f.endswith(('.png', '.jpg'))]
        self.selected_graphic_thumbnail = None
        self.setup_gui()

    def setup_gui(self):
        # Left Pane for user inputs

        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        Label(left_frame, text="Flyer Generator", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        # Input: Background Image
        ttk.Label(left_frame, text="Background Image:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.bg_image_path, width=40).grid(row=1, column=1, pady=5)
        ttk.Button(left_frame, text="Browse", command=self.load_background_image).grid(row=1, column=2, pady=5)

        # Input: CSV File
        ttk.Label(left_frame, text="CSV File:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.csv_path, width=40).grid(row=2, column=1, pady=5)
        ttk.Button(left_frame, text="Browse", command=self.load_csv_file).grid(row=2, column=2, pady=5)

        # Input: Output Directory
        ttk.Label(left_frame, text="Output Directory:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.output_dir, width=40).grid(row=3, column=1, pady=5)
        ttk.Button(left_frame, text="Browse", command=self.select_output_dir).grid(row=3, column=2, pady=5)

        # Input: Font Options
        ttk.Label(left_frame, text="Font:").grid(row=4, column=0, sticky="w", pady=5)
        font_menu = ttk.Combobox(left_frame, textvariable=self.selected_font, values=self.font_options, state="readonly", width=35)
        font_menu.grid(row=4, column=1, pady=5)

        # Input: Font Size
        ttk.Label(left_frame, text="Font Size:").grid(row=5, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.font_size, width=10).grid(row=5, column=1, pady=5)

        # Input: Text Color
        ttk.Label(left_frame, text="Text Color:").grid(row=6, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.text_color, width=10).grid(row=6, column=1, pady=5)
        ttk.Button(left_frame, text="Choose", command=self.choose_color).grid(row=6, column=2, pady=5)

        # Input: Name Area Coordinates
        ttk.Label(left_frame, text="Name Area (x1, y1, x2, y2):").grid(row=7, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.name_coords, width=40).grid(row=7, column=1, pady=5)

        # Input: Phone Area Coordinates
        ttk.Label(left_frame, text="Phone Area (x1, y1, x2, y2):").grid(row=8, column=0, sticky="w", pady=5)
        ttk.Entry(left_frame, textvariable=self.phone_coords, width=40).grid(row=8, column=1, pady=5)

        # Graphics Section
        Label(left_frame, text="Choose Graphic", font=("Arial", 14)).grid(row=9, column=0, columnspan=2, pady=5)
        graphics_frame = Frame(left_frame, bd=2, relief="groove")
        graphics_frame.grid(row=10, column=0, columnspan=3, pady=5)
        self.display_graphics_thumbnails(graphics_frame)

        # Input: Text Coordinates
        #ttk.Label(left_frame, text="Text Coordinates (x,y):").grid(row=8, column=0, sticky="w", pady=5)
        #ttk.Entry(left_frame, textvariable=self.text_coords, width=20).grid(row=8, column=1, pady=5)


        # Action Buttons
        ttk.Button(left_frame, text="Preview Flyer", command=self.preview_flyer).grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(left_frame, text="Generate Flyers", command=self.generate_flyers).grid(row=10, column=0, columnspan=2, pady=10)

        # Right Pane for live preview
        self.canvas = Canvas(self.root, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
    def display_graphics_thumbnails(self, frame):
        row, column = 0, 0
        for graphic in self.graphic_options:
            img = Image.open(graphic).resize((100, 100), Image.Resampling.LANCZOS)  # Updated Resampling method
            img_tk = ImageTk.PhotoImage(img)

            btn = Button(frame, image=img_tk, command=lambda g=graphic: self.select_graphic(g))
            btn.image = img_tk
            btn.grid(row=row, column=column, padx=5, pady=5)
            column += 1
            if column == 3:
                row += 1
                column = 0
    def select_graphic(self, graphic_path):
        self.selected_graphic.set(graphic_path)
        messagebox.showinfo("Graphic Selected", f"Selected Graphic: {os.path.basename(graphic_path)}")
    def load_background_image(self):
        self.bg_image_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]))

    def load_csv_file(self):
        self.csv_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]))

    def select_output_dir(self):
        self.output_dir.set(filedialog.askdirectory())

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Text Color")[1]
        if color_code:
            self.text_color.set(color_code)



    def preview_flyer(self):
        if not self.bg_image_path.get():
            messagebox.showerror("Error", "Please select a background image.")
            return

        try:
            # Open the background image and convert it to RGBA (for transparency handling)
            bg_image = Image.open(self.bg_image_path.get()).convert("RGBA")

            # Create a drawing object
            draw = ImageDraw.Draw(bg_image)

            # Load the font and text color
            font = ImageFont.truetype(self.selected_font.get(), int(self.font_size.get()))
            text_color = self.text_color.get()

            # Contact details
            name = "Aditya"
            phone = "343482342"

            # Parse coordinates for name and phone text boxes
            name_box = list(map(int, self.name_coords.get().split(",")))
            phone_box = list(map(int, self.phone_coords.get().split(",")))

            # Calculate the available space for text (width and height)
            max_text_width = name_box[1] - name_box[0]
            max_text_height = name_box[3] - name_box[1]

            # Dynamically adjust font size based on space available
            font_size = min(max_text_width, max_text_height) // 2
            font = ImageFont.truetype(self.selected_font.get(), font_size)

            # Calculate bounding boxes for name and phone text
            name_text_box = draw.textbbox((0, 0), name, font=font)
            phone_text_box = draw.textbbox((0, 0), phone, font=font)

            # Calculate center coordinates for name
            name_center_x = (name_box[0] + name_box[2] - name_text_box[2]) // 2
            name_center_y = (name_box[1] + name_box[3] - name_text_box[3]) // 2

            # Calculate center coordinates for phone
            phone_center_x = (phone_box[0] + phone_box[2] - phone_text_box[2]) // 2
            phone_center_y = name_center_y + name_text_box[3] + 10  # Space between name and phone number

            # Draw the name and phone number on the background image
            draw.text((name_center_x, name_center_y), name, fill=text_color, font=font)
            draw.text((phone_center_x, phone_center_y), phone, fill=text_color, font=font)

            # If a graphic is selected, add it to the image
            if self.selected_graphic.get():
                phone_icon = Image.open(self.selected_graphic.get()).convert("RGBA")
                phone_icon_resized = phone_icon.resize((20, 20))  # Resize the icon as needed
                bg_image.paste(phone_icon_resized, (phone_center_x + phone_text_box[2] + 5, phone_center_y),
                               phone_icon_resized)

            # Resize the background image to fit within the canvas size without distortion
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Maintain the aspect ratio when resizing
            img_width, img_height = bg_image.size
            scale_factor = min(canvas_width / img_width, canvas_height / img_height)  # Scale image to fit
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            # Resize the image using high-quality resampling
            bg_image_resized = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert the image to Tkinter format
            bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

            # Update the canvas with the resized background image
            self.canvas.delete("all")  # Clear previous canvas content
            self.canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
            self.canvas.image = bg_image_tk  # Keep reference to avoid garbage collection

        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {e}")



    # Function to sanitize names or symbols in the CSV data

    def generate_flyers(self):
        import re
        def sanitize_input(input_string):
            # Define a pattern to remove unallowed characters (keeping only alphanumeric and spaces)
            sanitized_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
            return sanitized_string

        if not all([self.bg_image_path.get(), self.csv_path.get(), self.output_dir.get()]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        try:
            bg_image = Image.open(self.bg_image_path.get()).convert("RGBA")
            font = ImageFont.truetype(self.selected_font.get(), int(self.font_size.get()))
            output_dir = self.output_dir.get()

            with open(self.csv_path.get(), mode="r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row

                for row in reader:
                    name, phone = row[1], row[2]

                    # Sanitize the name and phone before using them
                    name = sanitize_input(name)
                    phone = sanitize_input(phone)

                    flyer = bg_image.copy()
                    draw = ImageDraw.Draw(flyer)

                    name_box = list(map(int, self.name_coords.get().split(",")))
                    phone_box = list(map(int, self.phone_coords.get().split(",")))

                    # Calculate the available space for text (width and height)
                    max_text_width = name_box[1] - name_box[0]
                    max_text_height = name_box[3] - name_box[1]

                    # Dynamically adjust font size based on space available
                    font_size = min(max_text_width, max_text_height) // 2
                    font = ImageFont.truetype(self.selected_font.get(), font_size)

                    # Calculate bounding boxes for name and phone text
                    name_text_box = draw.textbbox((0, 0), name, font=font)
                    phone_text_box = draw.textbbox((0, 0), phone, font=font)

                    # Calculate center coordinates for name
                    name_center_x = (name_box[0] + name_box[2] - name_text_box[2]) // 2
                    name_center_y = (name_box[1] + name_box[3] - name_text_box[3]) // 2

                    # Calculate center coordinates for phone
                    phone_center_x = (phone_box[0] + phone_box[2] - phone_text_box[2]) // 2
                    phone_center_y = name_center_y + name_text_box[3] + 10  # Space between name and phone number

                    # Draw the name and phone number on the background image
                    draw.text((name_center_x, name_center_y), name, fill=self.text_color.get(), font=font)
                    draw.text((phone_center_x, phone_center_y), phone, fill=self.text_color.get(), font=font)

                    # If a graphic is selected, add it to the image
                    if self.selected_graphic.get():
                        graphic = Image.open(self.selected_graphic.get()).convert("RGBA")

                        # Resize the graphic to match the phone font size (height of the font)
                        graphic_resized = graphic.resize((font_size, font_size))
                        icon_resized = graphic_resized.resize((font_size, font_size))

                        # Position the graphic just to the left of the phone number (2 units away)
                        icon_x = phone_center_x - icon_resized.width - 5 # 5 units of space between graphic and phone number
                        icon_y = phone_center_y - (
                                    icon_resized.height - font_size) // 2  # Align vertically with phone number

                        # Paste the resized icon on the flyer
                        flyer.paste(icon_resized, (icon_x, icon_y), icon_resized) # Align graphic vertically with phone number

                        #flyer.paste(graphic_resized, (icon_x, icon_y), graphic_resized)  # Center vertically with the phone text

                        flyer.paste(graphic_resized, (icon_x, icon_y), graphic_resized)

                    # Save the flyer to the output directory
                    flyer.save(os.path.join(output_dir, f"{name}_flyer.png"))

                messagebox.showinfo("Success", "Flyers generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Flyer generation failed: {e}")


# Run the app
root = Tk()
app = FlyerGeneratorApp(root)
root.mainloop()
