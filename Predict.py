from keras.models import load_model
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import win32gui

# Load the trained model from file
try:
    model = load_model('mnist.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def predict_digit(img):
    if model is None:
        return "Model not loaded", 0

    img = img.resize((28, 28))  # Resize the image to 28x28 pixels
    img = img.convert('L')  # Convert the image to grayscale
    img = np.array(img)  # Convert the image to a NumPy array
    img = img.reshape(1, 28, 28, 1)  # Reshape the array to match the model input shape
    img = img / 255.0  # Normalize the pixel values to the range [0, 1]

    # Debugging: Print the shape and min/max of the image data
    print(f"Image shape: {img.shape}")
    print(f"Image min: {np.min(img)}, max: {np.max(img)}")

    # Predict the digit using the model
    res = model.predict(img)[0]
    print(f"Prediction result: {res}")

    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=200, height=200, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Analyzing..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Classify", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        # Layout the UI elements
        self.canvas.grid(row=0, column=0, pady=2, sticky=tk.W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # Bind the canvas to the draw_lines method for drawing
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        # Clear the canvas
        self.canvas.delete("all")

    def classify_handwriting(self):
        # Get the coordinates of the canvas widget
        Hd = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(Hd)
        print(f"Rectangle coordinates: {rect}")  # Debugging line
        
        # Capture the drawn image from the canvas
        im = ImageGrab.grab(rect)
        
        # Debugging: Show the captured image
        im.show()
        
        # Predict the digit and accuracy
        digit, acc = predict_digit(im)
        self.label.configure(text=f'{digit}, {int(acc*100)}%')

    def draw_lines(self, event):
        # Draw a circle (representing a line) on the canvas
        r = 8
        self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='black')

# Create and run the application
app = App()
app.mainloop()
