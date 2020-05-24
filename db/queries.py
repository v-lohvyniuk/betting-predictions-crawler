create_table = """CREATE TABLE IF NOT EXISTS public.predictions_queue
(
    first_team "char"[] NOT NULL,
    second_team "char"[] NOT NULL,
    first_team_win "char"[] NOT NULL,
    draws "char"[] NOT NULL,
    second_team_win "char"[] NOT NULL,
    event_date "char"[] NOT NULL,
    PRIMARY KEY (first_team, second_team)
);

ALTER TABLE public.predictions_queue
    OWNER to gtvdrkjgsvphfm;
    """