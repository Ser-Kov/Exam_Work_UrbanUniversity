import os
import csv
import pandas


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='./Практическое задание _Анализатор прайс-листов._'):
        # Получаем все файлы из исходной директории
        files = os.listdir(path='./Практическое задание _Анализатор прайс-листов._')

        # Добавляем в self.data csv-файлы с названием "price"
        for file in files:
            if 'price' in file:
                self.data.append(file)

        # Прописывем названия для столбцов будущей таблицы и готовим список values_columns со значениями столбцов
        headers = ['Наименование', 'Цена', 'Вес', 'Файл', 'Цена за кг.']
        values_columns = []

        # Проходимся по каждому файлу из self.data
        for price_file in self.data:
            # Используя библиотеку csv читаем файл
            with (open(f'{file_path}/{price_file}', 'r', encoding='utf-8') as file):
                csvreader = csv.reader(file)

                # Возможные названия для столбцов
                example_product = ['товар', 'название', 'наименование', 'продукт']
                example_price = ['розница', 'цена']
                example_weight = ['вес', 'масса', 'фасовка']

                # Готовим переменные, которые будут содержать названия столбцов конкретного файла из self.data
                product = ''
                price = ''
                weight = ''

                # Читаем только первую строчку файла, содержащую названия столбцов
                first_line_in_file = next(csvreader)

                # В цикле перебираем возможное название столбца product с текущим
                for i in example_product:
                    for element_of_first_line in first_line_in_file:
                        # Если возможное название совпадает с текущим, присваиваем значение переменной product
                        if element_of_first_line == i:
                            product = i
                            break

                for i in example_price:
                    for element_of_first_line in first_line_in_file:
                        if element_of_first_line == i:
                            price = i
                            break

                for i in example_weight:
                    for element_of_first_line in first_line_in_file:
                        if element_of_first_line == i:
                            weight = i
                            break

                # Теперь можно узнать индекс каждого столбца
                index_for_product = first_line_in_file.index(product)
                index_for_price = first_line_in_file.index(price)
                index_for_weight = first_line_in_file.index(weight)

                # Добавляем в список значений данные каждой строки файла в соответствии с индексом столбца
                for row in csvreader:
                    values_columns.append([row[index_for_product], int(row[index_for_price]),
                                           row[index_for_weight], price_file, float(row[index_for_price])])

        # Создаем таблицу pandas с полученными значениями и заголовками для столбцов, указанными ранее
        table = pandas.DataFrame(values_columns, columns=headers)

        # Нумерацию осуществляем по индексу, меняя имя индекса на "Номер" и начиная отсчет с 1 (default_index=0)
        table.index.name = 'Номер'
        table.index += 1
        table.reset_index(level=0, inplace=True)

        # Сохраняем таблицу в self.result
        self.result = table

        return self.result

    def export_to_html(self, fname='output.html'):
        file_path = './Практическое задание _Анализатор прайс-листов._'
        table = self.result

        # Сортируем таблицу по цене (по возрастанию)
        try:
            sorted_table = table.sort_values(by='Цена')


            # Экспортируем таблицу в html (без индекса)
            html_table = sorted_table.to_html(index=False)

            # Перезаписываем html-файл "output.html", вставляя html_table при помощи {} и format
            with open(f'{file_path}/{fname}', 'w', encoding='utf-8') as f:
                result = '''
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>Позиции продуктов</title>
                            </head>
                            <body>
                                {html_table}
                            '''.format(html_table=html_table)
                f.write(result)

            return f'HTML файл "{fname}" обновлен'

        except AttributeError:
            return ('Чтобы перевести данные таблицы в html-формат, '
                    'сначала загрузите эти данные, выполнив метод load_prices()')

    def find_text(self):
        table = self.result

        # Еще раз сортируем исходную таблицу self.result
        try:
            sorted_table = table.sort_values(by='Цена')

            # Формируем цикл обмена с пользователем
            text = str(input('Введите фрагмент из названия товара (для выхода введите "exit"): '))
            while text != 'exit':
                # Готовим список значений для новой таблицы
                new_values = []

                # В цикле проходимся по итерируемым строчкам таблицы, производя поиск строк по введенному запросу
                for index, row in sorted_table.iterrows():
                    if text.lower() in row['Наименование'].lower():
                        # Когда слово по запросу найдено, добавляем данную строку в список new_values
                        new_values.append(row)

                # Создаем новую таблицу и отображаем ее пользователю
                new_table = pandas.DataFrame(new_values,
                                             columns=['Номер', 'Наименование', 'Цена', 'Вес', 'Файл', 'Цена за кг.'])
                print(new_table)
                text = str(input('Продолжите поиск по фрагменту (для выхода введите "exit"): '))

            print('Программа успешно завершена!')

        except AttributeError:
            print('Чтобы найти данные таблицы, '
                    'сначала загрузите эти данные, выполнив метод load_prices()')


pm = PriceMachine()
print(pm.load_prices())
print(pm.export_to_html())
pm.find_text()
