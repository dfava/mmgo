# mmGo
### Operational Semantics of a Weak Memory Model with Channel Synchronization

This is an implementation, in the [K-framework](http://www.kframework.org), of a weak memory model for a calculus inspired by the [Go](https://golang.org/) programming language. The model has buffered channel communication as the sole synchronization primitive.

Details of the memory model can be found in the following [technical report](http://folk.uio.no/danielsf/papers/fava2017operational.pdf).


## Install

It uses the K executable semantics framework.  Follow installation instructions from [K's github page](https://github.com/kframework/k).  It requires the Java Development Kit, Apache Maven.

## Running
Once K is installed, it is easy to run an example by following the steps:

#### 1. ```kompile```

```
cd src/k/mmgo-dw
kompile mmgo.k
```

#### 2. ```krun```
From ```src/k/mmgo-dw```:

```
krun ../../mmgo/example/example.mmgo | ../../../bin/kprint.py
```

This pipes the output to a pretty printer in ```bin```.  If you don't have Python (or the pretty printer does not work for you), you can also leave it out:

```
krun ../../mmgo/example/example.mmgo
```

This runs the *delayed-writes* version of the memory model (```mmgo-dw```).  There is also a sequentially consistent version of the memory model, which you can run by replacing ```mmgo-dw``` with ```mmgo-sc```.


## Development
These step are only required if you want to further develop ```mmgo```.

It assumes you have Python3 installed and assumes that you checked out the mmgo repository at ```~/mmgo```.


#### 1. Set-up for running regression tests
It is recommended to:

- add ```$HOME/mmgo/bin``` and ```$HOME/mmgo/lib``` to your ```PYTHONPATH```; and
- add ```$HOME/mmgo/bin``` to ```PATH```.

One way to do this, for example, is by adding the following lines to a ```.bash_profile```:

```
export PYTHONPATH=$PYTHONPATH:$HOME/mmgo/bin:$HOME/mmgo/lib
export PATH=$PATH:$HOME/mmgo/bin
```

Install dependencies

- [pyparsing](http://pyparsing.wikispaces.com/), which can be installed with pip:<br/>```pip3 install pyparsing```

- an XML query language called [python-simplexquery](https://github.com/bellbind/python-simplexquery)

```
brew install xqilla
pip3 install python-simplexquery
```

The regression scripts also use the Python [unittest](https://docs.python.org/3.6/library/unittest.html) library, which should be installed by default.

#### 2. Running regression tests

Here is an example of running a single test, in this case ```var_write.mmgo```, using the *delayed-writes* version of the memory model called ```mmmgo-dw```

```
cd src/mmgo/tests
mmgo-run.py mmgo-dw var_write.mmgo
```

Here is an example of running all tests using the sequentially consistent version of the memory model, called ```mmgo-sc```

```
cd src/mmgo/tests
mmgo-run.py mmgo-sc *.mmgo
```