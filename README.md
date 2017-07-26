# Ouroboros

Ouroboros is an experimental programming language.

It will attempt to abstract away things that most languages do not, and experiment with what powerful tools this gives programmers.
As such, it will be possible for people to write *really* bad code in this language.

That said, it is possible to write really bad code in any language.
Like a sharp knife, this will be a powerful tool.
We make no attempt to stop this, it's up to the user not to cut themselves.

## Plan

### No keywords

There are no special words in this language, and no special notations for functions.
Nothing is sacred.

```
some-variable = 1;
some-function = {
    print "Hi";
};
```

Loops are just another sort of statement, and so need a semicolon after them.

```
i = 0;
while (i < 10) {
    print i;
    i = i + 1;
};
```

All things that are normally keywords are just functions.
All of them.

```
equals = =;
x equals 1;

y equals print;

y x;
```

### Functions are classes are scopes

Basically unify the standard uses of `{}`.

#### Scopes are functions

Consider a standard `if` statement.

    if (x > 0) { ... };

If we take the block on the end to be another function, we can define `if` to be simply a function in the meta-language

    if = condition => body => { ... };

where `if` calls the argument `body` only when `condition` is true.

##### Return statements

This makes `return` statements interesting.
How does

```
f = x => {
    if (x > 10) {
        return 10;
    } else {
        return x;
    };
};
```

know to return from the `f`, and not just the `if`?

#### Classes are functions

Suppose that, if a function terminates without returning anything, then it returns an object representing it's own scope.

For example, if we had

```
color = (red, green, blue) => {};

hot-pink = color(255, 105, 180);
```

Then `hot-pink.red` would return `255`.

We could also have more complicated functions

```
color = (red, green, blue) => {
    (hue, saturation, lightness) = rgb-to-hsl(red, green, blue);
};
```

In which case `hot-pink.red` would still be `255`, while `hot-pink.hue` would be `220`.

##### Modification risks

Naturally, this runs the risk of someone modifying the RGB, without modifying the HSL to match.

We could instead write

```
color = (red, green, blue) => {
    get-hsl = {
        return rgb-to-hsl(red, green, blue);
    };
};
```

So that `hot-pink.get-hsl()` returns `(220, 240, 169)`.

##### Everything is public

This would mean that all members of a class are public.

For example, imagine a naïve `user` class.

```
user = (username, password) => {
    user-id = get-user-id(username, password);

    if (!user-id) {
        return();
    };
};
```

Then `current-user.password` would be available, even if we don't want it to be.

One solution would be to separate the object from it's initialization logic.

```
user = (user-id, username) => {};

login-user = (username, password) => {
    user-id = get-user-id(username, password);

    if (!user-id) {
        return();
    };

    return user(user-id, username);
};
```

Another would be the ability to delete a variable from a scope.

```
user = class (username, password) => {
    user-id = get-user-id(username, password);

    if (!user-id) {
        return();
    };

    del password;
};
```

There are more solutions, but I won't list them all here.

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
Ouroboros is developed in Python 3.5, but may work in other versions.
Then run

    pip install -r requirements.txt

## Usage

Ouroboros is currently written as an interpreter, in Python.

    python -m ouroboros [-h] [file]

## Examples

Look in the [`examples`](examples) directory for a number of examples.
