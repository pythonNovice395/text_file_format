"""
It is highly recomended to use file_setup() to setup the amount on lines needed
file_path will need the path to the textfile before using any functions
Two FileObjects are not allowed to use the same line in the same module
File symbols:
**X** - tells file_setup that this file has already been setup. Found on line 1. If removed, the file will be wiped clean.
||| - tells create_space that it is okay to wipe that area clean because it is unused. Found on any line other than line 1.
||X|| - empty space, the read function will not read this line and just return 'None'(NoneType)
"""
from . import ERRORS

# file_path = "F:/Python Projects/Testing Grounds/temp.txt"
file_path = ""
all_lines = []
max_lines = None

FAILED = 'failed'
P3SS = 'pass'



class FileObject:

            def __init__(self, line):
                self._line = line
                self.file_link = file_path
                return

            def write(self, data: str|int):
                if self._line == 0:
                    raise ERRORS.LineExistsError('Line 1 is reserved, check doc of this module for more info.')
                data = str(data)
                rfile = open(self.file_link, 'r')
                lines = rfile.readlines()
                with open(self.file_link, 'w') as wfile:
                    try:
                        lines.pop(self._line)
                    except IndexError:
                        pass # passes because if there is no line, lines.insert will just make another one anyway
                    lines.insert(self._line, f"{data}\n")
                    wfile.writelines(lines)
                    rfile.close()

            def append(self, data: str|int):
                if self._line == 0:
                    raise ERRORS.LineExistsError('Line 1 is reserved, check doc of this module for more info.')
                with open(self.file_link, 'r') as rfile:
                    lines = rfile.readlines()
                line = lines[self._line]
                if '\n' in line:
                    line = line.replace('\n', '')
                line = f"{line}{data}\n"
                lines.pop(self._line)
                lines.insert(self._line, line)
                with open(self.file_link, 'w') as wfile:
                    wfile.writelines(lines)
                return

            def read(self):
                if self._line == 0:
                    raise ValueError(f'''
Line 1 is reserved, doc below.

{__doc__}
                ''')
                file = open(self.file_link, 'r')
                lines = file.readlines()
                file.close()
                line = lines[self._line]
                if "||X||" not in line:
                    line = line.replace('\n', '')
                    try:
                        line = int(line)
                    except ValueError:
                        try:
                            line = float(line)
                        except ValueError:
                            line = str(line)
                    return line
                elif "||X||" in line:
                    return None


def expand_file(amount_of_lines):
    rfile = open(file_path, 'r')
    lines = rfile.readlines()
    rfile.close()
    for x in range(amount_of_lines):
        lines.insert(-1, "|||\n")
    wfile = open(file_path, 'w')
    wfile.writelines(lines)
    wfile.close()


def create_space(line: int):
    line -= 1
    state = "pass"
    for _line in all_lines:
        if _line == line:
            state = FAILED
            print(f'Line {line} already is used')
    if max_lines is not None:
        if line > max_lines:
            state = FAILED
            print('Line exceedes max_lines')
    if line == 0:
        state = FAILED
        print("line 1 is reserved")
    if state == P3SS:
        all_lines.append(line)
        rfile = open(file_path, 'r')
        lines = rfile.readlines()
        rfile.close()
        try:
            lines[line]
        except IndexError:
            expand_file(line)
            rfile = open(file_path, 'r')
            lines = rfile.readlines()
            rfile.close()
        if '|||' in lines[line]:
            with open(file_path, 'w') as wfile:
                try:
                    lines.pop(line)
                except IndexError:
                    pass # passes because if there is no line, lines.insert will just make another one anyway
                lines.insert(line, ' \n')
                wfile.writelines(lines)
        

        return FileObject(line)
    elif state == 'failed':
        print("Error")
        exit(1)


def file_setup(max_lines0):
    global max_lines
    max_lines = max_lines0
    lines = []
    with open(file_path, 'r') as test_file:
        test_file.seek(0, 0)
        data = test_file.readline(5)
    if '**X**' not in data:
        with open(file_path, 'w') as file:
            lines.append('**X**\n')
            for x in range(max_lines - 1):
                lines.append('|||\n')
            lines.append('|||')
            file.writelines(lines)




taken_lines = []


def detect_state(table_class):
    match table_class.state:
        case 'active':
            pass
        case 'deactivated':
            raise ERRORS.TableError("ERROR, cannot opporate on a deleted table")

