# Apple Health Export Insights

This project born because I was looking at Apple Health graphics and dashboards and, honestly, I don't really like them so much.

I think the data is very interesting, but the way Apple show it is not exactly how I want to understand my own body, habits, workouts, sleep, heart rate and health patterns. So I decided to create my own app to parse the Apple Health exported data and generate my own insights after.

The first idea was simple: read the exported files from iPhone and create some dashboards. But when I saw the files size, like hundreds of MBs, I understood that this is not just a dashboard project. This is also a good challenge to study Python, data structures, performance, streaming, queues, Postgres and concurrency.

So this project is not only about health data. It is also a personal engineering lab.

## Main idea

The central idea is:

```text
Apple Health export files
        ↓
streaming parser
        ↓
structured data
        ↓
Postgres
        ↓
queries and insights
        ↓
my own dashboard/app
```

I don't want to work directly with the big XML every time. The XML is too big and it is not a good format for analysis.

The goal is to parse it once, save the data in a database, and then create the insights from there.

## Why I am building this

I want to:

* understand my Apple Health data better;
* create my own metrics and charts;
* explore patterns in heart rate, sleep, workouts, steps and activity;
* learn how to process big files without breaking memory;
* train Python performance concepts in a real project;
* use Postgres from the beginning;
* practice algorithms, data structures and concurrency with something real.

This project is also a challenge for myself. I want to make it step by step, understanding what is happening and not just copying code.
::: 

# Project Currently Structure

```
apple_health_export
├─ .editorconfig
├─ README.md
├─ notebooks
│  ├─ README.md
│  └─ playground.ipynb
├─ poetry.lock
├─ pyproject.toml
└─ src
   ├─ __init__.py
   ├─ app.py
   ├─ config
   │  ├─ __init__.py
   │  ├─ logger.py
   │  └─ settings.py
   └─ parser
      ├─ __init__.py
      ├─ base_parser.py
      └─ xml_parser.py

```