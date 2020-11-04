import random
import string
import re
import copy
import os
import numpy as np
import cfg
import python_ast


class Transformer:
    def __init__(self, language):
        self.language = language    # programming language
        self.data = ''              # raw code  
        self.function_template = ''
        self.variable_template = ''
        self.class_template = ''


    # read the source file and return raw code
    def __read_source_code__(self, source):
        with open(source) as fin:
            return fin.read()


    def __remove_comments__(self, data):
        data = re.sub(re.compile(r"[\n\s]*#.*"), "" , data)
        return data

    
    def __add_comment__(self, data):
        com_template = ''

        print(f'language {self.language}')

        if self.language == 'py' or self.language == 'rb' or self.language == 'pl' or self.language == 'R':
            com_template = '#'

        if self.language == 'js' or self.language == 'php':
            com_template = '//'

        new_data = ''
        for line in data.splitlines():
            if re.match(r'.*\s*$', line) and random.choice([True, False]):
                random_com = self.__get_random_string__(3)
                new_data += line + f' {com_template} {random_com}'
            else:
                new_data += line
            
            new_data += '\n'

        return new_data


    def __get_random_string__(self, size=0):
        if size == 0:
            start = 2
            stop = 10
            size = random.randrange(start, stop)

        chars = string.ascii_letters + string.digits + '_'
        first_symbol = random.choice(string.ascii_letters)

        other_symbols = ''.join(random.choice(chars) for i in range(size))
        return first_symbol + other_symbols


    def __get_random_var__(self):
        keyword = '' # empty for Python, Ruby and R
        if self.language == 'js':
            keyword = 'var'
        if self.language == 'php' or self.language == 'pl':
            keyword = '$'
        name = self.__get_random_string__()
        value = random.randint(-100, 100)

        return keyword, name, value

    def __gen_all_types_vars__(self, context):
        variables = []
        for _ in range(random.randint(4, 10)):
            var = Variable(self.language)
            context['vars'].append(var)
            random_variable = f'{var.keyword} {var.name} = {var.value}'

            code = f'{random_variable}'
            variables.append(code)
        return variables


    def __get_context_vars__(self, count_vars, context):
        variables = []
        for _ in range(count_vars):
            var = Variable(self.language)
            context['vars'].append(vars)
            rand_var = f'{var.keyword} {var.name} = {var.value}'

            code = f'{rand_var}\n'
            variables.append(code)
        
        return variables

    
    def __get_context_func__(self, count_func, context):
        gen_funcs = []
        for _ in range(count_func):
            func = Function(self.language, context)
            context['funcs'].append(func)
            code = f'{func.name} ({func.params_to_str()}):\n{func.body}'
            gen_funcs.append(code)


        return gen_funcs

        
    def __get_func_body_(self, params):
        pass


    def __get_random_func__(self, context):
        keyword_start = ''
        keyword_end = '' # only for Ruby
        if self.language == 'py':
            keyword_start = 'def'
        if self.language == 'rb':
            keyword_start = 'def'
            keyword_end = 'end'
        if self.language == 'php' or self.language == 'js' or self.language == 'pl':
            keyword_start = 'function'

        context = copy.deepcopy(context)
        par_number = random.randrange(0, 5)
        params = []

        for _ in range(par_number):
            par = Variable(self.language)
            context['vars'].append(par)
            params.append(par)

        name = self.__get_random_string__()
        body = '\tpass'

        return keyword_start, name, params, body


    # def __get_random__body__(self, context):
    #     code = ''
    #     # add utils
    #     calls = random.choices(context['funcs'], k=utils.rand_count(1, 5, len(context['funcs'])))

    #     for call in calls:
    #         code += '\t'
    #         receive = None
            

    def __calc_counts__(self, N):
        number = random.uniform(0, 1)
        a = np.random.normal(number, 0.05)
        a = max(0.05, a)
        a = min(0.2, a)

        b = np.random.normal(1-number, 0.05)
        b = max(0.2, b)
        b = min(0.9, b)

        len_vars = N * a
        len_funcs = (N - len_vars) * b

        count_vars = int(len_vars / cfg.SYM_ON_VAR)
        count_funcs = int(len_funcs / cfg.SYM_ON_FUNC)

        count_vars = max(cfg.MIN_CONTEX_VARS, count_vars)
        count_funcs = max(cfg.MIN_CONTEX_FUNCS, count_funcs)

        return count_vars, int(len_vars), count_funcs, int(len_funcs)

    def __accumulate_float(self, arr):
        acc = 0
        for i in range(len(arr)):
            arr[i] += acc
            i_part = int(arr[i])
            acc = arr[i] - i_part
            arr[i] = i_part
        if acc > 0.001:
            arr[0] += 1
        return arr

    def __get_distribution(self, N, count):
        if N == 0:
            return []
        v = count / N
        dist_arr = [v for _ in range(N)]

        return self.__accumulate_float(dist_arr)


    def __rename__(self):
        a = Ast(self.data)
        for i in range(len(a.get_top_level_pos())):
            new_name = __get_random_string__()
            pos = a.get_top_level_pos()[i]
            a.rename(pos[0], new_name)



    # entry point
    def transform_code(self, source):
        print(f'Obfuscating {source:.<98}')

        self.data = self.__read_source_code__(source)

        available_bytes = len(self.data) * cfg.SCALE_FACTOR

        print(self.data)

        print(f'Renaming...')
        self.__rename__()

        self.__remove_comments__(self.data)
        self.__add_comment__(self.data)
        print(self.data)

        available_bytes -= len(self.data)

        context = {
            'vars' : [],
            'funcs' : []
        }        

        print(f"Available symbols: {available_bytes}")
        count_vars, len_vars, count_funcs, len_funcs = self.__calc_counts__(available_bytes)

        print(f"{count_vars} {count_funcs}")

        print(f"Will be generate: vars {count_vars}[{len_vars} sym], funcs {count_funcs}[{len_funcs} sym]")

        a = python_ast.Ast(self.data)
        poss = a.get_top_level_pos()

        print(f"poss {poss}")

        dist_vars = self.__get_distribution(10, count_vars)
        dist_funcs = self.__get_distribution(10, count_funcs)

        variables = self.__gen_all_types_vars__(context)
        new_code = '\n'.join(variables) + '\n'
        self.data = new_code + self.data

        offset_accum = len(new_code)
        for p, count_vars, count_funcs in zip(poss, dist_vars, dist_funcs):
            print("fff")
            variables = self.__get_context_vars__(count_vars, context)
            variables = '\n'.join(variables)

            print(f'=====VARIABLES: {variables}======')

            functions = self.__get_context_func__(count_funcs, context)
            functions = '\n'.join(functions)

            print(f'=====FUNCTIONS {functions}======')

            new_code = '\n' + variables + '\n' + functions + '\n'

            p = p[1] + offset_accum
            self.data = self.data[:p] + new_code + self.data[p:]
            offset_accum += len(new_code)

        print(self.data)
        

class Variable:
    def __init__(self, language):
        self.keyword, self.name, self.value = Transformer(language).__get_random_var__()

class Function:
    def __init__(self, language, context):
        self.keyword, self.name, self.params, self.body = Transformer(language).__get_random_func__(context)


    def params_to_str(self):
        params = ''
        for var in self.params:
            params += f'{var.keyword} {var.name}'
            if var != self.params[-1]:
                params += ', '

        return params                


    def print_func(self):
        print(f'{self.keyword} {self.name}({self.params})')

# class Class:
#     pass