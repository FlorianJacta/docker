from taipy import Gui
import pandas as pd
import time
from taipy.gui import(
    Markdown,
    notify,
    get_state_id,
    invoke_long_callback,
)



calculate_label = "Calc"
calculate_label_active = True
df = pd.DataFrame({"V": [21], "W": [22], "X": [23],"Y": [24],"Z": [25]})

def calculate_action(state):
    state.calculate_label = "0"
    state.df = pd.DataFrame({"V": [21], "W": [22], "X": [23],"Y": [24],"Z": [25]})

    invoke_long_callback(state,
        user_function=do_calculate,
        user_function_args=[get_state_id(state)],
        user_status_function=get_status_calculate,
        period=1000)

def get_status_calculate(state, status, result):
    if isinstance(status, bool):
        if status:
            notify(state, "success", "Heavy set function finished!")
            state.df = result

            state.calculate_label = "Calc"
        else:
            notify(state, "error", "Something went wrong")
        
    else:
        state.calculate_label = str(int(state.calculate_label)+1)


def do_calculate(state_id):
    time.sleep(15)
    df_old = pd.DataFrame({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5]})
    df_new = pd.DataFrame({"A": [12], "B": [14], "C": [16], "D": [18], "E": [20]})
    try:
        df_result = df_new.subtract(df_old, fill_value=0)
    except Exception as ex:
        raise ex
    
    return df_result

calc_md = Markdown(
    """
<|{calculate_label}|button|on_action=calculate_action|active={calculate_label_active}|>

<|{df}|table|>
"""
)

pages = {"taipy/Calculate": calc_md}


if __name__=="__main__":
    port = 8080
    Gui(pages=pages).run(title="Test", dark_mode=True, port=port, host="0.0.0.0")

else:
    app = Gui(pages=pages).run(title="Test", dark_mode=True, run_server=False, base_url="test")