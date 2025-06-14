import os
import tkinter as tk
import datetime
from CTkTable import *
from PIL import Image, ImageTk
from customtkinter import *
from AntiSpam_data import alg


class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.name == 'nt':
            self.iconbitmap("AntiSpam_data/icn.ico")
        else:
            icon_image = Image.open("AntiSpam_data/icn.png")
            self.tk_icon = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, self.tk_icon)


        bg_color = self._apply_appearance_mode(self.cget("background"))
        print(bg_color)

        name = CTkLabel(self, text="Проверка сообщения на спам", font=("Arial", 20, "bold"))
        name.pack(padx=10, pady=10, anchor="n")

        # Основной фрейм
        main_frame = CTkFrame(self, fg_color=bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Фрейм для вводо сообщения
        vvod_frame = CTkFrame(main_frame, fg_color=bg_color, border_color="gray", border_width=2, corner_radius=10, height=500)
        vvod_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        l = CTkLabel(vvod_frame, text="Введите сообщение для проверки")
        l.grid(row=0, column=0, padx=5, pady=5)
        l2=CTkLabel(vvod_frame, text="Cообщение должно быть на английском\nВ файле, одна строка - одно сообщение", text_color='gray', font=("Arial", 10), justify="left")
        l2.grid(row=1)

        input_text = CTkTextbox(vvod_frame)
        input_text.grid(row=2, padx=10, sticky="nsew")

        def rezume(val):
            rez = CTkToplevel()
            rez.geometry("400x400")
            rez.title("Отчет по проверке")



            s = CTkScrollableFrame(rez, width=400, height=400)
            s.pack(expand=True, anchor='center')

            l = CTkLabel(s, text='Процент спам слов получен \nиз анализа файла SMSSpamCollection')
            l.pack()

            t = CTkTable(s, values=val)
            t.pack(expand=True, padx=10, pady=10)

        # Проверка сообщения и вывод результата

        def print_text():
            text = input_text.get("1.0", "end-1c")
            is_spam, score = alg.check_spam(text)
            if is_spam:
                ans_text.delete(0.0, 'end')
                ans_text.configure(border_color="red")
                ans_text.insert(END, f"Сообщение: {text}\n\n"+"Вероятность: " + str(int(score*100))+"%")
            else:
                ans_text.delete(0.0, 'end')
                ans_text.configure(border_color="green")
                ans_text.insert(END, f"Сообщение: {text}\n\n"+"Вероятность: " + str(int(score*100))+"%")
            val = [['Слово', "% появления в спаме"]]
            v = alg.spam_words(text)
            for i in v:
                val.append(i)
            rezume(val)



        # Кнопка ввода
        btn_frame = CTkFrame(vvod_frame)
        btn_frame.grid(row=3, padx=10, pady=10, sticky="nsew")

        btn = CTkButton(btn_frame, text="Ввод", command=print_text, width=135, height=35)
        btn.grid(row=0, column=1, padx=5, pady=5)


        # Загрузка текста из файла
        def load_from_file():
            file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[('Text Files', '*.txt'), ('csv','*.csv')])
            file_name = file_path[file_path.rfind("/")+1:]
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.readlines()
                ans_text.delete(0.0, 'end')
                input_text.delete(0.0, 'end')
                input_text.insert(END, "Файл: "+file_name)
                val = [['Слово', "% появления в спаме"]]
                for line in text:
                    spam, score= alg.check_spam(line)
                    ans_text.insert(END, f"Сообщение: {line}")
                    ans_text.insert(END, f"Вероятность спама: {str(int(score*100))}%\n\n")
                    v = alg.spam_words(line)
                    for i in v:
                        val.append(i)
                rezume(val)




        def save_text():
            """Сохраняет содержимое текстового поля в файл"""
            # Получаем текст из виджета
            text_content = ans_text.get("1.0", "end-1c")
            text_content = "Дата записи: "+str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))+"\n"+text_content

            # Открываем диалоговое окно сохранения
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
                title="Сохранить текст как"
            )

            # Если пользователь не отменил диалог
            if file_path:
                try:
                    # Записываем текст в файл
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(text_content)
                except Exception as e:
                    print(e)

        # Кнопка выбора файла
        icon_path = "AntiSpam_data/icn1.png"
        icon = CTkImage(Image.open(icon_path))
        btn_file = CTkButton(btn_frame, width=35, image=icon, text='', command=load_from_file)
        btn_file.grid(row=0, column=0, padx=5, pady=5)

        # Фрейм с ответом
        ans_frame = CTkFrame(main_frame)
        ans_frame.grid(row=1, column=1, padx=10, pady=10)

        ans_text = CTkTextbox(main_frame, border_width=2, border_color="gray", corner_radius=10, width=400)
        ans_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        btnFrame2 = CTkFrame(main_frame, fg_color="transparent")
        btnFrame2.grid(row=2, column=1)

        save_btn = CTkButton(btnFrame2, text="Сохранить", command=save_text)
        save_btn.grid(row=0, column=0, padx=10)



app = App()
app.resizable(False, False)
app.title("AntiSpam")
app.mainloop()