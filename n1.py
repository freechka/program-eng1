"""Написать программу вычисления стоимости покупки с учетом скидки. Скидка в 5% предоставляется в
том случае, если сумма покупки больше 600 руб., в 7% – если сумма больше 3000 руб."""
import tkinter as tk
from tkinter import font
from tkinter import messagebox

def check_discount():
    try:
        number = float(summa.get())

        if number > 3000:
            result = number * 0.93  #
            message = "Скидка 7% применена."
        elif number > 600:
            result = number * 0.95
            message = "Скидка 5% применена."
        else:
            result = number
            message = "Скидка не применяется."

        result_label.config(text=f"{message} Итоговая стоимость: {result:.2f} руб.")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите сумму.")

root = tk.Tk()
root.title("Меню")
root.geometry("900x500")

Menu_font = font.Font(family="Impact", size=36, weight="bold")
Cost_font = font.Font(family="Impact", size=24, weight="bold")

label = tk.Label(root, text="Стоимость покупки с учетом скидки", font=Menu_font, fg="white", bg="black")
label.pack(pady=20)

input_label = tk.Label(root, text="Введите сумму:", font = Cost_font)
input_label.pack(pady=10)

summa = tk.Entry(root,  width=30)
summa.pack(pady=30)

check_button = tk.Button(root, text="Проверить", font = Cost_font, command=check_discount, width=10, height=1)
check_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.bind('<Return>', lambda event: check_discount())

root.mainloop()()