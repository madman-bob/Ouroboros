# Ouroboros

Ouroboros is an expressive interpreted programming language, for general purpose programming.
It focuses on bringing the power of Lisp, with the familiarity of C-based languages.
If the word "boilerplate" is ever used to describe an Ouroboros program, then I've done something wrong.

Part of the expressiveness comes from Ouroboros having no reserved words.
What, in many languages, are reserved words, are instead in Ouroboros variables.
As such, this gives programmers the ability to create their own custom structures, of similar power.

This gives powerful tools to programmers, so it will be possible for people to write *really* bad code in this language.
That said, it is possible to write really bad code in any language.
As with all powerful tools, it's up to the user not to hurt themselves.

## Expressiveness

### Control structures

For most purposes, the standard control structures suffice.
But every now and again, you need a control structure that doesn't quite fit.
As Ouroboros blocks are just functions, this means you can write your own control structures.

For example:

```
do_twice = f => {
    f();
    f();
};
```

defines a `do_twice` control structure, that runs its block twice.
You can then use it like so:

```
a = 0;

do_twice {
    a = a + 1;
};

print(a);
```

which prints `2`.

### Simplify component communication

Through use of decorators and compile time variables, can write code for multiple systems as though they're just one.

For example, you can define the decorator:

```
ServerSideFunction = path => f => {
    if (IS_SERVER) {
        my_server.serve(path, f);
        return f;
    } else {
        return () => http.get(path);
    };
};
```

and decorate functions like so:

```
get_current_user = ServerSideFunction("/user") {
    # Do stuff with db to get user
};
```

Then the server-side code presents the `/user` endpoint, and when `get_current_user` is called, it calls the database directly.
Meanwhile, in the client-side code, this function instead makes a HTTP GET call to that same endpoint.

This is similar to the Javascript idea of "isomorphic code".

Further, there is no need to restrict ourselves to a client-server relationship.
We could write code for an arbitrary number of components, as though they were all on the same machine.

## Technical ideas

Some technical ideas of language features to come:

### Able to iterate over statements in a function

For ease of compiling/meta-programming.

### Equality of functions

Two functions `f`, and `g` are considered equal (`f == g`) if they are defined at the same point in the source code, and their containing scopes are equal.
Scopes are equal if the functions creating them are equal, and all of their variables are equal.

I've considered having `f == g` if they are
[alpha equivalent](https://en.wikipedia.org/wiki/Lambda_calculus#Alpha_equivalence),
but decided against it, as two functions may be alpha equivalent, but not
[semantically equivalent](https://en.wikipedia.org/wiki/Semantic_equivalence).

eg. The constructors

```
person = (name, age) => { ... };
company = (name, age) => { ... };
```

may happen to be alpha equivalent, but they represent different objects.

### Ability to modify the syntax from within the language

Bit of a long-term goal.
Not thought too much about this, yet.

Ideally, I want to be able to completely rewrite the syntax of the language from within itself.
To demonstrate this, I'd like to be able to start with something C-like, and end up with
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Setup

Ensure Python is installed.
Ouroboros is developed in Python 3.6, but may work in other versions.
Then run

    pip install -r requirements.txt

## Usage

Ouroboros is currently written as an interpreter, in Python.

    python -m ouroboros [-h] [file]

## Examples

Look in the [`examples`](examples) directory for a number of examples.
