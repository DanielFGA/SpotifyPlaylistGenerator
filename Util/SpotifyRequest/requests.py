header = "Bearer {}"

def generate_parameter(parameter_name, parameter_values, seperator):
    if (len(parameter_values) == 0):
        return ""

    parameter = parameter_name + "="

    for value in parameter_values:
        parameter += value + seperator

    parameter = parameter[:-len(seperator)]

    return parameter

def concat_parameter(parameters, seperator):
    concats = ""

    for parameter in parameters:
        if (len(parameter) > 0):
            concats += parameter + seperator

    concats = concats[:-1]

    return concats
