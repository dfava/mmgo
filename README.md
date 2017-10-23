# mmGo
### Operational Semantics of a Weak Memory Model with Channel Synchronization

This is an implementation, in the [K-framework](http://www.kframework.org), of a weak memory model for a calculus inspired by the [Go](https://golang.org/) programming language. The model has buffered channel communication as the sole synchronization primitive.


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


## Technical background
Details of the memory model can be found in the following [technical report](http://folk.uio.no/danielsf/papers/fava2017operational.pdf).
