import random
import string
import lorem
import re
import copy
import os
import numpy as np
import cfg


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
        if self.language == 'py':
            com_template = '#'

        if self.language == 'js':
            comm_template = '//'

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
        keyword = ''
        if self.language == 'js':
            keyword = 'var'
        if self.language == 'php':
            keyword = '$'
        name = self.__get_random_string__()
        value = random.randint(-100, 100)

        return keyword, name, value


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
        # gen_func = []
        # for _ in range(count_func):
        #     func = Function(context)

        pass


        
    
    def __get_func_body_(self, params):
        pass


    def __get_random_func__(self, context):
        keyword = ''
        if self.language == 'py':
            keyword = 'def'
        if self.language == 'php' or self.language == 'js':
            keyword = 'function'

        context = copy.deepcopy(context)
        par_number = random.randrange(0, 5)
        params = []

        for _ in range(par_number):
            par = Variable(self.language)
            context['vars'].append(par)
            params.append(par)

        name = self.__get_random_string__()
        body = ''

        return keyword, name, params, body


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


    # entry point
    def transform_code(self, source):
        print(f'Obfuscating {source:.<98}')

        self.data = self.__read_source_code__(source)

        available_bytes = len(self.data) * cfg.SCALE_FACTOR

        self.data = self.__remove_comments__(self.data)
        self.data = self.__add_comment__(self.data)
        print(self.data)

        available_bytes -= len(self.data)

        context = {
            'vars' : [],
            'funcs' : []
        }        

        print(f"Available symbols: {available_bytes}")
        count_vars, len_vars, count_funcs, len_funcs = self.__calc_counts__(available_bytes)

        # count_vars = 5

        # for _ in range(count_vars):
        #     variables = self.__get_context_vars__(count_vars, context)
        #     variables = '\n'.join(variables)

        # Function('js', context).print_func()

            

            

        

class Variable:
    def __init__(self, language):
        self.keyword, self.name, self.value = Transformer(language).__get_random_var__()

class Function:
    def __init__(self, language, context):
        self.keyword, self.name, self.params, self.body = Transformer(language).__get_random_func__(context)

    def print_func(self):
        print(f'{self.keyword} {self.name}({self.params})')

# class Class:
#     pass