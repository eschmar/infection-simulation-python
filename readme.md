The goal of this simulation experiment is to determine the necessary probability of an infectious disease to become epidemic, under certain predefined constraints. An epidemic is reached, once more than 50% of the population is infected.

# setup
```
pip install numpy scipy pylab
```

# example usage:

run.py:
```
python run.py -N 40 -S 0.04 -L 0 -minDays 6 -maxDays 9 -x 20,20 --print
```

tests.py:
```
python tests.py
```

simulation.py:
```
python evaluation.py -rangeFrom 0 -rangeTo 10 --save
```
