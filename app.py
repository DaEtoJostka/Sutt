import datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import streamlit as st

from forecasting import prediction_script

MOST_IMPORTANT_CONSTANT = 300


def predict_line_chart(dataframe: pd.DataFrame) -> None:
    datetime_column = [_x for i, _x in enumerate(dataframe['datetime'].to_list())]
    predict_column = [_y for i, _y in enumerate(dataframe['predict'].to_list())]

    if len(datetime_column) > MOST_IMPORTANT_CONSTANT:
        datetime_column = [datetime_column[index] for index in
                           range(0, len(datetime_column), len(datetime_column) // MOST_IMPORTANT_CONSTANT)]
        predict_column = [predict_column[index] for index in
                          range(0, len(predict_column), len(predict_column) // MOST_IMPORTANT_CONSTANT)]

    st.line_chart(
        {
            'datetime': datetime_column,
            'predict': predict_column,
        }, y='predict'
    )

st.set_page_config(page_title="Streamlit Wide Mode", layout="wide")
tractor_data_upload__tab, origin_tractor_data__tab = st.tabs(
    ["Загрузить данные трактора", "Валидация исходных данных тракторов от оператора", ])

with origin_tractor_data__tab:
    directory_path = Path().joinpath(*['data', 'исходные данные от оператора'])

    files_dict = {file_path.parent.name: file_path.name for file_path in directory_path.rglob("*") if
                  file_path.is_file()}

    st.header("Система умной телеметрии трактора")

    st.text('Для начала работы выберите трактор')

    SELECT_TRACTOR_IDENTIFIER_SUGGEST = 'Выберите идентификатор'
    SELECT_TRACTOR_DETAIL_SUGGEST = "Выберите деталь"

    selected_tractor_id = st.selectbox("Выберите идентификатор трактора",
                                       [SELECT_TRACTOR_IDENTIFIER_SUGGEST]
                                       + [f'{tractor_id}' for tractor_id in files_dict.keys()])
    if selected_tractor_id != SELECT_TRACTOR_IDENTIFIER_SUGGEST:
        if selected_tractor_id in files_dict:
            st.success(f"Выбранный трактор: {selected_tractor_id}")

            files = directory_path.joinpath(selected_tractor_id).rglob("*")
            dataframes = [pd.read_csv(file, delimiter=';') for file in files]
            dataframe = pd.concat(dataframes)
            dataframe = prediction_script.predict(dataframe)
            predict_line_chart(dataframe)

            predict_column = [_y for i, _y in enumerate(dataframe['predict'].to_list())]

            if sum(predict_column) / len(predict_column) > 1.5:
                st.error('Трактор сейчас определённо имеет проблемы')

                detail_id = st.selectbox("Выберите деталь для замены", [
                    SELECT_TRACTOR_DETAIL_SUGGEST,
                    "ДВС",
                    "КПП",
                    "Гидравлика",
                    "Питание двигателя",
                    "Электросистема",
                    "Стояночный тормоз",
                    "Охлаждение",
                    "Термостат",
                ])

                if detail_id != SELECT_TRACTOR_DETAIL_SUGGEST:
                    if detail_id:
                        st.success(f"{detail_id} заказана.\n"
                                   f"Ждите")
            else:
                st.success(f"Выбранный трактор сейчас в нормальном состоянии")

        else:
            st.error("Идентификатор не найдет. ")
with tractor_data_upload__tab:
    uploaded_file = st.file_uploader("Choose a file", )
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        dataframe = pd.read_csv(uploaded_file, delimiter=';')

        dataframe = prediction_script.predict(dataframe)

        predict_line_chart(dataframe)

        predict_column = [_y for i, _y in enumerate(dataframe['predict'].to_list())]

        if sum(predict_column) / len(predict_column) > 1.5:
            st.error('Трактор сейчас определённо имеет проблемы')

            detail_id = st.selectbox("Выберите деталь для замены", [
                SELECT_TRACTOR_DETAIL_SUGGEST,
                "ДВС",
                "КПП",
                "Гидравлика",
                "Питание двигателя",
                "Электросистема",
                "Стояночный тормоз",
                "Охлаждение",
                "Термостат",
            ])

            if detail_id != SELECT_TRACTOR_DETAIL_SUGGEST:
                if detail_id:
                    st.success(f"{detail_id} заказана.\n"
                               f"Ждите")
        else:
            st.success(f"Выбранный трактор сейчас в нормальном состоянии")
