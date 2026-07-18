"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Named user profiles used for system evaluation.
# The first three are "normal" listeners; the last three are adversarial /
# edge-case profiles designed to try to trick the scoring logic.
PROFILES = {
    # --- Three distinct, realistic listeners ---
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},

    # --- Adversarial / edge-case profiles ---
    # Conflicting: wants high energy but a "sad" mood (no sad songs exist),
    # so the mood weight can never fire and energy has to carry the ranking.
    "Conflicted (loud + sad)": {"genre": "pop", "mood": "sad", "energy": 0.9},
    # Unknown tastes: genre and mood that aren't in the catalog at all,
    # so only the energy gap separates the songs.
    "Unknown Tastes": {"genre": "k-pop", "mood": "party", "energy": 0.5},
    # Sparse profile: only a genre is given (no mood, no energy key),
    # testing that scoring stays robust when preferences are missing.
    "Genre Only (lofi)": {"genre": "lofi"},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Score the catalog for one named profile and print its top 5 picks."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    header = f"{name}  ->  {user_prefs}"
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
        # explanation is a "; "-joined string of scoring reasons; show one per line.
        for reason in explanation.split("; "):
            print(f"     • {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
