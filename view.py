import tkinter as tk


class ScraperGUI:

    def __init__(self, scraper):
        self.scraper = scraper
    
    def GUI(self):
        self.scraper.main()

        HEIGHT = 700
        WIDTH = 800
        root = tk.Tk()


        #First parameter always represent the parent window the widget is placed in
        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()

        frame = tk.Frame(root, bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.3, anchor="n")

        addItemTextBox = tk.Entry(frame, font=40)
        addItemTextBox.place(relwidth=0.65, relheight=0.2)

        #Would normally make a controller class to handle the buttons so we don't get hard dependencies. But it's a small program that I don't intend to extend so kept it easy
        addItemButton = tk.Button(frame, text="Monitor new product", font=40, command=lambda: self.scraper.get_price(addItemTextBox.get(), currentlyMonitoring))
        addItemButton.place(relx=0.7, relwidth=0.3, relheight=0.2)


        deleteItemTextBox = tk.Entry(frame, font=40)
        deleteItemTextBox.place(rely=0.3, relwidth=0.65, relheight=0.2)
        deleteItemButton = tk.Button(frame, text="Stop monitoring product", font=40, command=lambda: self.scraper.delete_item(deleteItemTextBox.get(), currentlyMonitoring))
        deleteItemButton.place(relx=0.7, rely=0.3, relwidth=0.3, relheight=0.2)


        lower_frame = tk.Frame(root, bd=5)
        lower_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor="n")
        #Have to fix displaying the items (check add_items function)

        currentlyMonitoring = tk.Listbox(lower_frame, font=20)
        currentlyMonitoring.pack(fill="x")
        root.mainloop()