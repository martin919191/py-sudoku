class PySudoku:
    def print_sudoku(self, sudoku):
        rows_string = []
        for row in range(9):
            row_string = "│"
            for column in range(9):
                if column == 3 or column == 6:
                    row_string += "│"
                if sudoku[row][column] is None:
                    row_string += ' * '
                else:
                    row_string += ' {} '.format(sudoku[row][column])
            row_string += '│'
            rows_string.append(row_string)

        sudoku_string = """
        ┌─────────┬─────────┬─────────┐
        {}
        {}
        {}
        ├─────────┼─────────┼─────────┤
        {}
        {}
        {}
        ├─────────┼─────────┼─────────┤
        {}
        {}
        {}
        └─────────┴─────────┴─────────┘
        """.format(rows_string[0], rows_string[1], rows_string[2],
                   rows_string[3], rows_string[4], rows_string[5],
                   rows_string[6], rows_string[7], rows_string[8])
        print(sudoku_string)

    def get_columns(self, sudoku):
        columns = [[], [], [], [], [], [], [], [], []]
        for row in sudoku:
            columns[0] = columns[0] + [row[0]]
            columns[1] = columns[1] + [row[1]]
            columns[2] = columns[2] + [row[2]]
            columns[3] = columns[3] + [row[3]]
            columns[4] = columns[4] + [row[4]]
            columns[5] = columns[5] + [row[5]]
            columns[6] = columns[6] + [row[6]]
            columns[7] = columns[7] + [row[7]]
            columns[8] = columns[8] + [row[8]]
        return columns

    def get_sub_matices(self, sudoku):
        sub_matrices = []
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                sub_matrices.append([sudoku[i][j],
                                     sudoku[i][j+1],
                                     sudoku[i][j+2],
                                     sudoku[i+1][j],
                                     sudoku[i+1][j+1],
                                     sudoku[i+1][j+2],
                                     sudoku[i+2][j],
                                     sudoku[i+2][j+1],
                                     sudoku[i+2][j+2]])
        return sub_matrices

    def get_empty_sudoku(self, ):
        empty_sudoku = [[None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None, None]]
        return empty_sudoku

    def validate_repeated_values(self, array):
        repeated = False
        elements = {}
        for element in array:
            if element is not None:
                if element in elements.keys():
                    repeated = True
                    break
                else:
                    elements[element] = None
        return repeated

    def is_valid_sudoku(self, sudoku):
        for row in sudoku:
            repeated_values = (self.validate_repeated_values(row))
            if repeated_values:
                return False
        columns = self.get_columns(sudoku)
        for column in columns:
            repeated_values = (self.validate_repeated_values(column))
            if repeated_values:
                return False
        return True
        sub_matrices = get_sub_matrices(sudoku)
        for sub_matrix in sub_matrices:
            repeated_values = (validate_repeated_values(sub_matrix))
            if repeated_values:
                return False
        return True

    def get_empty_cells(self, sudoku):
        sub_matrices = self.get_sub_matices(sudoku)
        columns = self.get_columns(sudoku)
        empty_cells = {'single_value': [],
                       'multiple_values': [],
                       'no_possible_values': False}

        for row_index in range(len(sudoku)):
            row = sudoku[row_index]
            for col_index in range(len(row)):
                if sudoku[row_index][col_index] == None:
                    possible_values = self.get_possible_values(row_index,
                                                          col_index,
                                                          sudoku,
                                                          columns,
                                                          sub_matrices)
                    if 'single_value' in possible_values.keys():
                        empty_cells['single_value'].append((row_index,
                                                            col_index,
                                                            possible_values['single_value']
                                                            ))
                    elif 'no_possible_values' in possible_values.keys():
                        empty_cells['no_possible_values'] = True
                    else:
                        empty_cells['multiple_values'].append((row_index,
                                                               col_index,
                                                               possible_values['multiple_values']
                                                               ))
        empty_cells['multiple_values'].sort(key=lambda x: len(x[2]))
        return empty_cells

    def get_possible_values(self, row_index, col_index, rows, columns, sub_matrices):
        random = __import__('random')
        possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sub_matrix_index = int(row_index/3) * 3 + int(col_index/3)
        for i in range(9):
            row_value = rows[row_index][i]
            col_value = columns[col_index][i]
            sub_matrix_value = sub_matrices[sub_matrix_index][i]
            if row_value is not None and row_value in possible_values:
                possible_values.remove(row_value)
            if col_value is not None and col_value in possible_values:
                possible_values.remove(col_value)
            if sub_matrix_value is not None and sub_matrix_value in possible_values:
                possible_values.remove(sub_matrix_value)
        if len(possible_values) == 0:
            return {'no_possible_values': True}
        elif len(possible_values) == 1:
            return {'single_value': possible_values}
        else:
            random.shuffle(possible_values)
        return {'multiple_values': possible_values}

    def fill_single_value_cells(self, sudoku, empty_cells):
        for empty_cell in empty_cells:
            row = empty_cell[0]
            col = empty_cell[1]
            value = empty_cell[2][0]
            sudoku[row][col] = value

    def solve_sudoku(self, unsolved_sudoku, recursion_level=0):
        copy = __import__('copy')
        sudoku = copy.deepcopy(unsolved_sudoku)
        if not self.is_valid_sudoku(sudoku):
            return {'status': 'fail'}
        else:
            empty_cells = self.get_empty_cells(sudoku)
            if empty_cells['no_possible_values']:
                return {'status': 'fail'}
            while len(empty_cells['single_value']) > 0:
                self.fill_single_value_cells(
                    sudoku, empty_cells['single_value'])
                empty_cells = self.get_empty_cells(sudoku)
        ### BELOW THIS LINE, THERE IS TERROR ###
        still_unsolved = False
        if len(empty_cells['multiple_values']) > 0:
            # for empty_cell in empty_cells['multiple_values']:
            empty_cell_to_fill = empty_cells['multiple_values'][0]
            row_to_fill = empty_cell_to_fill[0]
            col_to_fill = empty_cell_to_fill[1]
            values_to_try = empty_cell_to_fill[2]
            for value in values_to_try:
                sudoku_copy = copy.deepcopy(sudoku)
                sudoku_copy[row_to_fill][col_to_fill] = value
                result = self.solve_sudoku(
                    sudoku_copy, recursion_level=recursion_level+1)
                if result['status'] != 'fail':
                    return result
        else:
            ### ABOVE THIS LINE, THERE IS TERROR ###
            if not self.is_valid_sudoku(sudoku):
                return {'status': 'fail'}
            else:
                return{'status': 'OK',
                       'sudoku': sudoku,
                       'recursion_level': recursion_level}
        return {'status': 'fail'}
