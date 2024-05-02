import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from pathlib import Path


# PATH = 'data\исходные данные от оператора\С0873\log(336802058)[25-03-2024_16-31-03] 01.09-01-10.csv'
def predict(dataframe):
    dataframe = dataframe.replace(r'^\s*-', np.nan, regex=True)

    dataframe.reset_index(drop=True, inplace=True)

    dataframe.drop_duplicates(inplace=True)

    data_time = dataframe['Дата и время']

    dataframe.drop(columns=['Дата и время', 'iButton2', 'Нагрузка на двигатель, %', 'Крутящий момент (spn513), Нм',
                            'Положение рейки ТНВД (spn51), %', 'Расход топлива (spn183), л/ч',
                            'ДВС. Температура наддувочного воздуха, °С',
                            'Давление наддувочного воздуха двигателя (spn106), кПа', 'Текущая передача (spn523)',
                            'Температура масла гидравлики (spn5536), С', 'Педаль слива (spn598)'], inplace=True)

    dataframe.drop(['Нейтраль КПП (spn3843)', 'Стояночный тормоз (spn3842)',
                    'Аварийная температура охлаждающей жидкости (spn3841)', 'Засоренность воздушного фильтра (spn3840)',
                    'Засоренность фильтра КПП (spn3847)', 'Аварийное давление масла ДВС (spn3846)',
                    'Засоренность фильтра ДВС (spn3845)',
                    'Засоренность фильтра рулевого управления (spn3844)',
                    'Засоренность фильтра навесного оборудования (spn3851)',
                    'Недопустимый уровень масла в гидробаке (spn3850)',
                    'Аварийная температура масла в гидросистеме (spn3849)',
                    'Аварийное давление в I контуре тормозной системы (spn3848)',
                    'Аварийное давление в II контуре тормозной системы (spn3855)',
                    'Зарядка АКБ (spn3854)', 'Отопитель (spn3853)',
                    'Выход блока управления двигателем (spn3852)',
                    'Включение тормозков (spn3859)', 'Засоренность фильтра слива (spn3858)',
                    'Аварийное давление масла КПП (spn3857)',
                    'Аварийная температура масла ДВС(spn3856)',
                    'Неисправность тормозной системы (spn3863)', 'Термостарт (spn3862)',
                    'Разрешение запуска двигателя (spn3861)', 'Низкий уровень ОЖ (spn3860)',
                    'Аварийная температура масла ГТР (spn3867)',
                    'Необходимость сервисного обслуживания (spn3866)',
                    'Подогрев топливного фильтра (spn3865)', 'Вода в топливе (spn3864)',
                    'Холодный старт (spn3871)'], axis=1, inplace=True)

    dataframe = dataframe.astype(str)

    dataframe["Сост.пед.сцепл."] = dataframe["Сост.пед.сцепл."].astype(bool)

    dataframe['Обор.двиг.,об/мин'] = dataframe['Обор.двиг.,об/мин'].str.replace(',', '.').astype(float)

    dataframe['Значение счетчика моточасов, час:мин'] = dataframe['Значение счетчика моточасов, час:мин'].str.replace(
        ':', '').astype(float)

    dataframe['Сост.пед.сцепл.'] = dataframe['Сост.пед.сцепл.'].replace(',', '.').astype(float)
    dataframe['Сост.пед.сцепл.'] = dataframe['Сост.пед.сцепл.'].astype(str)

    dataframe['Полож.пед.акселер.,%'] = dataframe['Полож.пед.акселер.,%'].str.replace(',', '.').astype(float)

    dataframe['Темп.масла двиг.,°С'] = dataframe['Темп.масла двиг.,°С'].str.replace(',', '.').astype(float)

    dataframe['КПП. Температура масла'] = dataframe['КПП. Температура масла'].astype(float)

    model = CatBoostClassifier()

    model.load_model(Path().joinpath(*['forecasting', 'model.cbm']))

    dataframe['predict'] = model.predict(dataframe)

    dataframe['datetime'] = data_time

    return dataframe
