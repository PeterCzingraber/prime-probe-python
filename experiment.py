from psychopy import visual, core, event
import random
import os
from datetime import datetime

# Parameters
PRIME_DURATION   = 0.133  
BLANK_DURATION   = 0.033
PROBE_DURATION   = 0.133   
PROBE_WINDOW     = 1.000  
FIXATION_MIN     = 0.400
FIXATION_MAX     = 0.600
FEEDBACK_DURATION = 0.700
SLOW_CUTOFF      = 1.000  

RESPONSE_KEYS = ['a', 'e', 'n', 'l', 'escape']

N_PRACTICE   = 10
N_EXPERIMENT = 50

# Define trials
ALL_TRIALS = [
    # Horizontal congruent
    {"prime": "bal\nbal\nbal", "probe": "bal",  "correct": "a", "congruency": "congruent",   "name": "horizontal_con_1"},
    {"prime": "jobb\njobb\njobb","probe": "jobb","correct": "l", "congruency": "congruent",   "name": "horizontal_con_2"},
    # Horizontal incongruent
    {"prime": "bal\nbal\nbal", "probe": "jobb", "correct": "l", "congruency": "incongruent", "name": "horizontal_incon_1"},
    {"prime": "jobb\njobb\njobb","probe": "bal", "correct": "a", "congruency": "incongruent", "name": "horizontal_incon_2"},
    # Vertical congruent
    {"prime": "fel\nfel\nfel", "probe": "fel",  "correct": "e", "congruency": "congruent",   "name": "vertical_con_2"},
    {"prime": "le\nle\nle",   "probe": "le",   "correct": "n", "congruency": "congruent",   "name": "vertical_con_1"},
    # Vertical incongruent
    {"prime": "fel\nfel\nfel", "probe": "le",   "correct": "n", "congruency": "incongruent", "name": "vertical_incon_1"},
    {"prime": "le\nle\nle",   "probe": "fel",  "correct": "e", "congruency": "incongruent", "name": "vertical_incon_2"},
]

def make_alternating_block(n_trials):
    horizontal = [t for t in ALL_TRIALS if "horizontal" in t["name"]]
    vertical   = [t for t in ALL_TRIALS if "vertical"   in t["name"]]

    block = []
    axis = random.choice(["horizontal", "vertical"])
    for _ in range(n_trials):
        pool = horizontal if axis == "horizontal" else vertical
        block.append(random.choice(pool).copy())
        axis = "vertical" if axis == "horizontal" else "horizontal"
    return block


#In

def show_text_and_wait(win, text, keys=['space'], height=0.07):
    stim = visual.TextStim(win, text=text, height=height,
                           wrapWidth=1.6, color='white', alignText='center')
    stim.draw()
    win.flip()
    event.clearEvents()
    event.waitKeys(keyList=keys)


def run_trial(win, fixation, prime_stim, blank_stim, probe_stim,
              trial, clock, practice=False):

    # Fixation
    fix_duration = random.uniform(FIXATION_MIN, FIXATION_MAX)
    fixation.draw()
    win.flip()
    core.wait(fix_duration)

    # Prime
    prime_stim.setText(trial["prime"])
    prime_stim.draw()
    win.flip()
    core.wait(PRIME_DURATION)

    # Blank
    blank_stim.draw()
    win.flip()
    core.wait(BLANK_DURATION)

    # Probe — show stimulus then blank, collect response during full window
    probe_stim.setText(trial["probe"])
    probe_stim.draw()
    win.flip()
    clock.reset()
    event.clearEvents()

    # Stimulus on screen
    core.wait(PROBE_DURATION)

    # Blank for remainder of window, still collecting
    blank_stim.draw()
    win.flip()

    remaining = PROBE_WINDOW - PROBE_DURATION
    keys = event.waitKeys(maxWait=remaining, keyList=RESPONSE_KEYS,
                          timeStamped=clock)

    # Parse response
    response = None
    rt = None

    if keys:
        response, rt = keys[0]
        if response == 'escape':
            win.close()
            core.quit()
        # If key was pressed during probe display, rt is already correct
        # If pressed during blank, it was captured by waitKeys with timeStamped clock

    correct = (response == trial["correct"]) if response else False
    slow    = (rt is None) or (rt > SLOW_CUTOFF)

    return {
        "response":   response,
        "rt":         rt,
        "correct":    correct,
        "slow":       slow,
        "prime":      trial["prime"].replace("\n", "/"),
        "probe":      trial["probe"],
        "congruency": trial["congruency"],
        "name":       trial["name"],
        "correct_response": trial["correct"],
    }


