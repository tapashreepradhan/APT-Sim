START

    Read YAML configuration
    Setp up SETUP dictionary (simulation settings)

    ┌───────────────────────────┐
    │ Create "0" directory      │
    │ Initial Emitter Setup     │
    │                           │
    │   IF new emitter          │
    │      Build from scratch   │
    │   ELSE IF node file exists│
    │      Copy node file       │
    │   ELSE IF uc file exists  │
    │      Build from uc file   │
    └───────────────────────────┘

    Run Meshgen (generate mesh)

    Count initial atoms
    Convert % events (if needed)

    Prepare initial mesh (add coordination column)

    ┌───────────────────────────┐
    │ Run Initial LAMMPS Relax  │
    └───────────────────────────┘
    Step Counter = 1

    ┌───────────────────────────┐
    │ Evaporation Loop          │
    │                           │
    │   WHILE events < total    │
    │                           │
    │   Create step directory   │
    │   Copy relaxed emitter    │
    │   Run TAPSim (evaporation)│
    │   Count remaining atoms   │
    │   Run LAMMPS Relaxation   │
    │                           │
    │   IF cleanup              │
    │      Delete intermediate  │
    │                           │
    │   Step Counter += 1       │
    └───────────────────────────┘

    LOG: Evaporation complete

END