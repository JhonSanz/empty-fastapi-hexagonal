DOMAIN_EXCEPTIONS_TEMPLATE = """


class {{ model_pascal_case }}NotFoundException(Exception):
    pass
"""
