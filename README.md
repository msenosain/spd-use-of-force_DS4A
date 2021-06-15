Assessing Crisis Intervention Training By Seattle Police Department
==============================

Capston project from Team #120 as part of the DS4A/Empowerment program

Business Problem
--------

Since 2012, Seattle’s Police Department (SPD) has been under federal oversight because in 2011, an assessment found that excessive force on a consistent basis rather than attempted deescalation measures. Moreover, the assessment in 2011 also revealed that 70% of SPD’s use of force involved civilians that were experiencing some type of crisis. As a result of this finding, SPD developed crisis intervention training and has implemented a policy in which SPD officers receive 8 hours of crisis intervention training annually and are considered “CIT-Certified” after completing an initial 40 hr crisis training foundation. SPD increased its number of CIT-Certified officers from 2014 to early 2020 before the COVID-19 pandemic. Thereafter, the training was suspended but is expected to resume in Q2 of 2021.

The CIT training is meant to reduce the number of times excessive force is used. Thus, the main problem to be solved is to look at various metrics related to training—e.g. # of trainings and # of personnel trained— as well as knowledge of current events and trends—e.g. The COVID-19 pandemic— and understand their relationship to the type of force used.
There are also specific questions that the client is looking to answer, such as:

* What are the trends on Crisis Intervention Training?

* Are there differences in outcomes depending on the CIT modalities that SPD officers were trained? [CIT-Trained (8 yearly hours of training), CIT-Certified, or not being trained on CIT at all]

* Is the use-of-force in situations of crisis decreasing?

* Is there evidence of de-escalation during situations of crisis?

* Where are areas for improvement?

* What trends can be found?

* What are key questions that the data cannot answer, which should be included in future CIIT reports

Furthermore, the group will evaluate how different communities are impacted by U of F cases and whether or not there is a disproportionate amount of U of F cases within these communities. Questions we would also like to answer:

* How is society impacted by U of F?

* What metrics can be made for the department to monitor and track progress?


Business Impact
--------

Since SPD (the client) is under federal oversight, it is important for it to demonstrate the effectiveness of the crisis intervention initiative by hopefully showing improvement in outcomes, i.e. reduced use of excessive force. Additionally, this problem is important because a considerable quantity of civilians impacted by SPD’s excessive force measures of the past have been people experiencing some type of crisis. Thus, insights derived from exploring the problem space can help better serve this segment of the population.

In determining how minorities are impacted by U of F cases, recommendations can be made to provide more support to the department and community to improve the rates of U of F. The department will also be provided with a dashboard for monitoring these key performance indicators. 

Being under federal oversight, the result of this analysis is intended to help the Seattle Police Department (SPD) be free from the Department of Justice (DOJ) oversight. Other ways it will impact SPD are;

1. Provide SPD with an overview of their unit's practice with regards to responses to police requests from the region they serve.

2. Help understand the impact of their responses on the community

3. Understand how and why Use of Force is being used in arrests

4. Help properly identify and address situations with encounters involving people experiencing some type of crisis

5. Provide information on the effectiveness of training that officers received and its importance.

6. Mental assessment impact of arrests and Covid-19 pandemic on policing

7. Provide relevant information to help SPD make impactful decisions that contribute to a drastically reduced Use of Force encounter

Amongst this is the overarching goal of community impact and relation which leads to a safer society and provides a point to focus on improvement efforts.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
