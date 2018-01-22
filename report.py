from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference,
)
from datetime import datetime


def report_to_spreadsheet(seeds_history: list):
    wb = Workbook()
    ws = wb.active
    cs = wb.create_chartsheet()

    chart = LineChart()

    headers = []
    header_seed_keys = []

    for key, value in seeds_history[0].items():
        if not value:
            continue
        headers.append(key.name)
        header_seed_keys.append(key)

    ws.append(headers)

    for row_index, seed in enumerate(seeds_history):
        row = []

        for key in header_seed_keys:
            try:
                row.append(seed[key])
            except KeyError:
                pass

        ws.append(row)

    data = Reference(ws, min_col=1, max_col=len(headers), min_row=1, max_row=len(seeds_history))
    chart.add_data(data, titles_from_data=True)

    cs.add_chart(chart)

    dnow = datetime.now()
    report_name = str(dnow.day) + '_' + str(dnow.hour) + '_' + str(dnow.minute) + '_' + str(dnow.second)

    wb.save('reports/' + report_name + '.xlsx')
