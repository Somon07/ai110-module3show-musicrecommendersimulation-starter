# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

-My version will score every song and have a specific matching number for each songs. It lets the user pick their favorite genre & mood to be able to align the perfect music with their taste profile.


## How The System Works

Real world music recommender algorithm, transforms user preferences and song attributes to simulate a personalized recommedation field. it also filters categorical boundaries like genre and vibes and help filter to align with user' s interests. It also tracks data using a Song object containing features like genre and energy storing target preferences.

For my version, each use song will earn a weighted total score where traits must match exactly, where numeric attributes are scored based on mathematical closeness.For example (1-song-target). Genre is given the highest weight like 2.0,mood given a weight of (1.5), energy is given 1.0. Ultimately, ranking sorts all evaluated songs from highest to lowest score to return a personalized playlist.




---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Sample output for the default `genre=pop, mood=happy, energy=0.8` profile:

```
Loading songs from data/songs.csv...

================================================
Top 5 picks for genre=pop, mood=happy, energy=0.8
================================================

1. Sunrise City — Neon Echo  (score: 4.48)
     • genre match: pop (+2.0)
     • mood match: happy (+1.5)
     • energy 0.82 vs target 0.80 (+0.98)

2. Gym Hero — Max Pulse  (score: 2.87)
     • genre match: pop (+2.0)
     • energy 0.93 vs target 0.80 (+0.87)

3. Rooftop Lights — Indigo Parade  (score: 2.46)
     • mood match: happy (+1.5)
     • energy 0.76 vs target 0.80 (+0.96)

4. Night Drive Loop — Neon Echo  (score: 0.95)
     • energy 0.75 vs target 0.80 (+0.95)

5. Storm Runner — Voltline  (score: 0.89)
     • energy 0.91 vs target 0.80 (+0.89)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