class Table:
        def __init__(self, ze_dict: dict, max_lines: int, columns: list[tuple[str, int]]):
            self.stor_vars = ze_dict.copy()
            self.max_lines = max_lines
            self.columns = columns
            self.state = 'active'
            
        def insert_once(self, data: str, column, row: int):
            """
            NOTE: will delete any pre-existing data in that row
            """
            detect_state(self)
            row -= 1
            reg = 0
            _vars = []
            for column1 in self.columns:
                    name = column1[0]
                    if name == column:
                        for x in range(column1[1]):
                            vname = f"{name}{reg}"
                            _vars.append(self.stor_vars[vname])
                            reg += 1
            vline: FileObject = _vars[row]
            vline.write(data)
            return
        
        def insert_many(self, data: list, column: str, rows: tuple):
            detect_state(self)
            reg = 0
            for row in rows:
                if len(data) > 1:
                    x = data[reg]
                elif len(data) == 1:
                    x = data[0]
                try:
                    self.insert_once(x, column, row)
                    reg += 1
                except IndexError:
                    raise ERRORS.SizeError("The amount of rows given excedes the max_lines of the column.")
            return
        
        def add_column(self, column_name, max_lines):
            self.columns.append((column_name, max_lines))
            reg = 0
            grouped_size = 0
            for column in self.columns:
                grouped_size += column[1]
            for x in range(max_lines):
                self.stor_vars[f"{column_name}{reg}"] = create_space(grouped_size + reg)
                reg += 1
            return

        def delete_row(self, column, row):
            detect_state(self)
            self.insert_once("||X||", column, row)

        def delete_column(self, column):
            detect_state(self)
            reg = 0
            _vars = []
            for column1 in self.columns:
                    name = column1[0]
                    if name == column:
                        for x in range(column1[1]):
                            vname = f"{name}{reg}"
                            self.stor_vars[vname].write("||X||")
                            reg += 1
                        self.columns.remove(column1)
            return

        def delete_table(self):
            detect_state(self)
            self.state = "deactivated"
            for v in self.stor_vars:
                vline = self.stor_vars[v]
                vline.write("||X||")
            self.__delattr__("columns")
            self.__delattr__("max_lines")
            self.__delattr__("stor_vars")

        def grab_row(self, column, row):
            detect_state(self)
            row -= 1
            reg = 0
            _vars = []
            for column1 in self.columns:
                    name = column1[0]
                    if name == column:
                        for x in range(column1[1]):
                            vname = f"{name}{reg}"
                            _vars.append(self.stor_vars[vname])
                            reg += 1
            vline: FileObject = _vars[row]
            return vline.read()
        
        def grab_column(self, column):
            detect_state(self)
            reg = 0
            _vars = []
            out = []
            for column1 in self.columns:
                    name = column1[0]
                    if name == column:
                        for x in range(column1[1]):
                            vname = f"{name}{reg}"
                            _vars.append(self.stor_vars[vname])
                            reg += 1
            for var in _vars:
                out.append(var.read())
            return out
        
        def grab_table(self):
            detect_state(self)
            _vars = []
            out = []
            out2 = []
            for column1 in self.columns:
                reg = 0
                name = column1[0]
                for x in range(column1[1]):
                    vname = f"{name}{reg}"
                    _vars.append(self.stor_vars[vname])
                    reg += 1
            reg = 0
            for column2 in self.columns:
                for x in range(column2[1]):
                    out2.append(_vars[reg].read())
                    reg += 1
                out.append(out2.copy())
                out2.clear()
                pass
            return out



def construct_table(start_on_line: int, max_lines: int, columns: list[tuple[str, int]]):
    """
columns example: ((name, max_lines), (name, max_lines))
NOTES:
the max_lines used by a column cannot excede the max_lines of the table.
when changing the max_lines of a table, make sure that it doesn't collide with another table.
the txt file MUST have enough space for the table.
Columns will be created in the same order of the tuple provided in the columns paramater.
Two columns cannot have the same name
    """
    if start_on_line in taken_lines:
        raise ERRORS.TableCollisionError("This table is intersecting another")
    if max_lines in taken_lines:
        raise ERRORS.TableCollisionError("This table is intersecting another")
    reg = start_on_line
    for x in range(max_lines):
        taken_lines.append(reg)
        reg += 1
    ze_dict = {}
    file_setup(max_lines)
    column_names = []
    grouped_size = 0
    for column in columns:
        if column[0] in column_names:
            raise ERRORS.ColumnExistsError(f"Column name '{column[0]}' already exists")
        if column[0] not in column_names:
            column_names.append(column[0])
            grouped_size += column[1]
            if grouped_size > max_lines:
                raise ERRORS.SizeError("Error, the size of the columns combined is larger than the table")
            reg = 0
            for x in range(column[1]):
                ze_dict[f"{column[0]}{reg}"] = create_space(start_on_line + grouped_size + reg - column[1])
                reg += 1
    return Table(ze_dict, max_lines, columns)


pass
