# corpus  (c)2024  Henrique Moreira

""" Basic deterministic first usage of `markovify.Text`
"""

# pylint: disable=missing-function-docstring

import os.path
import random
import markovify

DEBUG = 0
IO_ENCODING = "ISO-8859-1"
IN_ENCODING = "utf-8"

RAND_FIXED = False	# Put 'True' if you prefer to have predictable random output
RAND_APPLY = 42		# Put any fixed seed if you prefer


def main():
    myname = __file__
    opts = {
        "rand": RAND_APPLY if RAND_FIXED else -1,
    }
    runner(
        os.path.join(os.path.dirname(myname), "corpus.txt"),
        [],
        opts,
        DEBUG,
    )

def runner(fname, param, opts, debug=0):
    if param:
        return None
    res = script(fname, opts, debug)
    return res

def script(fname:str, opts, debug=0):
    print(f"markovify.Text(read={fname}, state_size=1)")
    with open(fname, "r", encoding=IN_ENCODING) as fdin:
        text = fdin.read()
    r_opt = opts["rand"]
    if r_opt != -1:
        print("# Fixed random seed:", r_opt)
        random.seed(r_opt)
    text_model = markovify.Text(text, state_size=1)
    iters = 100
    code, msg = run_tests(text_model, iters=iters, debug=debug)
    assert code == 0, msg
    if msg:
        print("# Note:", msg)
    return code

def run_tests(text_model, iters=100, debug=0):
    max_t = 100
    form = {}
    test_out = False
    for idx, _ in enumerate(range(iters), 1):
        if debug > 0:
            print(f"Iteration# {idx}/{iters}: ", end="")
        astr = text_model.make_short_sentence(
            max_chars=940,
            min_chars=20,
            tries=max_t,
            test_output=test_out,
        )
        assert astr is not None, "Not different enough?"
        print(astr, end="\n\n")
        if astr in form:
            form[astr] += 1
        else:
            form[astr] = 1
    any_r, any_c = "", 0
    for astr, cnt in form.items():
        if cnt <= 1:
            continue
        any_c += 1
        print(f"# Repeated ({cnt}x): '{astr}'")
        if not any_r:
            any_r = astr
    if any_c > 0:
        return 0, f"Repeated ({any_c}), first was: '{any_r}'"
    return 0, ""

# Main script
if __name__ == "__main__":
    main()
