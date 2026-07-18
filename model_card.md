# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

## 2. Intended Use

Recommends songs from a small catalog based on a listener's favorite genre, mood,
and target energy. Built for **classroom exploration**, not real users.

## 3. How the Model Works

Each song earns points, then songs are sorted highest-to-lowest:

- **Genre match:** +2.0
- **Mood match:** +1.5
- **Energy closeness:** `1 − |song_energy − target|` (up to +1.0)

Genre and mood are all-or-nothing; energy is a sliding scale. The top 5 totals
become the recommendations.

## 4. Data

Only **10 songs** in `data/songs.csv`, and the genres are unbalanced: lofi (3),
pop (2), and rock/ambient/jazz/synthwave/indie pop (1 each). Whole categories
(hip-hop, classical, sad moods) are missing, so the model can't recommend them.

## 5. Strengths

- For well-represented tastes (pop/happy, lofi/chill, rock/intense), the #1 pick
  is exactly what a human would choose.
- Every recommendation shows its point breakdown, so it's clear *why* a song ranked.
- It won't crash on missing or unknown preferences — it scores whatever fields exist.

## 6. Limitations and Bias

The main weakness is a **filter bubble caused by the tiny, pop-heavy dataset**.
With only 10 songs, high-energy pop tracks like *Gym Hero* keep surfacing across
unrelated users — it appeared in the top 5 for **three** different profiles
(High-Energy Pop, Deep Intense Rock, and "loud + sad"). A second bias: the energy
term **always adds points** (`1 − |gap|` is never zero), so *every* song gets some
credit and the top-5 list always fills up — even for a user whose genre and mood
match nothing. Finally, the model is **blind to tastes it has no data for**, so
those users silently get irrelevant filler instead of an honest "no match."

## 7. Evaluation

I tested six profiles (defined in `src/main.py`, run with `python -m src.main`) —
three realistic and three adversarial. Top 3 of each shown below.

**High-Energy Pop** `{pop, happy, 0.9}`
```
1. Sunrise City   4.42  (genre +2.0, mood +1.5, energy +0.92)
2. Gym Hero       2.97  (genre +2.0, energy +0.97)
3. Rooftop Lights 2.36  (mood +1.5, energy +0.86)
```
**Chill Lofi** `{lofi, chill, 0.3}`
```
1. Library Rain    4.45  (genre +2.0, mood +1.5, energy +0.95)
2. Midnight Coding 4.38  (genre +2.0, mood +1.5, energy +0.88)
3. Focus Flow      2.90  (genre +2.0, energy +0.90)
```
**Deep Intense Rock** `{rock, intense, 0.95}`
```
1. Storm Runner 4.46  (genre +2.0, mood +1.5, energy +0.96)
2. Gym Hero     2.48  (mood +1.5, energy +0.98)
3. Sunrise City 0.87  (energy +0.87)  <- filler
```
**Conflicted (loud + sad)** `{pop, sad, 0.9}` — *"sad" isn't in the catalog*
```
1. Gym Hero     2.97  (genre +2.0, energy +0.97)
2. Sunrise City 2.92  (genre +2.0, energy +0.92)
3. Storm Runner 0.99  (energy +0.99)  <- mood never matched, energy took over
```
**Unknown Tastes** `{k-pop, party, 0.5}` — *neither genre nor mood exists*
```
1. Midnight Coding 0.92  (energy +0.92)
2. Focus Flow      0.90  (energy +0.90)  <- entire list is energy-only filler
3. Coffee Shop...  0.87  (energy +0.87)
```
**Genre Only (lofi)** `{lofi}` — *mood/energy keys missing*
```
1-3. three lofi songs tied at 2.00 (genre only); rest score 0.00 filler
```

**What surprised me:** the "Unknown Tastes" user still got a confident-looking top
5 built purely on energy padding — the system never says "no match." The "loud +
sad" conflict didn't break anything either; the mood weight just never fired.

**Pairwise comparisons:**
- *High-Energy Pop vs Chill Lofi:* near-opposites, and it shows — Pop pulls loud
  tracks up (*Sunrise City*, 0.82), Lofi pulls quiet ones (*Library Rain*, 0.35).
  The energy target genuinely steers the list. ✅
- *High-Energy Pop vs Deep Intense Rock:* both want high energy, so they **share**
  *Gym Hero* at #2 despite asking for different genres — because it's pop AND
  intense AND loud. This is the filter bubble in miniature.
- *Chill Lofi vs Genre Only (lofi):* same genre, but Chill Lofi cleanly ranks
  *Library Rain* first while Genre Only ties all three lofi songs at 2.00. Shows
  mood and energy are what create a meaningful *order*, not genre alone.

**Data experiment (energy ×2, genre ×0.5):** for High-Energy Pop, *Rooftop
Lights* (mood + close energy) jumped #3 → #2, pushing genre-only *Gym Hero* down.
The result was **different and arguably more accurate** for a "vibe" app, but it
weakened the signal users state most confidently, so I reverted.

**Why "Gym Hero" keeps showing up for "Happy Pop" (plain language):** score it
like a game. *Gym Hero* is pop (big genre points) and very high energy (nearly all
the energy points), so it nails 2 of the 3 boxes even though its mood is "intense,"
not "happy." With only two pop songs in the catalog, there's no better pop track to
bump it down. A bigger, more varied library would give it real competition.

## 8. Future Work

Add a "no match" signal instead of energy-only filler; grow and balance the
catalog; use the unused features (valence, danceability, acousticness); and
penalize near-duplicates so one vibe doesn't fill the whole top 5.

## 9. Personal Reflection

A recommender is really just **arithmetic plus sorting** — no understanding of
music, only points added and ranked. What surprised me most is how confidently it
recommends to users it has no real match for, which reframed how I see apps like
Spotify: some of a playlist is a genuine match and some is just the algorithm
filling space, and the interface makes both look equally intentional.
