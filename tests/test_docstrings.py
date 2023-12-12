import pytest
from pytest_examples import find_examples, CodeExample, EvalExample


# --------------------------------------------------------------------------- #
# API                                                                         #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./settus"), ids=str)
def test_docstrings_spark_functions(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(
            example,
            module_globals={
            },
        )
    else:
        eval_example.lint(example)
        eval_example.run_print_check(
            example,
            module_globals={
                # "spark": spark,
                # "display": lambda x: x,
            },
        )


# --------------------------------------------------------------------------- #
# Markdowns                                                                   #
# --------------------------------------------------------------------------- #


# @pytest.mark.parametrize("example", find_examples("./docs/"), ids=str)
# def test_docstrings_spark_functions(example: CodeExample, eval_example: EvalExample):
#     """
#     Examples in documentation are not all designed to be run in isolation. We only format them using black. To be
#     investigated if there is a better approach.
#     """
#
#     if eval_example.update_examples:
#         # eval_example.format_black(example)
#         eval_example.format(example)
#         eval_example.run_print_update(example)
#
#     else:
#         # eval_example.lint_black(example)
#         eval_example.lint(example)
#         eval_example.run_print_check(example)