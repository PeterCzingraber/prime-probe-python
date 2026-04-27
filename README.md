# Hi! This is a university project work. I'll makle a simple prime-probe design in python.

---

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Key dependencies include `psychopy`, `numpy`, `pandas`. See `requirements.txt` for the full list.

---

## Running the Experiment

```bash
python experiment.py
```

The experiment runs in fullscreen. Press **Escape** at any time to quit.

---

## Configurable Parameters

All parameters are defined as constants at the top of `experiment.py` and can be adjusted in the code.

| Parameter | Default value | Description |
|---|---|---|
| `PRIME_DURATION` | `0.133` s | How long the prime stimulus is displayed |
| `BLANK_DURATION` | `0.033` s | Blank interval between prime and probe |
| `PROBE_DURATION` | `0.133` s | How long the probe stimulus is displayed |
| `PROBE_WINDOW` | `1.000` s | Total response window from probe onset |
| `FIXATION_MIN` | `0.400` s | Minimum fixation cross duration (jittered) |
| `FIXATION_MAX` | `0.600` s | Maximum fixation cross duration (jittered) | 
| `FEEDBACK_DURATION` | `0.700` s | How long error/slow feedback is shown |
| `SLOW_CUTOFF` | `1.000` s | RT threshold above which a response is flagged as slow |
| `N_PRACTICE` | `10` | Number of practice trials |
| `N_EXPERIMENT` | `50` | Number of experimental trials |

---

## Trial Design

Each trial consists of a fixation cross, a prime (shown three times, stacked vertically), a blank, and a probe word. Participants press the key corresponding to the probe's direction.

### Response key mapping

| Word | Key |
|---|---|
| `bal` (left) | **A** |
| `jobb` (right) | **L** |
| `fel` (up) | **E** |
| `le` (down) | **N** |

### Trial types

There are 8 unique trial templates across two axes and two congruency conditions:

| Axis | Congruency | Prime → Probe |
|---|---|---|
| Horizontal | Congruent | bal → bal, jobb → jobb |
| Horizontal | Incongruent | bal → jobb, jobb → bal |
| Vertical | Congruent | fel → fel, le → le |
| Vertical | Incongruent | fel → le, le → fel |

Trials are sampled with alternation between axes (horizontal ↔ vertical) throughout each block.

---

## Output

### File location

Data is saved automatically at the end of the experimental block to:

```
data/<subj_code>_<YYYYMMDD_HHMMSS>.csv
```

The `data/` directory is created automatically if it does not exist. The subject code is a randomly generated 6-character alphanumeric string (e.g. `F3uGoh`).

### Saved columns

| Column | Type | Description |
|---|---|---|
| `subj_code` | string | Randomly generated participant identifier |
| `trial_number` | integer | Sequential trial index (1-based) |
| `block` | string | Always `"experimental"` for saved data |
| `name` | string | Trial template name (e.g. `vertical_incon_1`) |
| `prime` | string | Prime word(s), slash-separated (e.g. `fel/fel/fel`) |
| `probe` | string | Probe word shown to participant |
| `congruency` | string | `"congruent"` or `"incongruent"` |
| `correct_response` | string | Expected key press |
| `response` | string | Actual key pressed (empty if no response) |
| `rt` | float | Reaction time in seconds from probe onset |
| `correct` | boolean | Whether response matched the correct key |
| `slow` | boolean | `True` if RT exceeded `SLOW_CUTOFF` or no response was given |

> **Note:** Practice block data is not saved to disk — only experimental trials are written to the CSV.

---

## Notes

- The fixation duration is jittered randomly between `FIXATION_MIN` and `FIXATION_MAX` on each trial to reduce anticipatory responses.
- Feedback (error or slow) is shown during practice only.