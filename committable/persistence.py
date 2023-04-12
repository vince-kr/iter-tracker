class Persistence:
    def read(db_path: str) -> tuple:
        return (
            5,
            "2023-04-01",
            {
                "description": "3hrs studying Fluent Python (at least finish ch.5, which is 30 more pages); 1hr practicing TCR.",
                "target_in_minutes": 240,
            },
            {
                "description": "I want to implement showing the progress on an iteration in terms of percentage of the time goal versus how much of the iteration has passed. I also want to keep working on the note transposing problem. Say 3hrs for Iteration-Tracker and 1hr on music.",
                "target_in_minutes": 270,
            },
            [],
        )
