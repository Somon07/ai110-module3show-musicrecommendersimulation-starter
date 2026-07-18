import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Weighted score for one song against the user's profile."""
        score = 0.0
        # Categorical traits must match exactly.
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.5
        # Numeric trait scored by closeness: closer energy -> higher score.
        score += 1.0 * (1 - abs(song.energy - user.target_energy))
        # Acoustic preference nudges the score in the user's direction.
        if user.likes_acoustic:
            score += 0.5 * song.acousticness
        else:
            score += 0.5 * (1 - song.acousticness)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Rank every song high-to-low by its weighted score, return the top k.
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons: List[str] = []
        if song.genre == user.favorite_genre:
            reasons.append(f"it's {song.genre}, your favorite genre")
        if song.mood == user.favorite_mood:
            reasons.append(f"its mood is {song.mood}, which matches yours")
        if abs(song.energy - user.target_energy) <= 0.15:
            reasons.append(f"its energy ({song.energy:.2f}) is close to your target ({user.target_energy:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("it's fairly acoustic, which you like")

        if not reasons:
            return f"'{song.title}' was included as a filler pick — no strong matches to your profile."
        return f"'{song.title}' was recommended because " + ", and ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts, converting numeric fields to int/float."""
    print(f"Loading songs from {csv_path}...")

    songs: List[Dict] = []

    # Columns that must be converted from text so we can do math with them later.
    int_fields = ("id", "tempo_bpm")
    float_fields = ("energy", "valence", "danceability", "acousticness")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                if row.get(field) not in (None, ""):
                    row[field] = int(row[field])
            for field in float_fields:
                if row.get(field) not in (None, ""):
                    row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song dict against user_prefs, returning (numeric_score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical traits must match exactly (highest weights).
    if user_prefs.get("genre") is not None and song.get("genre") == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if user_prefs.get("mood") is not None and song.get("mood") == user_prefs["mood"]:
        score += 1.5
        reasons.append(f"mood match: {song['mood']} (+1.5)")

    # Numeric trait scored by closeness: the nearer the energy, the higher the score.
    if user_prefs.get("energy") is not None and song.get("energy") is not None:
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        energy_points = 1.0 * closeness
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{energy_points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), highest first."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches — filler pick"
        scored.append((song, score, explanation))

    # Rank all evaluated songs from highest to lowest score.
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
