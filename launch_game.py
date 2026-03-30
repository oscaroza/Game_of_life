from welcome import show_welcome


def main():
    should_start_game = show_welcome(duration_seconds=3)
    if not should_start_game:
        return

    # UI.py lance sa boucle principale au chargement du module.
    import UI


if __name__ == "__main__":
    main()
