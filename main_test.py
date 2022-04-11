from pathlib import Path
import pandas as pd

from load_holdet_highscore import load_holdet_highscore_data

def main():
    #### INPUT ####
    Liga_all = ["1. Premier League",
                "2. La Liga", #2. La liga
                "3. Bundesliga",
                "4. Superliga",
                "9. Serie A",
                "99. Champions League"]

    output_folder = Path(__file__).parent

#--------------------------------------------------------------------------

    holdet_highscore_run = [1, 2, 3, 4, 5, 6, 7] #Kører de 7 ligaer

    if len(holdet_highscore_run) > 0:
        n_pages = 4
        load_holdet_highscore_data(holdet_highscore_run, Liga_all, n_pages)

if __name__ == '__main__':
    main()