def show_feedback(win, result, clock):
    if result["slow"] or result["rt"] is None:
        msg = "Túl lassú!"
        color = "red"
    elif not result["correct"]:
        msg = "Hibás válasz!"
        color = "red"
    else:
        return  # correct and fast: no feedback, blank already shown

    fb = visual.TextStim(win, text=msg, height=0.08, color=color)
    fb.draw()
    win.flip()
    core.wait(FEEDBACK_DURATION)


# Main experiment function
def run_experiment():

  
    win = visual.Window(
        fullscr=True,
        color='black',
        units='norm',
        allowGUI=False
    )
    core.wait(0.5)  # brief pause to ensure window is ready

#stimuli
    fixation   = visual.TextStim(win, text='+', height=0.12, color='white')
    blank_stim = visual.TextStim(win, text='',  height=0.08, color='white')
    prime_stim = visual.TextStim(win, text='',  height=0.08, color='white',
                                  alignText='center')
    probe_stim = visual.TextStim(win, text='',  height=0.10, color='white',
                                  bold=True)
    clock = core.Clock()

# Generate random subject code
    import string
    subj_code = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6))

#Welcome screen
    welcome_text = (
        "Üdvözlünk a kísérletben!\n"
        "Nyomj SZÓKÖZT a folytatáshoz."
    )
    show_text_and_wait(win, welcome_text, keys=['space'])

#Instructions
    instructions_text = (
        "FELADAT\n\n"
        "Minden körben egy rövid szót látsz (prime), majd egy célingerszót (probe).\n"
        "A célingerszóra a megfelelő gombbal reagálj:\n"
       "    bal    -    A\n"
       "    jobb   -    L\n"
       "    fel    -    E\n"
       "    le     -    N\n\n"
        "Reagálj a lehető leggyorsabban és legpontosabban!\n"
        "Nyomj SZÓKÖZT a gyakorláshoz.\n"
    )
    show_text_and_wait(win, instructions_text, keys=['space'], height=0.055)

#Practice block
    practice_trials = make_alternating_block(N_PRACTICE)

    practice_intro = (
        "GYAKORLÁS\n\n"
        f"{N_PRACTICE} gyakorló kör következik.\n"
        "Helytelen vagy lassú válasz esetén visszajelzést kapsz.\n"
        "Nyomj SZÓKÖZT a kezdéshez.\n"
    )
    show_text_and_wait(win, practice_intro, keys=['space'])

    practice_results = []
    for trial in practice_trials:
        result = run_trial(win, fixation, prime_stim, blank_stim,
                           probe_stim, trial, clock, practice=True)
        show_feedback(win, result, clock)
        practice_results.append(result)

# Practice summary
    n_correct  = sum(1 for r in practice_results if r["correct"])
    accuracy   = n_correct / N_PRACTICE * 100
    prac_end_text = (
        f"Gyakorlás vége!\n\n"
        f"Pontosság: {accuracy:.0f}%\n\n"
        "Most a valódi kísérlet következik — visszajelzés nem lesz.\n"
        "Nyomj SZÓKÖZT a kezdéshez.\n"
    )
    show_text_and_wait(win, prac_end_text, keys=['space'])

#Experimental block
    exp_trials = make_alternating_block(N_EXPERIMENT)

    exp_results = []
    for i, trial in enumerate(exp_trials):
        result = run_trial(win, fixation, prime_stim, blank_stim,
                           probe_stim, trial, clock, practice=False)
        result["trial_number"] = i + 1
        result["block"]        = "experimental"
        result["subj_code"]    = subj_code
        exp_results.append(result)

#Save data
    os.makedirs("data", exist_ok=True)
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"data/{subj_code}_{timestamp}.csv"

    import csv
    fieldnames = ["subj_code", "trial_number", "block", "name",
                  "prime", "probe", "congruency",
                  "correct_response", "response", "rt", "correct", "slow"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in exp_results:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

#End of experiment
    n_correct_exp = sum(1 for r in exp_results if r["correct"])
    acc_exp       = n_correct_exp / N_EXPERIMENT * 100

    end_text = (
        "A kísérlet véget ért!\n"
        f"Pontosság: {acc_exp:.0f}%\n\n"
        f"Adatok mentve:\n{filename}\n\n"
        "Köszönjük a részvételt!\n"
        "Nyomj SZÓKÖZT a kilépéshez.\n"
    )
    show_text_and_wait(win, end_text, keys=['space'])

    win.close()
    core.quit()


if __name__ == "__main__":
    run_experiment()