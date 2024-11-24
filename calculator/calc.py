import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE38
        self.color = ft.colors.WHITE


class DigitButton_else(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE




class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 3200  # 横幅
        self.height = 1800  # 横幅
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),

                ## 1行目
                ##　新たにボタンを追加すえれば新しい列ができる

                ft.Row(
                    controls=[
                        DigitButton_else(text="(", button_clicked=self.button_clicked),
                        DigitButton_else(text=")", button_clicked=self.button_clicked),
                        DigitButton_else(text="mc", button_clicked=self.button_clicked),
                        DigitButton_else(text="m+", button_clicked=self.button_clicked),
                        DigitButton_else(text="m-", button_clicked=self.button_clicked),
                        DigitButton_else(text="mr", button_clicked=self.button_clicked),
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),

                ## 2行目

                ft.Row(
                    controls=[
                        DigitButton_else(text="2^nd", button_clicked=self.button_clicked),
                        DigitButton_else(text="X^2", button_clicked=self.button_clicked),
                        DigitButton_else(text="X^3", button_clicked=self.button_clicked),
                        DigitButton_else(text="X^y", button_clicked=self.button_clicked),
                        DigitButton_else(text="e^x", button_clicked=self.button_clicked),
                        DigitButton_else(text="10^x", button_clicked=self.button_clicked),
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),

                ## 3行目

                ft.Row(
                    controls=[
                        DigitButton_else(text="1/X", button_clicked=self.button_clicked),
                        DigitButton_else(text="2√x", button_clicked=self.button_clicked),
                        DigitButton_else(text="3√x", button_clicked=self.button_clicked),
                        DigitButton_else(text="y√x", button_clicked=self.button_clicked),
                        DigitButton_else(text="In", button_clicked=self.button_clicked),
                        DigitButton_else(text="log10", button_clicked=self.button_clicked),
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),

                ## 4行目

                ft.Row(
                    controls=[
                        DigitButton_else(text="X!", button_clicked=self.button_clicked),
                        DigitButton_else(text="sin", button_clicked=self.button_clicked),
                        DigitButton_else(text="cos", button_clicked=self.button_clicked),
                        DigitButton_else(text="tan", button_clicked=self.button_clicked),
                        DigitButton_else(text="e", button_clicked=self.button_clicked),
                        DigitButton_else(text="EE", button_clicked=self.button_clicked),
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),

                ## 5行目

                ft.Row(
                    controls=[
                        DigitButton_else(text="Rad", button_clicked=self.button_clicked),
                        DigitButton_else(text="sinh", button_clicked=self.button_clicked),
                        DigitButton_else(text="cosh", button_clicked=self.button_clicked),
                        DigitButton_else(text="tanh", button_clicked=self.button_clicked),
                        DigitButton_else(text="π", button_clicked=self.button_clicked),
                        DigitButton_else(text="Rand", button_clicked=self.button_clicked),
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    ##下記でそれぞれのtextごとにおされた時の処理を記述
    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/","(",")","mc","m+","m-","mr","2^nd","X^2”,”X^3","X^y","e^x","10^x", "1/X","2√x","3√x”,”y√x","In","log10","X!","sin","cos","tan","e","EE","Rad","sinh","cosh", "tanh","π","Rand",):    
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True


        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):

        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)
        
        elif operator == "X^y":
            return self.format_number(operand1 ** operand2)
        
        elif operator == "X^2":
            return self.format_number(operand1 ** 2)
        
        elif operator == "X^3":
            return self.format_number(operand1 ** 3)
        
        elif operator == "1/X":
            return self.format_number(1 / operand1)
        
        elif operator == "X!":
            if operand1 < 0 or not operand1.is_integer():  
                return "Error"
            return self.format_number(math.factorial(int(operand1)))
        
        elif operator == "sin":
            radians = math.radians(operand1)  
            return self.format_number(math.sin(radians))
        
        elif operator == "cos":
            radians = math.radians(operand1)
            return self.format_number(math.cos(radians))
        
        elif operator == "tan":
            radians = math.radians(operand1)
            return self.format_number(math.tan(radians))

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.app(target=main)
