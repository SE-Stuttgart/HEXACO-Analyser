#!/usr/bin/env python
""" Calculates personality profiles based on the HEXACO-100 test inventory

The HEXACO-PI-R is a validated personality test. You can find more detailed
information and the inventories themselves here: http://www.hexaco.org
In its current version it only works with the HEXACO-100 inventory. It
expects a CSV file with columns with the headings q1 to q100 for the 100
items in the inventory. Change the name of this file to your results file.
It then reverses the questions as prescribed by HEXACO-PI-R and summarises
each major personality trait. The results are written into a file called
personality.csv.


This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Stefan Wagner"
__contact__ = "stefan.wagner@iste.uni-stuttgart.de"
__copyright__ = "Copyright 2020, Stefan Wagner"
__date__ = "2021/02/01"
__deprecated__ = False
__license__ = "GPLv3"
__status__ = "Production"
__version__ = "0.0.1"


import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from numpy import nanmean
from numpy import isnan

traitNames = [
    "Honesty-Humility", "Sincerity", "Fairness",
    "Greed-Avoidance", "Modesty", "Emotionality",
    "Fearfulness", "Anxiety", "Dependence",
    "Sentimentality", "eXtraversion", "Social Self-Esteem",
    "Social Boldness", "Sociability", "Liveliness",
    "Agreeableness", "Forgivingness", "Gentleness",
    "Flexibility", "Patience", "Conscientiousness",
    "Organization", "Diligence", "Perfectionism",
    "Prudence", "Openness to Experience", "Aesthetic Appreciation",
    "Inquisitiveness", "Creativity", "Unconventionality",
    "Altruism"
]


def reverse(item_value):
    if item_value == 1:
        return 5
    elif item_value == 2:
        return 4
    elif item_value == 3:
        return 3
    elif item_value == 4:
        return 2
    elif item_value == 5:
        return 1



# Read raw questionnaire data from file
df = pd.read_csv('results.csv')


# Reverse items that need to be reversed for further analysis
reversal_questions = ["q6", "q54", "q12", "q36", "q84", "q42", "q66", "q90", "q72", "q96", "q29", "q77", "q35", "q59",
                      "q41", "q89", "q95", "q52", "q76", "q10", "q82", "q16", "q70", "q94", "q51", "q75", "q9", "q15",
                      "q63", "q87", "q21", "q93", "q50", "q74", "q56", "q80", "q38", "q20", "q44", "q92", "q1", "q25",
                      "q55", "q79", "q13", "q85", "q19", "q91", "q99", "q100"]

df[reversal_questions] = df[reversal_questions].applymap(reverse)


# Calculate means for individual traits

honesty_humility_questions = ["q6", "q30", "q54", "q78", "q12", "q36", "q60", "q84", "q18", "q42", "q66", "q90", "q24",
                              "q48", "q72", "q96"]
personality = pd.DataFrame(df[honesty_humility_questions].mean(axis=1))
personality.columns = ['Honesty-Humility']

emotionality_questions = ["q5", "q29", "q53", "q77", "q11", "q35", "q59", "q83", "q17", "q41", "q65", "q89", "q23",
                          "q47", "q71", "q95"]
emotionality = pd.DataFrame(df[emotionality_questions].mean(axis=1))
emotionality.columns = ['Emotionality']
personality = personality.merge(emotionality, left_index=True, right_index=True)

extraversion_questions = ["q4", "q28", "q52", "q76", "q10", "q34", "q58", "q82", "q16", "q40", "q64", "q88", "q22",
                          "q46", "q70", "q94"]
extraversion = pd.DataFrame(df[extraversion_questions].mean(axis=1))
extraversion.columns = ['Extraversion']
personality = personality.merge(extraversion, left_index=True, right_index=True)

agreeableness_questions = ["q3", "q27", "q51", "q75", "q9", "q33", "q57", "q81", "q15", "q39", "q63", "q87", "q21",
                           "q45", "q69", "q93"]
agreeableness = pd.DataFrame(df[agreeableness_questions].mean(axis=1))
agreeableness.columns = ['Agreeableness']
personality = personality.merge(agreeableness, left_index=True, right_index=True)

conscientiousness_questions = ["q2", "q26", "q50", "q74", "q8", "q32", "q56", "q80", "q14", "q38", "q62", "q86",
                               "q20", "q44", "q68", "q92"]
conscientiousness = pd.DataFrame(df[conscientiousness_questions].mean(axis=1))
conscientiousness.columns = ['Conscientiousness']
personality = personality.merge(conscientiousness, left_index=True, right_index=True)

openness_questions = ["q1", "q25", "q49", "q73", "q7", "q31", "q55", "q79", "q13", "q37", "q61", "q85", "q19", "q43",
                      "q67", "q91"]
openness = pd.DataFrame(df[openness_questions].mean(axis=1))
openness.columns = ['Openness to Experience']
personality = personality.merge(openness, left_index=True, right_index=True)

altruism_questions = ["q97", "q98", "q99", "q100"]
altruism = pd.DataFrame(df[altruism_questions].mean(axis=1))
altruism.columns = ['Altruism']
personality = personality.merge(altruism, left_index=True, right_index=True)

print(personality)

personality.to_csv("personality.csv")