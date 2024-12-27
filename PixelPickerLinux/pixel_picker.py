import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Uses pillow python module


def view_help():
    messagebox.showinfo(
        "Help",
        "Open an image file. \n\n"
        "Plenty of useful shortcuts. \n\n"
        "Ctrl+P activates pixel picking mode. \n\n"
        "Clicking on a pixel in this mode gives you the co-ordinates and RGB values. \n\n"
        "Happy picking."
    )


def show_about():
    messagebox.showinfo(
        "About",
        f"         PixelPicker\nA Simple Image Viewer\n"
        f"      Created by MrJ\n             2024"
    )


class PixelPicker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PixelPicker")
        self.geometry("1024x576")

        self.image_path = None
        self.image = None
        self.tk_image = None
        self.zoom_factor = 1.0
        self.canvas = None
        self.canvas_frame = None
        self.scrollbar_y = None
        self.scrollbar_x = None
        self.is_pixel_picking = False

        self.create_menu()
        self.create_ui()

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit_program, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl+Shift+Plus")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+Minus")
        menu_bar.add_cascade(label="View", menu=view_menu)

        # Details menu
        details_menu = tk.Menu(menu_bar, tearoff=0)
        details_menu.add_command(label="Position & Color", command=self.get_color_and_position, accelerator="Ctrl+P")
        menu_bar.add_cascade(label="Details", menu=details_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View Help", command=view_help)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=show_about)

        self.config(menu=menu_bar)

        # Bind keyboard shortcuts
        self.bind_all("<Control-o>", self.open_image)
        self.bind_all("<Control-q>", self.quit_program)
        self.bind_all("<Control-plus>", self.zoom_in)
        self.bind_all("<Control-minus>", self.zoom_out)
        self.bind_all("<Control-p>", self.get_color_and_position)

    def create_ui(self):
        # Create a frame for the canvas and scrollbars
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True)

        # Create the Canvas widget
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add vertical and horizontal scrollbars
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Link the scrollbars to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Configure the grid weight to allow resizing
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # Bind mouse wheel to scroll vertically (works across both Windows and Linux)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)  # Linux support
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)  # Linux support

    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.canvas.yview_scroll(1, "units")

    def open_image(self, event=None):
        # Open file dialog to choose image
        self.image_path = filedialog.askopenfilename(filetypes=[
            ("All Files", "*.*"),
            ("JPG Files", "*.jpg"),
            ("JPEG Files", "*.jpeg"),
            ("PNG Files", "*.png"),
            ("BMP Files", "*.bmp"),
            ("GIF Files", "*.gif")
        ])
        if self.image_path:
            self.load_image()

    def load_image(self):
        try:
            # Open the image using Pillow (supporting PNG, JPG, GIF, etc.)
            self.image = Image.open(self.image_path)

            # Convert image to RGB (remove the alpha channel if present)
            self.image = self.image.convert('RGB')

            self.zoom_factor = 1.0
            self.display_image()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {e}")

    def display_image(self):
        if not self.image:
            return

        # Resize image based on zoom factor
        width, height = self.image.size
        new_width = int(width * self.zoom_factor)
        new_height = int(height * self.zoom_factor)

        resized_image = self.image.resize((new_width, new_height))
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # Clear the canvas and display the new image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Update scroll region based on the image size
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self, event=None):
        # Increase zoom factor and update display
        self.zoom_factor *= 1.1
        self.display_image()

    def zoom_out(self, event=None):
        # Decrease zoom factor and update display
        self.zoom_factor /= 1.1
        self.display_image()

    def get_color_and_position(self, event=None):
        # Set the pixel picking mode state
        self.is_pixel_picking = True
        self.canvas.config(cursor="crosshair")  # Change cursor to crosshair
        # Set up the click event to get pixel info
        self.canvas.bind("<Button-1>", self.show_pixel_info)

    def show_pixel_info(self, event):
        if not self.is_pixel_picking:
            return

        # Get the coordinates of the click relative to the canvas
        x = event.x
        y = event.y

        # Get the scroll position of the canvas
        canvas_scroll_x = self.canvas.canvasx(0)  # Horizontal scroll position
        canvas_scroll_y = self.canvas.canvasy(0)  # Vertical scroll position

        # Convert the canvas click position to the original image coordinates
        original_x = (x + canvas_scroll_x) / self.zoom_factor
        original_y = (y + canvas_scroll_y) / self.zoom_factor

        # Ensure the original coordinates are within the bounds of the image
        if 0 <= original_x < self.image.width and 0 <= original_y < self.image.height:
            # Get the RGB values of the clicked pixel (no alpha channel)
            pixel_color = self.image.getpixel((int(original_x), int(original_y)))
            # Show the pixel info in the new window
            self.show_pixel_info_window(f"({int(original_x)}, {int(original_y)})", f"{pixel_color}")
        else:
            messagebox.showwarning("Warning", "Clicked outside the image area!")

        # After picking the pixel, turn off pixel picking mode
        self.is_pixel_picking = False
        self.canvas.config(cursor="")  # Reset cursor to default
        self.canvas.unbind("<Button-1>")  # Unbind click event

    def show_pixel_info_window(self, position, color):
        # Create a new top-level window to display the pixel information
        info_window = tk.Toplevel(self)
        info_window.title("Pixel Information")

        # Bring the new window into focus
        info_window.focus_force()

        # Create and place position entry widget
        tk.Label(info_window, text="Position:").grid(row=0, column=0, padx=10, pady=10)
        position_entry = tk.Entry(info_window, width=40)
        position_entry.insert(0, position)  # Pre-fill with the position
        position_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create and place color entry widget
        tk.Label(info_window, text="Color:").grid(row=1, column=0, padx=10, pady=10)
        color_entry = tk.Entry(info_window, width=40)
        color_entry.insert(0, color)  # Pre-fill with the color
        color_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add a close button to the pixel info window
        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.grid(row=2, columnspan=2, pady=10)  # Place button below the entries

    def quit_program(self, event=None):
        # Gracefully exit the program
        self.quit()


if __name__ == "__main__":
    app = PixelPicker()
    app.mainloop()
