# THE TRUST ENGINE
## The Evolution of Cooperation in a Connected World

### Project Overview

THE TRUST ENGINE explores how trust and cooperation evolve in a connected society.

The project investigates whether cooperation can survive in environments where betrayal may sometimes be more profitable than cooperation.

It combines real-world reputation data, experimental human behavior, and agent-based simulation to explore the mechanisms that influence trust.

### Research Question

**Can trust and cooperation survive in a society where betrayal can sometimes be more profitable?**

### Research Objectives

- Explore real-world reputation patterns in a connected network.
- Analyze human cooperation and defection in repeated Prisoner's Dilemma experiments.
- Simulate how memory, reputation, and social influence affect cooperation.
- Investigate how individual decisions and collective behavior shape trust.

### Data Sources

**1. Bitcoin OTC — Stanford SNAP**

A real-world network of signed trust ratings between Bitcoin OTC users.

- 5,881 nodes
- 35,592 directed ratings
- Ratings range from -10 to +10
- Data period: 2010–2016

Source: https://snap.stanford.edu/data/soc-sign-bitcoinotc.html

**2. Dryad — Repeated Prisoner's Dilemma Experiment**

Experimental human behavior data comparing fixed-partner and random-partner interactions.

- FIX: 9,200 interaction records
- RAND: 9,600 interaction records
- 188 participant-session records
- 100 rounds per participant-session

Source: https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk

**3. Agent-Based Simulation**

A synthetic environment where agents interact repeatedly using different strategies and behavioral mechanisms.

### Five Simulation Experiments

1. **Can Cooperation Survive?** — Investigating whether cooperation can persist among cooperative and defecting agents.
2. **The Cost of Betrayal** — Exploring how memory of previous interactions influences future decisions.
3. **Reputation Matters** — Testing whether reputation encourages cooperative behavior.
4. **The Collective Mind** — Investigating how social influence and group behavior affect individual decisions.
5. **The Reputation Trap** — Exploring whether unfair negative reputation signals can trigger cascading distrust.

### Technology Stack

- Python
- Pandas and NumPy
- NetworkX
- Snowflake
- dbt
- Apache Kafka
- Apache Airflow
- Streamlit
- Git and GitHub

### Data Engineering Architecture

The project follows a data pipeline approach:

1. Data ingestion from real-world datasets.
2. Data transformation and quality checks.
3. Storage in Snowflake.
4. Data modeling with dbt.
5. Streaming simulated interaction events with Kafka.
6. Pipeline orchestration with Airflow.
7. Data visualization with Streamlit.

### Project Structure

```text
the-trust-engine/
├── airflow/
├── dashboard/
├── data/
│   ├── raw/
│   ├── processed/
│   └── simulation/
├── dbt/
├── docs/
├── kafka/
├── notebooks/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── simulation/
│   └── streaming/
├── tests/
├── requirements.txt
└── README.md
```

### Important Research Limitations

- Bitcoin OTC ratings represent reputation signals, not direct observations of cooperation or fraud.
- Dryad data represents behavior in a controlled experimental setting and should not be generalized to the entire population.
- Simulation outcomes depend on model assumptions and do not establish real-world causal relationships.

### Project Status

**Day 1 — Data Discovery & Project Foundation: Completed**

- Project structure created.
- Datasets downloaded and explored.
- Initial Python ingestion pipeline implemented.
- Processed datasets saved and verified.

Further development: behavioral analysis, agent-based simulation, data platform integration, and dashboard development.