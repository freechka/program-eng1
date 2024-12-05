# Функция расчета вязкости
def calculate_viscosity(CB, t):
    x = CB / (1900 - 18 * CB)
    try:
        ny = 10 ** (22.46 * x - 0.114 + (30 - t) / (91 + t) * (1.1 + 43.1 * x ** 1.25))
        return ny
    except (ZeroDivisionError, OverflowError):
        return None

# Функция для генерации значений концентрации и температуры
def generate_values(start, end, step):
    values = []
    current = start
    while current <= end:
        values.append(round(current, 2))
        current += step
    return values

# Функция для занесения данных
def viscosity_range(CB_start, CB_end, CB_step, t_start, t_end, t_step):
    CB_values = generate_values(CB_start, CB_end, CB_step)
    t_values = generate_values(t_start, t_end, t_step)

    viscosities = [[calculate_viscosity(CB, t) for t in t_values] for CB in CB_values]

    return viscosities if all(v is not None for row in viscosities for v in row) else None

# Функция выводов
def write_results_to_file(viscosities, method_name, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Расчет вязкости с помощью {method_name} (cP):\n")
        file.write(f"{'CB (%)':<10}")
        for t in generate_values(10, 50, 10):
            file.write(f"{t:<10}")
        file.write("\n")

        for i, CB in enumerate(generate_values(0, 50, 5)):
            file.write(f"{CB:<10.2f}")
            for ny in viscosities[i]:
                file.write(f"{ny:<10.2f}")
            file.write("\n")

def compare_with_experimental(viscosities, experimental_data, filename):
    with open(filename, 'a', encoding='utf-8') as file:  # Append mode
        file.write("\nСравнение с экспериментальными данными:\n")
        file.write(f"{'Temp (°C)':<12}{'CB (%)':<10}{'Эксп. вязкость (cP)':<25}{'Рассч. вязкость (cP)':<25}{'Ошибка (%)':<10}\n")

        for (t, CB), ny_exp in experimental_data.items():
            ny_calc = calculate_viscosity(CB, t)
            error = abs((ny_calc - ny_exp) / ny_exp) * 100 if ny_exp != 0 else None
            if error is not None:
                file.write(f"{t:<12}{CB:<10}{ny_exp:<25.2f}{ny_calc:<25.2f}{error:<10.2f}\n")
            else:
                file.write(f"{t:<12}{CB:<10}{ny_exp:<20.2f}{ny_calc:<20.2f}N/A\n")

experimental_data = {
    (40, 0): 0.65,
    (50, 50): 4.94,
    (30, 30): 2.50
}

# Функция для чтения параметров из файла с пояснениями
def read_parameters_from_file(file_path):
    parameters = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.split(':')
                parameters[key.strip()] = float(value.strip())
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None
    except ValueError as e:
        print(f"Ошибка при обработке файла: {e}. Проверьте формат данных.")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}.")
        return None

    # Проверка корректности диапазонов значений
    if any(param is None for param in parameters.values()):
        print("Ошибка: Не все параметры заданы в файле.")
        return None

    return (
        parameters.get('CB_start'),
        parameters.get('CB_end'),
        parameters.get('CB_step'),
        parameters.get('t_start'),
        parameters.get('t_end'),
        parameters.get('t_step')
    )

file_path = 'date.txt'
params = read_parameters_from_file(file_path)
try:
    CB_start, CB_end, CB_step, t_start, t_end, t_step = read_parameters_from_file(file_path)
except Exception as e:
    print(f"Ошибка при чтении параметров из файла: {e}")
else:
    # Проверка на корректность диапазонов
    if CB_start is None or CB_end is None or CB_step is None or t_start is None or t_end is None or t_step is None:
        print("Ошибка: Не все параметры заданы в файле.")
    else:
        # Вычисление вязкостей
        filename = "viscosity_results.txt"

        open("viscosity_results.txt", "w")

        viscosities = viscosity_range(CB_start, CB_end, CB_step, t_start, t_end, t_step)
        if viscosities is not None:
            write_results_to_file(viscosities, "Стандартного метода", filename)
            compare_with_experimental(viscosities, experimental_data, filename)
        else:
            print("Ошибка при расчете вязкости.")

        # Использование lambda-функций
        calculate_viscosity_lambda = lambda CB, t: (
            10 ** (22.46 * (CB / (1900 - 18 * CB)) - 0.114 +
                (30 - t) / (91 + t) * (1.1 + 43.1 * (CB / (1900 - 18 * CB)) ** 1.25))
                )

        viscosities_lambda = viscosity_range(CB_start, CB_end, CB_step, t_start, t_end, t_step)

        if viscosities_lambda is not None:
            write_results_to_file(viscosities_lambda, "lambda-функций", filename)
            compare_with_experimental(viscosities_lambda, experimental_data, filename)
        else:
            print("Ошибка при расчете вязкости lambda-функциями.")

        # Использование map-функций
        def calculate_viscosities_with_map(CB_values, t_values):
            viscosities = []
            for CB in CB_values:
                viscosities.append([calculate_viscosity(CB, t) for t in t_values])
            return viscosities

        CB_values = generate_values(CB_start, CB_end, CB_step)
        t_values = generate_values(t_start, t_end, t_step)


        viscosities_map = calculate_viscosities_with_map(CB_values, t_values)

        if viscosities_map is not None:
            write_results_to_file(viscosities_map, "map-функций", filename)
            compare_with_experimental(viscosities_map, experimental_data, filename)
        else:
            print("Ошибка при расчете вязкости методом map-функций.")