import xlwt
import json
from progress_bar import progress

def build_xls(input_file, output_file):

	with open(input_file, 'r') as f:
		users_info = json.load(f)

	book = xlwt.Workbook()
	xlwt.add_palette_colour("background_color", 0x21)
	book.set_colour_RGB(0x21, 73, 208, 122)
	sheet = book.add_sheet("DOM.RIA")

	cols = ["Имя", "Тип", "Агентство", "Работает с DOM.RIA", "Всего предложений", "Область", "Город", "Телефон"]
	cols_width_ratio = 256
	sheet.set_panes_frozen(True)
	sheet.set_horz_split_pos(1)
	sheet.col(0).width = cols_width_ratio * 30
	sheet.col(1).width = cols_width_ratio * 10
	sheet.col(2).width = cols_width_ratio * 25
	sheet.col(3).width = cols_width_ratio * 19
	sheet.col(4).width = cols_width_ratio * 18
	sheet.col(5).width = cols_width_ratio * 20
	sheet.col(6).width = cols_width_ratio * 20
	sheet.col(7).width = cols_width_ratio * 13
	sheet.col(8).width = cols_width_ratio * 13
	sheet.col(9).width = cols_width_ratio * 13
	sheet.col(10).width = cols_width_ratio * 13

	total = len(users_info)

	row = sheet.row(0)
	for index, col in enumerate(cols):
		row.write(index, col, xlwt.easyxf('pattern: pattern solid, fore_colour background_color'))
	for user in range(total):
		progress(user, total-1, status = "Building .xls file")
		row = sheet.row(user+1)
		for index in range(8):
			if index == 0:
				i = 'name'
			elif index == 1:
				i = 'type'
			elif index == 2:
				i = 'agency'
			elif index == 3:
				i = 'term'
			elif index == 4:
				i = 'offers'
			elif index == 5:
				i = 'state'
			elif index == 6:
				i = 'city'
			elif index == 7:
				i = 'phones'
			
			if index<7:
				row.write(index, users_info[user][i])
			else:
				if type(users_info[user][i])==int:
					users_info[user][i]==[users_info[user][i]]
				for j in range(len(users_info[user][i])):
					row.write(index+j, users_info[user][i][j])
	progress(total, total, status = "Building .xls file")
	book.save(output_file)